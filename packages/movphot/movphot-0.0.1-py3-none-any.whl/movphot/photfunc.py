#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Color photmetry main functions
"""
import pandas as pd
import numpy as np
from scipy.ndimage import median_filter
from skimage.morphology import binary_dilation, disk
import os
import sep
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import mpl_toolkits.axes_grid1
import astropy.io.fits as fits
from astropy.wcs import WCS as wcs
import astropy.units as u
from astropy.stats import sigma_clipped_stats

from movphot.common import calc_xy, remove_close, remove_edge
from movphot.visualization import plot_photregion


kernel_7x7 = np.array([
 [1., 3., 5., 6., 5., 3., 1.],
 [3., 7.,13.,15.,13., 7., 3.],
 [5.,13.,21.,25.,21.,13., 5.],
 [6.,15.,25.,30.,25.,15., 6.],
 [5.,13.,21.,25.,21.,13., 5.],
 [3., 7.,13.,15.,13., 7., 3.],
 [1., 3., 5., 6., 5., 3., 1.],
])


def calc_time_shift(shape, x, y):
  """Calculate time-shift from the (1,1) pixel.

  Args:
    img: an nd array with (nx,ny) dimension
    x: NAXIS1 coordinate of the target
    y: NAXIS2 coordinate of the target

  Returns:
    The timeshift value in units of second.
  """

  nx,ny = shape
  if nx==2000 and ny==1128:
    return (930+2160+1000+np.floor(nx/4)*25)*np.floor(y/4)*100e-9
  else:
    return (930+2160+975+np.floor(nx/4)*25)*np.floor(y/4)*100e-9


def wrap_angle(angles):
   """Force angles within (-90.0, +90.0)
   """
   angles[angles>np.pi/2.0] -= np.pi
   angles[angles<-np.pi/2.0] += np.pi
   return angles


def tomoegain(gain_kwd):
  """
  Obtain inverse gain from header keyword

  Parameter
  ---------
  gain_kwd : str
    header keyword about gain ("high" etc.)
  
  Return
  ------
  gain : float
    inverse gain in e-/ADU
  """
  dic = dict(high=0.23)
  return dic[gain_kwd]


def triccsgain(gain_kwd):
  """
  Obtain inverse gain from header keyword

  Parameter
  ---------
  gain_kwd : str
    header keyword about gain ("x4" etc.)
  
  Return
  ------
  gain : float
    inverse gain in e-/ADU
  """

  gain_kwd = gain_kwd.strip()
  dic = dict(x32=0.19, x16=0.38, x8=0.76, x4=1.5, x2=3, x1=6)
  return dic[gain_kwd]


def bandcheck(catalog, band):
  """Check whether the band in catalog.
  """
  if catalog=="gaia":
    bands = ["G"]
  elif catalog=="ps":
    bands = ["u", "g", "r", "i", "z"]
  elif catalog=="sdss":
    bands = ["g", "r", "i", "z", "y"]
  elif catalog=="usnob":
    bands = ["R", "I"]
  
  if band in bands:
    return True
  else:
    return False


def search_param(w, nx, ny):
  """Obtain catalog search parameters.

  Parameters
  ----------
  w : astropy.wcs.WCS
    wcs information of the fits
  nx, ny : float
    number of pixels 

  Returns 
  -------
  cra, cdec : float
    ra and dec of field of view center
  fovradius : float
    radius of field of view
  """

  # Ra and Dec of center 
  cra, cdec  = w.all_pix2world(nx/2., ny/2., 0)
  # Width of search region.
  edge_1 =  w.all_pix2world(0, 0, 0)
  edge_2 =  w.all_pix2world(nx, ny, 0)
  width_ra = abs(edge_1[0]-edge_2[0])/2.
  width_dec = abs(edge_1[1]-edge_2[1])/2.
  fovradius = max(width_ra, width_dec)
  return cra, cdec, fovradius


def create_saturation_mask(image, satu_count, nloop=1):
  """ Create a 2D mask image from the first frame using SEXtractor
  """
  minimum_detection_area = 1.0
  mask_radius            = 15.0
  mask_dilation_radius   = 10.0

  mask = np.zeros(image.shape, dtype=np.bool)
  obj = sep.extract(image, satu_count, filter_kernel=kernel_7x7, 
          minarea=minimum_detection_area, err=None, mask=None)
  sep.mask_ellipse(mask, obj['x'], obj['y'],
        obj['a'], obj['b'], obj['theta'], r=mask_radius)
  mask = binary_dilation(mask, disk(mask_dilation_radius))
  return mask


def remove_background2d(image, mask):
  ''' Remove background from 2D FITS
  '''
  bg_engine = sep.Background(image, mask=mask)
  bg_engine.subfrom(image)
  bg_global = bg_engine.globalback
  bg_rms = bg_engine.globalrms
  bg_info = {'level': bg_global, 'rms': bg_rms}
  return image, bg_info


def obtain_winpos(data, x, y, radius):
  """ # x y and should be numpy.ndarray
  Parameters
  ----------
  """

  # radius should be large enough to obtain total flux
  wpos_param  = 2.0/2.35
  frad_frac   = 0.5
  frad_subpix = 5
  frad_ratio  = 5.0

  # Photometry at first to obtain all flux
  # (err and gain are useless for flux estimation)
  flux,fluxerr,eflag = sep.sum_circle(data, x, y, r=radius)
  # Use nonzero eflag
  # x, ym flux
  # r = 0.5*fwhm
  # radius is not used when norm flux is used
  radius = np.full_like(x, radius)
  r, flag = sep.flux_radius(
    data, x, y, radius, frad_frac,
    normflux=flux, subpix=frad_subpix)
  sigma = wpos_param*r
  # wflag is always 0 if mask=None
  xwin, ywin, wflag = sep.winpos(data, x, y, sigma)
  
  # If differences are large ( > 0.3*radius), return 1
  diff = np.sqrt((xwin-x)**2 + (ywin-y)**2)
  flag = np.where(diff > 0.3*radius, 1, 0)
  ratio_1 = np.sum(flag)/flag.size 
  if ratio_1 > 0.3:
    print(f"    Large winpos correct ratio :{ratio_1:.1f}")
    print(f"    Please check wcs information etc.")
  return xwin, ywin, flag


def photloc_xy(src, df, radius, gain, err, mask=None, ann=False):
  """
  Photometry using x and y.
  Save original x/y as x0/y0 and used x/y as x1/y1.
  Create pandas.DataFrame which contains both 
  catalog magnitude and photometric result.

  Parameters
  ----------
  src : array-like
    input data
  df : pandas.DataFrame
    input DataFrame
  gain : float
    inverse gain in e-/ADU
  err : float
    typical photometric error in ADU
  mask : array-like, optional
    boolian mask
  ann : bool, optional
    whether use annulus to do photometry

  Return
  ------
  df : pandas.DataFrame
    result DataFrame
  """

  image = src.data.byteswap().newbyteorder()
  hdr = src.header
  w = wcs(header=hdr)

  # Origianl coodinates.
  x0, y0  = df["x"], df["y"]

  # Obtain winpos.
  image = image.byteswap().newbyteorder()
  xwin, ywin, flag = obtain_winpos(image, x0, y0, radius)
  # If error is large (due to no detection etc.), use x0 and y0 for photometry.
  xwin = np.where(flag==1, x0, xwin)
  ywin = np.where(flag==1, y0, ywin)
  rawin, decwin = w.all_pix2world(xwin, ywin, 0)

  # Do photometry using winpos.
  flux, fluxerr, eflag = sep.sum_circle(
    image, xwin, ywin, r=radius, err=err, mask=mask, gain=gain)
  
  # Add to the DataFrame
  df["x1"] = xwin
  df["y1"] = ywin
  df["ra1"] = rawin
  df["dec1"] = decwin
  df["flux"] = flux
  df["fluxerr"] = fluxerr
  df["eflag"] = eflag
  
  # Use positive flux data
  df = df[df["flux"]>0]
  df = df[df["fluxerr"]>0]

  # Add constant values.
  df["radius"] = radius
  df["gain"] = gain

  df = df.reset_index(drop=True)
  return df


def merge_objects(objects, segmap, epsilon, min_samples=2):
  ''' Merge separately-detected objects by DBSCAN

  Paramters:
    objects (ndarray): structured array generated by SExtractor
    segmap (ndarray): segmentation map generated by SExtractor
    epsilon (float): range parameter for clustering
    min_samples (int): minimum cluster size

  Returns:
    objects (ndarray): array where separated objects are merged
    segmap (ndarray): updated segmentation map
  '''
  engine = dbscan_engine(eps=epsilon, min_samples=min_samples)
  xy = np.array((objects['x'],objects['y'])).copy().T
  clusters = engine.fit(xy)
  labels = clusters.labels_
  merged,done,newmap = list(), list(), np.zeros_like(segmap)
  for n,idx in enumerate(labels):
    obj = objects[n]
    if idx in done:
      continue
    if idx != -1:
      done.append(idx)
      objs = objects[idx==labels]
      for key in obj.dtype.names:
        if key in sum_keywords:
          obj[key] = objs[key].sum()
        elif key in max_keywords:
          obj[key] = objs[key].max()
        elif key in min_keywords:
          obj[key] = objs[key].min()
        elif key in peak_keywords:
          obj[key] = objs[key][objs['peak'].argmax()]
        elif key in or_keywords:
          obj[key] = reduce(np.bitwise_or, objs[key].astype('int'))
        else:
          obj[key] = objs[key].mean()
          tmpmap = reduce(np.logical_or,
              [segmap==(s+1) for s in np.argwhere(labels==idx)])
    else:
      tmpmap = segmap==(n+1)
    merged.append(obj.copy())
    newmap += (len(merged))*tmpmap
  return np.array(merged),newmap


def sum_isophot(image,segmap,r,err,mask=None,gain=None):
  ''' Measure source fluxes by isophotal photometry
  Return fluxerr=0 for minus flux data.

  Parameters:
    image (ndarray): image to be measured
    segmap (ndarray): segmentation map generated by SExtractor
    r (int): disk radius for mask dilation
    err (float): standard error per pixel
    mask (ndarray): bad pixel mask
    gain (float): sensor gain (e-/ADU)

  Returns:
    flux (ndarray): measured flux
    fluxerr (ndarray): uncertainty
    isomap (ndarray): area map in photometary
  '''
  ny,nx = image.shape
  nz = segmap.max()
  isomap = np.zeros((nz,ny,nx))
  flux,fluxerr = np.zeros(nz),np.zeros(nz)
  for n in range(nz):
    isomask = binary_dilation(segmap==(n+1), disk(r))
    if mask is not None: isomask = isomask & (~mask)
    flux[n] = image[isomask].sum()
    fluxerr[n] = err*np.sqrt(isomask.sum())
    if gain: 
      if flux[n] <= 0:
        fluxerr[n] = -1
      else:   
        fluxerr[n] += np.sqrt(flux[n]/gain)
    isomap[n] = isomask
  return flux,fluxerr,isomap



def photiso(
  image, stddev, sigma=3, r_disk=2, epsilon=20, minarea=3, gain=None):
  """
  Parameters
  ----------
  image : array-like
    2-d image
  stddev : float
    typical flux standard deviation
    use stddev times sigma for extraction
  sigma : int
    extraction threshold in  object-merging process
    use stddev times sigma for extraction
  r_disk : float
    disk size of isophotal photometry in pixel
  epsilon : int
    range parameter in object-merging process in pixel
  minarea : int
    minimum area in object-merging process in pixel
  gain : float, optional
    inverse gain in e-/ADU

  Return
  ------
  df : pandas.DataFrame
    resuls DataFrame
  objects : sep.extract
    extracted objects 
  isomap : array-like
    area map in photometary
  """
  
  # radius for aperture photometry in pixel
  radius = 10
  
  # set segmentation_map=True to create a segmentation map
  objects, segmap = sep.extract(
    image, sigma, err=stddev,
    minarea=minarea, filter_kernel=kernel_7x7,
    segmentation_map=True)

  # merge separated objects by DBSCAN
  objects, segmap = merge_objects(objects, segmap, epsilon)

  # measure flux and flux error by circle apertures
  aper_flux, aper_fluxerr, flag = sep.sum_circle(
    image, x=objects['x'], y=objects['y'], r=radius, err=stddev, gain=gain)

  # measure flux and flux error by isophotal apertures
  iso_flux, iso_fluxerr, isomap = sum_isophot(
    image, segmap, r=r_disk, err=stddev, gain=gain)
  
  df = pd.DataFrame({
      "x": objects["x"], "y": objects["y"], 
      "iso_flux": iso_flux, "iso_fluxerr": iso_fluxerr, 
      "aper_flux": aper_flux, "aper_fluxerr": aper_fluxerr,
      })
  return df, objects, isomap


def merge_photres_xy(df_phot, df_obj, radius=10):
  """Merge photometory result and object(s) using x,y.

  Parameters
  ----------
  df_phot : pandas.DataFrame
    input DataFrame which should have x and y
  df_obj : pandas.DataFrame
    input DataFrame which should have x and y
  radius : float
    matching radius in x,y 

  Return
  ------
  df : pandas.DataFrame
    merged DataFrame
  """
  for idx,row_phot in df_phot.iterrows():
    df_temp_obj = (
      df_obj[((row_phot["x"]-df_obj["x"])**2 
      + (row_phot["y"]-df_obj["y"])**2)**0.5 < radius])
    if len(df_temp_obj)==1:
      df_temp_obj["flux"] = row_phot["iso_flux"]
      df_temp_obj["fluxerr"] = row_phot["iso_fluxerr"]
      df_temp_obj["xiso"] = row_phot["x"]
      df_temp_obj["yiso"] = row_phot["y"]
      res.append(df_temp_obj)
    else:
      pass

  df = pd.concat(res, axis=0)
  df = df.reset_index(drop=False)
  return df


def appphot_loc(
    src, x, y, err, mask, hdr_kwd, radius, photmap):
  """Do photometry for specific object.

  Parameters
  ----------
  src : str
    target fits
  x,y : float
    photometry coordinates
  err : float
    background rms
  mask : array-like
    photometry mask
  hdr_kwd : dict
    header keyword
  radius : float
    aperture radius in pixel
  photmap : str or bool
    mapping photometry area

  Return
  ------
  df_obj : pandas.DataFrame
    photometory result DataFrame
  """

  image = src.data.byteswap().newbyteorder()
  hdr = src.header
  w = wcs(header=hdr)

  # Obtain gain value.
  gain = hdr[hdr_kwd["gain"]]
  if hdr_kwd["gain"]=="GAINCNFG":
    # Convert str(ex. x4) to float value(1.5)
    gain = triccsgain(gain)

  # Create DataFrame
  df_obj = pd.DataFrame(dict(x=x, y=y))

  # Do photometry using x and y.  (add flux and fluxerr to the DataFrame)
  df_obj = photloc_xy(
    src, df_obj, radius, gain, err, mask)
  
  # Photometry mapping
  if photmap:
    plot_photregion(image, err, df_obj, radius, photmap)

  df_obj = df_obj.reset_index(drop=True)
  return df_obj


def isophot_loc(
    src, err, hdr_kwd, orb, radius, photmap):
  """Do isophotla photometry for specific object.

  Parameters
  ----------
  src : str
    target fits
  err : float
    background rms
  hdr_kwd : dict
    header keyword
  orb : neoorb class
    neo orbit
  radius : float
    aperture radius in pixel
  ann : bool, optional
    whether use annulus to estimate background noise of the source

  Return
  ------
  df_obj : pandas.DataFrame
    photometory result DataFrame
  return df
  """
  image = src.data.byteswap().newbyteorder()
  hdr = src.header
  w = wcs(header=hdr)

  # Obtain gain value.
  gain = hdr[hdr_kwd["gain"]]
  if hdr_kwd["gain"]=="GAINCNFG":
    # Convert str(ex. x4) to float value(1.5)
    gain = triccsgain(gain)

  # Create DataFrame
  df_obj = pd.DataFrame(dict(x=x, y=y))

  # Do isophotal photometry (add flux and fluxerr to the DataFrame)
  ## Extract and do photometry of all objects.
  df_iso, objects, isomap = photiso(
    image, err, sigma, r_disk, epsilon, minarea, gain)
  ## Merge df_iso (isophot result) and df_obj (object) using x, y.
  df = merge_iso_xy(df_iso, df_obj, radius=10)


  df_obj = df_obj.reset_index(drop=True)
  return df_obj


def appphot_catalog(
    src, df_cat, err, mask, hdr_kwd, radius, radius_edge=None, photmap=None):
  """
  Do aperture photometry of stars in catalog.
  Assume all data are already background subtracted
  and not mask saturated stars.

  Parameters
  ----------
  src : HDU object
    HDU object of target fits
  df_cat : pandas.DataFrame
    catalog DataFrame
  err : float or array-like
    standard deviation of sky background
  mask : array-like
    mask array when photometry
  hdr_kwd : dict
    header keyword
  radius : float
    photometry radius in pixel
  radius_edge : float, optional
    edge radius to be removed
  photmap : str, optional
    whether plot photometry regions. if plot, set output file path

  Return
  ------
  df_cat : pandas.DataFrame
    photometry result added DataFrame
  """
  
  image = src.data.byteswap().newbyteorder()
  hdr = src.header
  w = wcs(header=hdr)
  ny, nx = image.shape
  

  gain = hdr[hdr_kwd["gain"]]
  if hdr_kwd["gain"]=="GAINCNFG":
    # Convert str(ex. x4) to float value(1.5)
    gain = triccsgain(gain)

  # Do photometry using x and y.  (add flux and fluxerr to the DataFrame)
  df_cat0 = photloc_xy(
    src, df_cat, radius, gain, err, mask)
  print(f"    N_ref={len(df_cat0)} (after photometry           )")

  # Remove objects near edge 
  if radius_edge:
    df_cat1 = remove_edge(df_cat0, radius_edge, nx, ny)
    print(f"    N_ref={len(df_cat1)} (after edge objects removal)")
    df_cat = df_cat1.reset_index(drop=True)
  else:
    df_cat = df_cat0.reset_index(drop=True)
  # Photometry mapping
  if photmap:
    plot_photregion(image, err, df_cat, radius, photmap, df_cat0)

  return df_cat


def isophot_catalog(
    src, df_cat, err, mask, hdr_kwd, r_disk, epsilon, minarea, sigma, 
    photmap=None):
  """Do photometry for reference stars.

  Define header keyword for murikabushi.
  Do not mask saturated stars.

  Parameters
  ----------
  src : str
    target fits
  err :
    ho
  band : str
    g, r, i or z band of target fits
  magmin, magmax : float
    magnitude to be searched
  r_disk : float
    disk size of isophotal photometry in pixel
  epsilon : float
    range parameter in object-merging process')
  minarea : int
    minimum area in object-merging process in pixel
  sigma : int
    extraction threshold in  object-merging process
    use stddev times sigma for extraction
  ps : str,
    Pan-STARRS catalog style (db for homemade database or query)
  table : str,
    table name of homemade database
  photmap : str, optional
    whether plot photometry regions. if plot, set output file path

  Returns
  -------
  df : pandas.DataFrame
    photometry result DataFrame
  """

  image = src.data.byteswap().newbyteorder()
  hdr = src.header
  w = wcs(header=hdr)
  ny, nx = image.shape

  # Center of cordinate and radius of catalog search region.
  cra, cdec, fovradius = search_param(w, nx, ny)

  # Extract Pan-STARRS catalog information.
  if self.catalog=="ps":
    df_cat = extract_ps(
      db, table, cra, cdec, fovradius, magmin, magmax)

  # Calculate x, y of catalog stars
  df_cat = calc_xy(df_cat, w)

  # Obtain gain value.
  gain = hdr[hdr_kwd["gain"]]
  if hdr_kwd["gain"]=="GAINCNFG":
    # Convert str(ex. x4) to float value(1.5)
    gain = triccsgain(gain)

  # apply median filter before exract (drop cosmic rays and bad pixels)
  image = median_filter(image, size=3)


  # Do isophotal photometry (add flux and fluxerr to the DataFrame)
  ## Extract and do photometry of all objects.
  df_iso, objects, isomap = photiso(
    image, err, sigma, r_disk, epsilon, minarea, gain)
  ## calculate objects radec from x, y
  df_iso = calc_radec(df_iso, w)
  ## Merge df_iso (isophot result) and df_cat (catalog stars) using x, y.
  df = merge_iso_xy(df_iso, df_cat, radius=10)

  # Remove close objects and objects in edge region.
  df = remove_dist(df, radius, nx, ny)

  df = df.reset_index(drop=True)
  return df
