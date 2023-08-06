#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Do relative photometory for 3-band data taken with the 
murikabushi/MITSuME or seimei/TriCCS.
2nd band(R for murikabushi, r for TriCCS) 
is used to predict orbit of the object.

Use colcommon, colphotlib, colplot.

Call photometry region plot as photmap (from photmetry map) in this script.

Output file is only 'photometry_result.csv'.
See README.md to create various figures.
Note: When objID = 518 and g,r,z photometry, there are
  gMeanPSFMag_518_g,  gMeanPSFMag_518_r, gMeanPSFMag_518_z
  in output csv.
  These have always the same values when not 0. 
  But sometimes 0 due to the detection close to the edge.

For moving object photometry (i.e. non-sidereal tracked image), 
you can use different photometry radius by setting radius_obj and radius_ref.


Example
---
without photmap
>>> phot_test 2021DX1 TriCCS glist9.txt rlist9.txt zlist9.txt wcs 
standardr9.txt --bands g r z --catalog ps --table _2021DX1 --radius_ref 25 
--radius_obj 25 --refphot app --objphot app --refmagmax 20 --refmagmin 12 

with photmap
>>> phot_test 2021DX1 TriCCS glist9.txt rlist9.txt zlist9.txt wcs 
standardr9.txt --bands g r z --catalog ps --table _2021DX1 --radius_ref 25 
--radius_obj 25 --refphot app --objphot app --refmagmax 20 --refmagmin 12 
--photmap
"""
import time
import os
import logging
import pandas as pd
import numpy as np
from argparse import ArgumentParser as ap
from argparse import ArgumentDefaultsHelpFormatter
from astropy.wcs import FITSFixedWarning
from astropy.wcs import WCS as wcs
import astropy.io.fits as fits
import warnings
# to ignore 
## WARNING: FITSFixedWarning: MJD-END = '59281.674688' / MJD at exposure end
## a floating-point value was expected. [astropy.wcs.wcs]
warnings.simplefilter('ignore', category=FITSFixedWarning)

import movphot.movphot as mp
#from movphot.src.movphot import Movphot
from movphot.common import (
  get_filename, obtain_objorb, modify_ref, concat_allband, extract_obj, nowstr)
from movphot.photfunc import obtain_winpos


def main(args=None):
  """This is the main function called by the `phot_color` script.

  Parameters
  ----------
  args : argparse.Namespace
    Arguments passed from the command-line as defined below.
  """
  parser = ap(
    description="Do multi-bands data relative photometry.",
    formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    "--obj", type=str, required=True,
    help="object name")
  parser.add_argument(
    "--inst", type=str, required=True, choices=["TriCCS", "murikabushi"],
    help="used instrument")
  parser.add_argument(
    "--flist", required=True, nargs="*", 
    help="fitslist of each bands")
  parser.add_argument(
    "--fitsdir", type=str, required=True,
    help='all fits directory')
  parser.add_argument(
    "--standard", type=str, required=True,
    help="standard fits list text")
  parser.add_argument(
    "--idx_standard", type=int, default=2,
    help="index of standard fits")
  parser.add_argument(
    "--bands", nargs="*", required=True,
    help="used bands")
  parser.add_argument(
    "--catalogs", nargs="*", required=True,
    help="catalog for each bands (ps, gaia, sdss, usnob)")
  parser.add_argument(
    "--radius_ref", type=int, default=15, 
    help="reference aperture radius for loc photal photometry in pixel")
  parser.add_argument(
    "--radius_obj", type=int, default=15, 
    help="object aperture radius for loc photal photometry in pixel")
  parser.add_argument(
    "--r_disk", type=int, default=15, 
    help="aperture disk radius for isophotal photometry in pixel")
  parser.add_argument(
    "--sigma", dest='sigma', type=int, default=3,
    help="extraction threshold in  object-merging process")
  parser.add_argument(
    "--epsilon", dest='epsilon', type=int, default=20,
    help='range parameter in object-merging process in pixel')
  parser.add_argument(
    "--minarea", dest='minarea', type=int, default=3,
    help='minimum area to be extracted in pixel')
  parser.add_argument(
    "--refphot",  type=str, default="app",
    help='choose loc to use app (faint object) or iso (bright)')
  parser.add_argument(
    "--objphot",  type=str, default="app",
    help='choose loc to use app (faint object) or iso (bright)')
  parser.add_argument(
    "--refmagmin", type=str, default="12.0", 
    help="minimum magnitude to be searched")
  parser.add_argument(
    "--refmagmax", type=str, default="18.0", 
    help="maximum magnitude to be searched")
  parser.add_argument(
    "--radius_mask", type=int, default=15, 
    help="mask radius in pixel")
  parser.add_argument(
    "-p", "--photmap", action='store_true',
    help='create photometry region map (a bit slow)')
  parser.add_argument(
    "--table",  type=str, default=None,
    help="table name of homemade database (see README.md)")
  parser.add_argument(
    "--dbdir",  type=str, default="~/db4movphot",
    help="database directory name")
  args = parser.parse_args()

  # Start time
  t0 = time.time()


  # Parse photometry parameters.
  param_app = dict(
    radius=args.radius_ref)
  param_iso = dict(
    r_disk=args.r_disk, epsilon=args.epsilon, 
    sigma=args.sigma, minarea=args.minarea)

  assert len(args.flist)==len(args.bands), f"Check fitslist and bands!"
  N_band = len(args.flist)

  fitsdir = args.fitsdir

  rmmin = "f".join(args.refmagmin.split("."))
  rmmax = "f".join(args.refmagmax.split("."))
  bands_str = "".join(args.bands)

  dbdir = args.dbdir


  ## Check fitslist dimensions
  for idx,f in enumerate(args.flist):
    with open(f, "r") as f:
      lines = f.readlines()
      n_line = len(lines)
      if idx==0:
        n_line_stan = n_line
      else:
        assert n_line == n_line_stan, "Check fitslists."
        pass


  ## Parse catalog.
  ## Use some catalogs for different system  (e.g. MITSuME g and RI)
  if len(args.catalogs)==1:
    catalogs = [args.catalogs[0]]*N_band
  else:
    catalogs = args.catalogs


  # Create output directory
  now = nowstr()
  filename = get_filename(args.standard)
  if args.refphot=="app":
    outdir = (
      f"{now}_app_"
      f"r{args.radius_ref}robj{args.radius_obj}"
      f"{args.objphot}rm{rmmin}to{rmmax}_"
      f"{bands_str}_{filename}")
  elif args.refphot=="iso":
    outdir = (
      f"{now}_iso_"
      f"rdisk{args.r_disk}sigma{args.sigma}eps{args.epsilon}ma{args.minarea}"
      f"{args.objphot}rm{rmmin}to{rmmax}_"
      f"{bands_str}_{filename}")
  os.makedirs(outdir, exist_ok=True)

  ## Create directory for photometry region png in output directory
  if args.photmap:
    photmapdir = os.path.join(outdir, "photregion")
    os.makedirs(photmapdir, exist_ok=True)
 

  # Construct Phot class
  ph = mp.Movphot(
    args.inst, args.obj, 
    args.refmagmin, args.refmagmax, 
    args.radius_mask, param_app, param_iso)


  # Do orbit prediction using idx_standard-th band(bright) data.
  flist_standard = args.flist[args.idx_standard]
  orb = obtain_objorb(ph.hdr_kwd, flist_standard, fitsdir, args.standard)
  

  # Do photometry of reference stars and target object simultaneously.
  # for loop (bands)
  #   for loop (fits)
  #     1. reference star
  #     2. target object
  ## List to save all band photometric results
  res_allband = []


  # Save arguments in log file.
  logging.basicConfig(
    filename=os.path.join(outdir, f"{args.obj}phot.log"), level=logging.DEBUG)
  logging.info("Parameters")
  for arg, value in sorted(vars(args).items()):
    logging.info(f"Argument {arg}: {value}")



  # For loop of bands
  for idx_band, (band, flist, catalog) in enumerate(
    zip(args.bands, args.flist, catalogs)):

    print(f"\n# Start {band}-band photometry")

    # Set catalog of the band
    ph.set_catalog(catalog, dbdir)

    # Open fitslist of the band
    with open(flist, "r") as f:
      # List to save 1 band photometric results
      res_1band = []
      f = f.readlines()
      # Number of frames
      N_frame = len(f)
      # For loop of fits 
      for idx_fits, line in enumerate(f):
        infits = line.split("\n")[0]
        print(f"  {band}-band Frame {idx_fits+1}/{N_frame} start")
        fitsID = get_filename(infits)
        infits = os.path.join(fitsdir, infits)
        # fits source  (HDU0, header + image data)
        src = fits.open(infits)[0]
        # fits header
        hdr = src.header
        # wcs information
        w = wcs(header=hdr)
        # fits image data
        image = src.data.byteswap().newbyteorder()

        # Create mask for photometry
        ph.create_mask(src, band)

        # Remove background using the mask
        ph.remove_background(src, ph.mask)

        # Set photomap info for reference star
        ## Reset photometry radius loop
        ph.radius = args.radius_ref
        if args.photmap:
          photmap = os.path.join(
            outdir, "photregion", f"{fitsID}_ref.png")
        else:
          photmap = None 

        # Do reference star photometry
        df_ref = ph.phot_catalog(src, args.refphot, band, photmap)
        assert len(df_ref)!=0, "No reference stars were detected."

        # Change to 1 liner dataframe (extract flux and fluxerr of each objects).
        df_ref = modify_ref(df_ref, ph.kwd_objID)

        
        # Obtain time and coordinates using orbit.
        ph.obtain_time_from_hdr(hdr)
        ra_obj, dec_obj = orb.calcloc(obstime=ph.t_mjd)
        x_obj, y_obj = w.all_world2pix(ra_obj, dec_obj, 0)
        x0, y0 = np.array([x_obj]), np.array([y_obj])

        # Obtain winpos (corrected position using based on its PSF)
        # (not good for non-sidereal tracked image?)
        xwin, ywin, flag = obtain_winpos(image, x0, y0, ph.radius)
        ## Use original x0, y0 when error is large (due to no detection etc.)
        xwin = np.where(flag==1, x0, xwin)
        ywin = np.where(flag==1, y0, ywin)
        # Calculate ra, dec from x, y
        rawin, decwin = w.all_pix2world(xwin, ywin, 0)

        # Reset photomap info for target object
        if args.photmap:
          photmap = os.path.join(
            outdir, "photregion", f"{fitsID}_obj.png")
        else:
          photmap = None 

        # Reset photometry radius for target object
        ph.radius = args.radius_obj

        # Do object photometry
        df_obj = ph.phot_loc(src, args.objphot, xwin, ywin, photmap)


        # Concatenate photometry results
        ## Obtained data structure
        ## x, y, ... x_ref1, y_ref1, ...
        ## 2, 8, ...   1090,   2000, ...
        df_concat = pd.concat([df_obj, df_ref], axis=1)

        # Add fits original info 
        # e.g. background, time 
        ph.add_photmetry_info(df_concat)
        
        # Save 1-band 1-frame DataFrame in predefined list
        res_1band.append(df_concat)
        print("")

    # Concatenate 1-band all frame DataFrame
    df_1band = pd.concat(res_1band)

    # Fill no data points by 0.
    df_1band = df_1band.fillna(0)
    # Save all photometry result
    out = f"photometry_result_{band}.csv"
    out = os.path.join(outdir, out)
    df_1band.to_csv(out, sep=" ", index=False)


    # Save 1-band all-frame DataFrame in list
    res_allband.append(df_1band)
  
  # Concatenate all-bands DataFrame 
  # and remove common raws (i.e. catalog magnitude)
  df_all = concat_allband(res_allband, args.bands)

  # Add common info
  # e.g. pixel scale, instrument name
  ph.add_instrumental_info(df_all)

  # Save all photometry result
  out = "photometry_result.csv"
  out = os.path.join(outdir, out)
  df_all.to_csv(out, sep=" ", index=False)

  # Save object photometry result for quicklook
  df_obj = extract_obj(df_all, args.bands)
  out = "photometry_obj.csv"
  out = os.path.join(outdir, out)
  df_obj.to_csv(out, sep=" ", index=False)

  # End time
  t1 = time.time()

  # Ouptut elapsed time
  t_total = t1 - t0
  t_frame = t_total/N_frame
  print(
    "\n\nt_elapse\n"
    f"  {t_total:.1f}s\n"
    f"  {t_frame:.1f}s (N={N_frame})")


if __name__ == "__main__":
  parser = ap(
    description="Do multi-bands data relative photometry.",
    formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument(
    "--obj", type=str, required=True,
    help="object name")
  parser.add_argument(
    "--inst", type=str, required=True, choices=["TriCCS", "murikabushi"],
    help="used instrument")
  parser.add_argument(
    "--flist", required=True, nargs="*", 
    help="fitslist of each bands")
  parser.add_argument(
    "--fitsdir", type=str, required=True,
    help='all fits directory')
  parser.add_argument(
    "--standard", type=str, required=True,
    help="standard fits list text")
  parser.add_argument(
    "--idx_standard", type=int, default=2,
    help="index of standard fits")
  parser.add_argument(
    "--bands", nargs="*", required=True,
    help="used bands")
  parser.add_argument(
    "--catalogs", nargs="*", required=True,
    help="catalog for each bands (ps, gaia, sdss, usnob)")
  parser.add_argument(
    "--radius_ref", type=int, default=15, 
    help="reference aperture radius for loc photal photometry in pixel")
  parser.add_argument(
    "--radius_obj", type=int, default=15, 
    help="object aperture radius for loc photal photometry in pixel")
  parser.add_argument(
    "--r_disk", type=int, default=15, 
    help="aperture disk radius for isophotal photometry in pixel")
  parser.add_argument(
    "--sigma", dest='sigma', type=int, default=3,
    help="extraction threshold in  object-merging process")
  parser.add_argument(
    "--epsilon", dest='epsilon', type=int, default=20,
    help='range parameter in object-merging process in pixel')
  parser.add_argument(
    "--minarea", dest='minarea', type=int, default=3,
    help='minimum area to be extracted in pixel')
  parser.add_argument(
    "--refphot",  type=str, default="app",
    help='choose loc to use app (faint object) or iso (bright)')
  parser.add_argument(
    "--objphot",  type=str, default="app",
    help='choose loc to use app (faint object) or iso (bright)')
  parser.add_argument(
    "--refmagmin", type=str, default="12.0", 
    help="minimum magnitude to be searched")
  parser.add_argument(
    "--refmagmax", type=str, default="18.0", 
    help="maximum magnitude to be searched")
  parser.add_argument(
    "--radius_mask", type=int, default=15, 
    help="mask radius in pixel")
  parser.add_argument(
    "-p", "--photmap", action='store_true',
    help='create photometry region map (a bit slow)')
  parser.add_argument(
    "--table",  type=str, default=None,
    help="table name of homemade database (see README.md)")
  parser.add_argument(
    "--dbdir",  type=str, default="~/db4movphot",
    help="database directory name")
  args = parser.parse_args()
 
  main(args)
