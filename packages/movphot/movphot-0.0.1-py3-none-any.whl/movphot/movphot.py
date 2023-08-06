#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Relative photometory class using Gaia/Pan-STARRS catalog.
This function tracks moving objects (e.g. asteorids etc.).

Dependence
----------
class Movhot ---- photfunc.py ----- [catalog object photmetry]
                     |               appphot_catalog, isophot_catalog
                     |
                     |
                     | ------------ [object photometry]
                                     apphot_loc, isophot_loc
"""
import os
import sys
import pandas as pd
import numpy as np
import sep
import astropy.io.fits as fits
from astropy.wcs import WCS as wcs
from astropy.time import Time
import matplotlib.pyplot as plt
import time
import datetime 

# Functions to handle database.
from movphot.common import log10err, adderr_series, time_keeper
from movphot.photfunc import *
from movphot.visualization import mycolor, mymark, plot_photregion 
from movphot.psdb import extract_ps


class Movphot:
  def __init__(
    self, inst, obj, refmagmin, refmagmax,
    radius_mask, param_app=None, param_iso=None):
    """
    Note: (ref:app and obj:iso) situation is not available now.

    Parameters
    ----------
    inst : str
      instrument name to deternime header kwyword
    obj : str
      object name used to choice handmade database table
    refmagmin/refmagmax : float
      minimum/maximum magnitude of reference star
    param_app_ref : dict, optional
      apperture photometry parameter (radius)
    param_app_obj : dict, optinaol
      apperture photometry parameter (radius)
    param_iso : dict, optional
      isophotal photometry parameter (r_disk, epsilon, sigma, minarea)
    """

    # Define header keywords.
    if inst=="TriCCS":
      # Example
      # DATE-OBS= '2021-03-08'         / observation date
      # UTC     = '2021-03-08T15:46:18.152736' / exposure starting date and time
      # TFRAME  =           0.99646400 / [s] frame interval in seconds
      # GAINCNFG= 'x4      '           / sensor gain setting
      self.hdr_kwd = dict(
        datetime="UTC", date="DATE-OBS", time=None, 
        exp="TFRAME", gain="GAINCNFG")
      # 0.34 arcsec/pixel
      self.p_scale = 0.34
      # Saturation count ? 
      self.satu_count = 15000.
      # Dead zone 
      # not used region is dead_pix + radius
      # from 2021CC2, 2021/02/24
      self.dead_pix = 30

    if inst=="murikabushi":
        # DATE-OBS= '2020-10-28'         /  [yyyy-mm-dd] Observation start date
        # UT      = '14:10:15.84'        / [HH:MM:SS.SS] Universal Time at start
        # EXPTIME =               30.000 / [sec] Exposure time
        # GAIN    =                 1.70 / [e-/ADU] CCD gain
      self.hdr_kwd = dict(
        datetime=None, date="DATE-OBS", time="UT", 
        exp="EXPTIME", gain="GAIN")
      # 0.72 arcsec/pixel
      self.p_scale = 0.72
      # Saturation count ? 
      self.satu_count = 15000.
      self.dead_pix = 0
    if inst=="tomoe":
      # Saturation count ? 
      self.satu_count = 25000.
      self.dead_pix = 0
      pass
    self.inst = inst

    ## Photometry type of reference stars (app or iso).
    self.radius = param_app["radius"]
    self.r_disk = param_iso["r_disk"]
    self.epsilon = param_iso["epsilon"]
    self.sigma = param_iso["sigma"]
    self.minarea = param_iso["minarea"]

    self.refmagmin = refmagmin
    self.refmagmax = refmagmax
    self.radius_mask = radius_mask
    self.obj = obj
    self.table = f"_{obj}"
 
  
  def set_catalog(self, catalog, dbdir):
    """Set catalog for reference star photmetry.

    Parameter
    ---------
    catalog : str
      catalog name
    dbdir : str
      databse directory 
    """
    catalogs = ["gaia", "ps"]
    assert catalog in catalogs, f"Invalid catalog : {catalog}."
    self.catalog = catalog

    if catalog=="gaia":
      self.db = os.path.join(dbdir, "gaia.db")
      self.kwd_ra = "ra"
      self.kwd_dec = "dec"
      self.kwd_objID = "objID"
    if catalog=="ps":
      self.db = os.path.join(dbdir, "ps.db")
      self.kwd_ra = "raMean"
      self.kwd_dec = "decMean"
      self.kwd_objID = "objID"


  @time_keeper
  def remove_background(self, src, mask):
    """Subtract backgraound and add its infomation.

    Parameter
    ---------
    src : HDU object
      fits HDU 
    """
    image = src.data.byteswap().newbyteorder()
    image, bg_info = remove_background2d(image, mask)
    # Insert background subtracted image
    src.data = image
    self.bg_level = bg_info["level"]
    self.bg_rms = bg_info["rms"]


  @time_keeper
  def create_mask(self, src, band):
    """Create mask from reference star and sep.extract.

    Parameters
    ----------
    src : HDU object
      fits HDU 
    band : str
      band of objects in catalog
    """
    image = src.data.byteswap().newbyteorder()
    ny, nx = image.shape
    hdr = src.header
    w = wcs(header=hdr)

    # # Create mask of extracted objects.
    # ext_mask = create_ext_mask(image, err=self.bg_rms)
    # Create mask of saturated objects.
    satu_mask = create_saturation_mask(image, self.satu_count)

    # Create mask of catalog objects.
    ## Center of cordinate and radius of catalog search region.
    cra, cdec, fovradius = search_param(w, nx, ny)
    if self.catalog=="gaia":
      df_cat = extract_gaia(
        self.db, self.table, cra, cdec, fovradius, 
        self.refmagmin, self.refmagmax)
    elif self.catalog=="ps":
      df_cat = extract_ps(
        self.db, self.table, cra, cdec, fovradius, 
        self.refmagmin, self.refmagmax)
    x, y  = w.all_world2pix(df_cat[self.kwd_ra], df_cat[self.kwd_dec], 0)
    cat_mask = np.zeros(image.shape, dtype=np.bool)
    sep.mask_ellipse(cat_mask, x, y, a=1, b=1, theta=0, r=self.radius_mask)

    self.mask = satu_mask|cat_mask


  def obtain_time_from_hdr(self, hdr):
    """Obtain time information from header.
  
    Parameters
    ----------
    hdr : 
      header
    """
    hdr_kwd = self.hdr_kwd

    if hdr_kwd["datetime"]:
      exp_start = hdr[hdr_kwd["datetime"]]
    else:
      exp_start = f"{hdr[hdr_kwd['date']]}T{hdr[hdr_kwd['time']]}"
    exp_frame = hdr[hdr_kwd["exp"]]
    obs_start = datetime.datetime.strptime(exp_start, "%Y-%m-%dT%H:%M:%S.%f")
    obs_center = obs_start + datetime.timedelta(seconds=exp_frame/2.0)
    obs_center = datetime.datetime.strftime(obs_center, "%Y-%m-%dT%H:%M:%S.%f")
    t = Time(str(obs_center), format='isot', scale='utc')
    self.t_utc = t
    self.t_mjd = t.mjd
    self.t_jd = t.jd


  def add_photmetry_info(self, df):
    """
    Add common constant values for all star/object in a fits
    (bg_level, bg_rms and time ) to input DataFrame.
    Gain should be added when photometry.

    Parameter
    ---------
    df : pandas.DataFrame
      dataframe
    """
    # Add bg info.
    df["bg_level"] = self.bg_level
    df["bg_rms"] = self.bg_rms
    df["t_utc"] = self.t_utc
    df["t_jd"] = self.t_jd
    df["t_mjd"] = self.t_mjd


  def add_instrumental_info(self, df):
    """
    Add instrumental information to input DataFrame.
    Gain should be added when photometry.

    Parameter
    ---------
    df : pandas.DataFrame
      dataframe
    """
    # Add pixel scale.
    df["p_scale"] = self.p_scale
    df["inst"] = self.inst

  @time_keeper
  def phot_catalog(self, src, phottype, band, photmap):
    """Do photometry using stars in catalog.
 
    Parameters
    ----------
    src : HDU object
      fits source
    phottype : str
      "app" (apperture) or "iso" (isophotal)
    catalog : str
      catalog of stars (gaia, PS, SDSS or USNOB)
    band : str
      band of filter ("g", "r", "i", "z", "R", "I" etc.)
    photmap : bool
      whether create photometry region map

    Return 
    ------
    df : pandas.DataFrame
      photometry result dataframe
    """

    # Band check
    assert bandcheck(self.catalog, band), f"Check {self.catalog} {band}"

    image = src.data.byteswap().newbyteorder()
    ny, nx = image.shape
    hdr = src.header
    w = wcs(header=hdr)
    # Center of cordinate and radius of catalog search region.
    cra, cdec, fovradius = search_param(w, nx, ny)
    
    # Obtain lots of objects using loose magnitude threshold 
    if self.catalog=="gaia":
      df_cat = extract_gaia(
        self.db, self.table, cra, cdec, fovradius, 
        self.refmagmin, self.refmagmax)
    elif self.catalog=="ps":
      df_cat = extract_ps(
        self.db, self.table, cra, cdec, fovradius, 
        self.refmagmin, self.refmagmax)
    print(f"    N_ref={len(df_cat)} (after extraction from catalog broad FoV)")
    assert len(df_cat)!=0, "No reference stars were detected."
    
    # Calculate x, y of catalog stars
    df_cat = calc_xy(df_cat, w)
    # Use objects in FoV 
    df_cat = df_cat[(df_cat["x"] > 0) & (df_cat["x"] < nx) 
                    & (df_cat["y"] > 0) & (df_cat["y"] < ny) ]
    print(f"    N_ref={len(df_cat)} (objects in FoV)")

    # Remove close objects using photometry radius
    # Use 2 * aperture radius just in case
    df_cat = remove_close(df_cat, 2*self.radius)
    print(f"    N_ref={len(df_cat)} (after close objects removal)")


    # Do photometery
    # Remove objects located near other stars or edge in the functions
    if phottype=="app":
      # Do not use edge region
      radius_edge = self.dead_pix + self.radius
      df_ref = appphot_catalog( 
        src, df_cat, self.bg_rms, None, self.hdr_kwd, 
        self.radius, radius_edge, photmap)

    elif refphot=="iso":
      df_ref = isophot_catalog(
        src, df_cat, self.bg_rms, None, self.hdr_kwd, 
        self.r_disk, self.epsilon, self.minarea, 
        self.sigma, self.magmin, self.magmax, 
        self.db, self.table, photmap)

    df_ref = df_ref.reset_index(drop=True)
    return df_ref


  @time_keeper
  def phot_loc(
    self, src, phottype, x, y, photmap):
    """Do Photometry of target object.
 
    Parameters
    ----------
    src : HDU object
      fits source
    phottype : str
      "app" (apperture) or "iso" (isophotal)
    x, y : float
      object location in pixel
    photmap : bool
      whether create photometry region map

    Return 
    ------
    df_obj : pandas.DataFrame
      photometry result dataframe
    """

    if phottype=="app":
      df_obj = appphot_loc(
        src, x, y, self.bg_rms, self.mask, self.hdr_kwd, 
        self.radius, photmap)
 
    elif phottype=="iso":
      df_obj = isophot_loc(
        src, x, y, self.bg_rms, self.mask, self.hdr_kwd, 
        self.r_disk, self_epsilon, self.minarea, self.sigma, photmap)

    assert (len(df_obj) <= 1), "More than two objects detected."
    return df_obj

