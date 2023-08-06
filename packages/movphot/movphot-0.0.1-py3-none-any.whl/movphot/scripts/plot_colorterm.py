#s!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plot and determine colorterm (CT) and color transfornation gradient (CTG)
and color transformation intercept (CTI).
Return CT, CTG and CTI values at last.
These values are also used in `plot_lc.py` to calculate 
target magnitudes and colors.

Definitions of CT, CTG and CTI
------------------------------
  CT :
    slope of color_cat (m_cat,1-m_cat,2) vs m_inst,1-m_cat, 1
  CTG :
    slope of color_cat (m_cat,1-m_cat,2) vs color_inst (m_inst,1-m_inst, 2)
  CTI :
    intercept of color_cat (m_cat,1-m_cat,2) vs color_inst (m_inst,1-m_inst, 2)

CT, CTG, CTI are common values during a night.
On the othre hand, magzpt is not common during a night.
So this script calculates CTG, CTI using instrumental color vs catalog color 
of comparison stars at first.
Then object color light curve are obtained using CTG and CTI.
  Equation: color_inst = (color_cat)*CTG + CTI


If you need to plot object magnitude light curves, 
this script calculates CT using 
instrumental magnitude - catalog magnitude vs catalog color
of comparison stars.
  Equation: mag_inst - mag_cat = color_cat*CT + magzpt
            magzpt = mag_inst - mag_cat - color_cat*CT

After calculating magzpt of each frame,
object magnitude can be obtained in each frame.
  Equation: mag_cat = mag_inst - color_cat*CT - magzpt
  

Summary of Procedures
---------------------
(p1, p2, ... are usefull search words.)
  p1  Read photometric csv
  p2  Obtain 3-bands common objID (XX__(objid)__XX) from DataFrame 
  p3  Calculate reference dfs to check 
  p4  Remove red comparison stars from df 
  p5  Calculate object instrumental mag 
  p6  Calculate CTG and CTI 
  p7  Calculate median magzpt and its error
  p8  Calculate object color using CTG and CTI
  p9  Calculate CT
  p10 Plot CT histogram
  p11 Remove outlier (nan,inf,larg error/eflag) after all calculateion
  p12 Calculate time in second and save for periodic analysis 
  p13 Plot object mag/color light curve
  p14 plot magzpt
  p15 Save photometric result csv
"""

import os 
import sys
from argparse import ArgumentParser as ap
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  

from myplot import mycolor, mymark, myls, myfigure, myfigure_ver

# Functions ==================================================================

def get_filename(file_path):
  return file_path.split("/")[-1].split(".")[0]


def linear_fit(x, a, b):
  """Linear fit function for scipy.optimize.
  """
  return a*x + b


def adderr(*args):
  """Calculate additional error.

  Parameters
  ----------
  args : array-like
    list of values

  Return
  ------
  err : float
    calculated error
  """
  err = np.sqrt(np.sum(np.square(args)))
  return err


def adderr_series(*args):
  """Add error of multiple pandas.Series.

  Parameters
  ----------
  args : array-like
    list of pandas.Series 

  Return
  ------
  err_s : pandas.Series
    single pandas.Series of calculated error
  """ 
  for i,x in enumerate(args):
    assert type(x) is pd.core.frame.Series, "Input should be Series."
    #assert type(x)==type(pd.Series()), "Sould be Series"
    if i==0:
      temp = x.map(np.square)
    else:
      temp += x.map(np.square)
  err_s = temp.map(np.sqrt)
  return err_s


def log10err(val, err):
  """Calculate log10 error.
  """
  return err/val/np.log(10)


def band4cterm(band, bands):
  """Return 2 bands for color term determination.
  
  Parameters
  ----------
  band : str
    band of fits
  bands : str
    3 bands

  Returns
  -------
  mag_l, mag_r : float
    used magnitude
  """

  if bands == ["g", "r", "i"]:

    #if band=="g":
    #  mag_l, mag_r = "g", "r"
    #elif band=="r":
    #  mag_l, mag_r = "g", "r"
    #elif band=="i":
    #  mag_l, mag_r = "g", "i"
    if band=="g":
      mag_l, mag_r = "g", "r"
    elif band=="r":
      mag_l, mag_r = "r", "i"
    elif band=="i":
      mag_l, mag_r = "g", "i"

  elif bands == ["g", "r", "z"]:
    if band=="g":
      mag_l, mag_r = "g", "r"
    elif band=="r":
      mag_l, mag_r = "r", "z"
    elif band=="z":
      mag_l, mag_r = "g", "z"

  return mag_l, mag_r


def calc_inst_color(df, bands, magkwd):
  """Calculate instrumental color.

  Parameters
  ----------
  df : pandas.DataFrame
    input DataFrame
  bands : list
    bands in DataFrame
  magkwd : dict
    magnitude keyword

  Return
  ------
  df : pandas.DataFrame
    instrumental magnitude calculated DataFrame
  """
  if bands == ["g", "r", "i"]:
    df["g_r"] = df[magkwd["g"]] - df[magkwd["r"]]
    df["r_i"] = df[magkwd["r"]] - df[magkwd["i"]]

  if bands == ["g", "r", "z"]:
    df["g_r"] = df[magkwd["g"]] - df[magkwd["r"]]
    df["r_z"] = df[magkwd["r"]] - df[magkwd["z"]]

  return df


def obtain_magkwd(bands):
  """Obtain magnitude keyword to calculate instrumental color.
  for only this script.
  
  Parameters
  ----------
  bands : list
    bands in DataFrame

  Return
  ------
  magkwd : dict
    magnitude keyword dictionary
  """
    
  if bands == ["g", "r", "i"]:
    magkwd = dict(g="mag_g", r="mag_r", i="mag_i")
  elif bands == ["g", "r", "z"]:
    magkwd = dict(g="mag_g", r="mag_r", z="mag_z")
  return magkwd


def add_color_reverse(df, bands):
  """Add reverse color to input DataFrame.
  If df has g_r, g_rerr, add r_g and r_gerr

  Parameter
  ---------
  df : pandas.DataFrame
    input dataframe

  Return
  ------
  df : pandas.DataFrame
    output dataframe
  """
  col = df.columns.tolist()
  N = len(bands)
  for i in range(N):
    idx_band1 = i%N
    idx_band2 = (i+1)%N
    band1 = bands[idx_band1]
    band2 = bands[idx_band2]
    print(f"{band1}, {band2}")
    try:
      df[f"{band1}_{band2}"] = -df[f"{band2}_{band1}"]
      df[f"{band1}_{band2}err"] = df[f"{band2}_{band1}err"]
    except:
      pass
    try:
      df[f"{band2}_{band1}"] = -df[f"{band1}_{band2}"]
      df[f"{band2}_{band1}err"] = df[f"{band1}_{band2}err"]
    except:
      pass
  return df


# Functions finish ============================================================


if __name__ == "__main__":
  parser = ap(description="Colorterm determination")
  parser.add_argument(
    "csv", type=str, help="photres.csv")
  parser.add_argument(
    "obj", type=str, help="object name")
  parser.add_argument(
    "magtype", type=str, choices=["SDSS", "PS"],
    help="griz magnitude type of input csv")
  parser.add_argument(
    "--magmin", type=float, default=12,
    help="minimum magnitude")
  parser.add_argument(
    "--magmax", type=float, default=20,
    help="maximum magnitude")
  parser.add_argument(
    "--gr_th", type=float, default=1.5, 
    help="maximum g_r value for comparison stars")
  parser.add_argument(
    "--err_th", type=float, default=1, 
    help="maximum magnitude error value for both object and comparison stars")
  parser.add_argument(
    "--eflag_th", type=float, default=1, 
    help="maximum eflag value for both object and comparison stars")
  parser.add_argument(
    "--bands", nargs=3, default=["g", "r", "i"],
    help="3 bands")
  parser.add_argument(
    "--rawmagrange", nargs=2, type=float, default=None, 
    help="raw mag range")
  parser.add_argument(
    "--rawcolrange", nargs=2, type=float, default=None, 
    help="raw color range")
  args = parser.parse_args()


  # Set output directory
  outdir = "plot"
  if not os.path.isdir(outdir):
    os.makedirs(outdir)

  # Selection criteria
  err_th = args.err_th
  eflag_th = args.eflag_th
  gr_th = args.gr_th
  magmin, magmax = args.magmin, args.magmax

  # Determine color
  bands = args.bands
  if (bands[2]=="i") or (bands[2]=="I"):
    colors = ["green", "red", "magenta"]
  elif bands[2]=="z":
    colors = ["green", "red", "blueviolet"]

 

  # p1 Read photometric csv ==================================================
  filename = get_filename(args.csv)
  df = pd.read_csv(args.csv, sep=" ")
  print(f"DataFrame Dimention (original) {len(df)}")
  N_nan = np.sum(df.isnull().sum())
  # Do not remove 'nan' here.
  # Some 'nan' arise from nonsiderial tracking 
  print(f"N_nan={N_nan}")
  print(f"DataFrame Dimention (original) {len(df)}")
  N_nan = np.sum(df.isnull().sum())
  # Do not remove 'nan' here.
  # Some 'nan' arise from nonsiderial tracking 
  print(f"N_nan={N_nan}")
  # Read photometric csv ======================================================


  # p2 Obtain 3-bands common objID (XX__(objid)__XX) from DataFrame ===========
  # 18 is length of objID for Pan-STARRS catalog
  column = df.columns.tolist()
  print(f"{len(column)}")
  # list of objID for each bands
  objID_bands = []
  for band in bands:
    col_ref = [col for col in column if (len(col))>18]
    col_band = [col for col in column if (len(col))>18 and f"_{band}" in col]
    objID_band = [col.split("_")[1] for col in col_band]
    objID_band = list(set(objID_band))
    #print(f"objID {band} N={len(objID_band)}")
    objID_bands.append(objID_band)
  # Common objID 
  objID = set(objID_bands[0]) & set(objID_bands[1]) & set(objID_bands[2]) 
  print(f"Final common {len(objID)}")
  # Obtain reference dataframe and objID finish ================================


  # p3 Calculate reference dfs to check =======================================
  # Fill non-data by 0
  #   dfs = [df_obj1, df_obj2, ...]
  #   df_obj1 = [mag_g_inst, magerr_g_inst, mag_g, magerr_g, ...]
  dfs = []
  # Use three band common objID
  for obj in objID:
    res_band = []
    for band in bands:
      band_l, band_r = band4cterm(band, bands)

      # Search 1-band ref star
      col_ref = [col for col in column if (len(col)>18) and f"_{band}" in col]
      col_ref = [col for col in col_ref if obj in col]
      df_1band = df[col_ref]

      # flux 
      flux = df_1band[f"flux_{obj}_{band}"]
      fluxerr = df_1band[f"fluxerr_{obj}_{band}"]
      # instrumental mag
      maginst = -2.5*np.log10(flux)
      maginsterr = 2.5*log10err(flux, fluxerr)
      # catatlog mag
      magcat = df_1band[f"{band}MeanPSFMag_{obj}_{band}"]
      magcaterr = df_1band[f"{band}MeanPSFMagErr_{obj}_{band}"]

      d = {
        f"mag_{band}_inst":maginst,
        f"magerr_{band}_inst":maginsterr,
        f"mag_{band}_cat":magcat,
        f"magerr_{band}_cat":magcaterr,
      }
      df_obj_band = pd.DataFrame(d.values(), index=d.keys()).T
      # Fill outliers by 0
      df_obj_band = df_obj_band.replace([np.inf, -np.inf], np.nan)
      df_obj_band = df_obj_band.fillna(0)
      res_band.append(df_obj_band)

    df_obj = pd.concat(res_band, axis=1)
    df_obj["obj"] = obj
    dfs.append(df_obj)
  # Calculate each reference instrumental magnitude finish =====================


  # p4 Remove red comparison stars from df ====================================
  # Use gr here (the same threshold with Kokotanekova+2017)
  gr_th = args.gr_th
  col_all = df.columns.tolist()
  for obj in objID:
    df_red = df[
      (df[f"gMeanPSFMag_{obj}_g"]-df[f"rMeanPSFMag_{obj}_g"]) > gr_th]
    if len(df_red)!=0:
      # Remove red object
      print(f"Remove red object : {obj}")
      col_red = [col for col in col_all if obj in col]
      df = df.drop(col_red, axis=1)

  # Remove red comparison stars from df finish ================================


  # p5 Calculate object instrumental mag ======================================
  for band in bands:
    # 1. instrumental magnitude
    s_maginst = -2.5*np.log10(df[f"flux_{band}"])
    s_maginsterr = 2.5*log10err(
      df[f"flux_{band}"], df[f"fluxerr_{band}"])
    df.insert(0, f"mag_{band}_inst", s_maginst)
    df.insert(0, f"magerr_{band}_inst", s_maginsterr) 
  # Calculate object instrumental and median mag finish =======================


  # p6 Calculate CTG and CTI ==================================================
  res = []
  for idx,band in enumerate(bands):
    color = mycolor[idx]
    mark = mymark[idx]
    fig, ax1, ax2 = myfigure(n=2)
    band_l, band_r = band4cterm(band, bands)
    print(f"{band}, {band_l}, {band_r}")
     
    # For all objects fitting to estimate CTG and CTI
    col_cat_list, col_cat_err_list = [], []
    col_inst_mean_list, col_inst_meanerr_list = [], []

    # Loop for object (each df_ref has ideally N_frame)
    for idx_obj, df_ref in enumerate(dfs):
      N0 = len(df_ref)
      # Remove 0 data
      df_ref = df_ref[df_ref[f"mag_{band}_inst"]!=0]
      df_ref = df_ref[df_ref[f"mag_{band_l}_inst"]!=0]
      df_ref = df_ref[df_ref[f"mag_{band_r}_inst"]!=0]
      df_ref = df_ref[df_ref[f"magerr_{band}_inst"]!=0]
      N1 = len(df_ref)
      # Remove large error
      df_ref = df_ref[df_ref[f"magerr_{band}_inst"] < err_th]
      df_ref = df_ref[df_ref[f"magerr_{band_l}_inst"] < err_th]
      df_ref = df_ref[df_ref[f"magerr_{band_r}_inst"] < err_th]
      N2 = len(df_ref)
      # Remove faint obj
      df_ref = df_ref[df_ref[f"mag_{band}_cat"] < magmax]
      N3 = len(df_ref)
      #print(
      #  f"df_ref {idx_obj} N0={N0}(original),"
      #  f"N1={N1}(remove 0 data), N2={N2}(remove large error)"
      #/)
      
      if len(df_ref)==0:
        continue
      if idx_obj == 0:
        label = f"N_frame={len(df_ref)}, N_obj={len(dfs)}"
      else:
        label=None
      
      # Instrumental color
      col_inst = df_ref[f"mag_{band_l}_inst"] - df_ref[f"mag_{band_r}_inst"]
      col_inst_err = adderr_series(
      df_ref[f"magerr_{band_l}_inst"] - df_ref[f"magerr_{band_r}_inst"])

      # Catalog color
      col_cat = df_ref[f"mag_{band_l}_cat"] - df_ref[f"mag_{band_r}_cat"]
      col_cat_err = adderr_series(
      df_ref[f"magerr_{band_l}_cat"] - df_ref[f"magerr_{band_r}_cat"])

      # Plot 
      ## All col_col
      ax1.errorbar(
        col_cat, col_inst, xerr=col_cat_err, yerr=col_inst_err,
        fmt="o", linewidth=0.5, color=color, marker=mark, label=label)

      
      # Ideally std is small since col_inst is not affected by atmo. variation
      col_inst_mean, col_inst_std = np.mean(col_inst), np.std(col_inst)
      print(f"{idx_obj:3d} {col_inst_mean}, {col_inst_std}")

      col_inst_mean_list.append(col_inst_mean)
      # Consider color error and standard deviation/sqrt(n) ??
      err = adderr(adderr(col_inst_err)/N2, col_inst_std/np.sqrt(N3))
      # Consider color error and standard deviation ??
      err = adderr(adderr(col_inst_err)/N2, col_inst_std/np.sqrt(N3))
      col_inst_meanerr_list.append(err)

      col_cat_list.append(np.mean(col_cat))
      col_cat_err_list.append(np.mean(col_cat_err))


    # col_inst_err_list, col_cat_err_list
    # Fitting color_inst = color_cat*CTG + CTI
    # Using mean value of all objects
    cmin, cmax = np.min(col_cat_list), np.max(col_cat_list)
    x_fit = np.arange(cmin, cmax, 0.1)

    # Raw fit
    params_r, _ = curve_fit(linear_fit, col_cat_list, col_inst_mean_list)
    CTG_r, CTI_r = params_r[0], params_r[1]

    # Weighted fit (bad?)
    params_w, _ = curve_fit(
      linear_fit, col_cat_list, col_inst_mean_list, sigma=col_inst_meanerr_list,
      absolute_sigma=True)
    CTG_w, CTI_w = params_w[0], params_w[1]
    print(f"col_inst_meanerr_list: {col_inst_meanerr_list}")
    
    # Add to the obj DataFrame
    # Fix error calculation!!
    # Use CTG_r !!
    CTG_list = [CTG_r]*len(df)
    CTGerr_list = [0]*len(df)
    CTI_list = [CTI_r]*len(df)
    CTIerr_list = [0]*len(df)
    s_CTG = pd.Series(CTG_list, name="CTG")
    s_CTI = pd.Series(CTI_list, name="CTI")
    s_CTGerr = pd.Series(CTGerr_list, name="CTG")
    s_CTIerr = pd.Series(CTIerr_list, name="CTI")
    # Do not insert when already exists
    try:
      df.insert(0, f"{band_l}_{band_r}_CTG", s_CTG)
      df.insert(0, f"{band_l}_{band_r}_CTGerr", s_CTGerr)
      df.insert(0, f"{band_l}_{band_r}_CTI", s_CTI)
      df.insert(0, f"{band_l}_{band_r}_CTIerr", s_CTIerr)
    except:
      pass

    print(f"Raw fit      {band_l}-{band_r} {CTG_r}, {CTI_r}")
    print(f"Weighted fit {band_l}-{band_r} {CTG_w}, {CTI_w}")


    # Plot (Continued)
    ## Mean values
    xmin, xmax = ax1.get_xlim()
    ymin, ymax = ax1.get_ylim()
    #ax2.set_xlim([xmin, xmax])
    #ax2.set_ylim([ymin, ymax])
    x = np.arange(xmin, xmax, 0.01)
    ax2.errorbar(
      col_cat_list, col_inst_mean_list, xerr=col_cat_err_list, 
      yerr=col_inst_meanerr_list, fmt="o", color="red",
      label=f"stacked mean values")

    ## Fitting curve
    ax2.plot(
      x, CTG_r*x+CTI_r, marker="", lw=3, ls=myls[1], color=mycolor[0],
      label=f"Raw y={CTG_r:.2f}x + {CTI_r:.2f}")
    ax2.plot(
      x, CTG_w*x+CTI_w, marker="", lw=3, ls=myls[2], color=mycolor[1],
      label=f"Weighted y={CTG_w:.2f}x + {CTI_w:.2f}" 
      )


    col_cat_label = "$m_{cat," + band_l + "} - m_{cat," + band_r + "}$"
    col_inst_label = "$m_{inst," + band_l + "} - m_{inst," + band_r + "}$"

    ax1.set_xlabel(col_cat_label)
    ax1.set_ylabel(col_inst_label)
    ax2.set_xlabel(col_cat_label)
    ax2.set_ylabel(col_inst_label)
    xmin, xmax = ax1.get_xlim()
    ax2.set_xlim([xmin, xmax])
    ax1.legend(fontsize=10)
    ax2.legend(fontsize=10)
    out =  f"colorterm{args.obj}_{band}band_{band_l}_{band_r}_CTG.png"
    out = os.path.join(outdir, out)
    plt.savefig(out, dpi=100)
    plt.close()
  # Calculate CTG and CTI finish ==============================================


  # p7 Calculate median magzpt and its error ==================================
  # Save magzpt (magzpt_g and magzpterr_g etc.) 
  # Save magzpt corrected mag (magzpt_g_median and magzpterr_g_median etc.) 
  # Save colorterm corrected mag (magzpt_g_ccor and magzpterr_g_ccor etc.) 
  #   First, determine CT by fitting of comparison stars for each frame.
  #     mag_inst - mag_cat = color_cat*CT + magzpt
  #     <-> mag_diff = col_cat*CT + magzpt
  #   Then, magzpt can be calculated for each frame.
  #     magzpt = mag_inst - mag_cat - color_cat*CT
  for band in bands:
    magzpt_list, magzpterr_list = [], []
    CT_list, CTerr_list = [], []
    for n in range(len(df)):
      magzpt_list_frame, magzpterr_list_frame = [], []
      mag_diff_list, col_cat_list = [], []
      mag_diff_err_list, col_cat_err_list = [], []
      # Use n-th frame dataframe
      df_n = df.loc[n:n]
      col_n = df_n.columns.tolist()
      # Band unique column
      col_band = [
        col for col in col_n if (len(col)>18) and f"_{band}" in col]
      # Mag column in band unique column
      col_catmag = [
        col for col in col_band if f"{band}Mean" in col and f"Err" not in col]
      # MagErr column in band unique column
      col_catmagerr = [
        col for col in col_band if f"{band}Mean" in col and f"Err" in col]
      # Flux column in band unique column
      col_flux = [
        col for col in col_band if  f"flux_" in col]
      # Fluxerr column in band unique column
      col_fluxerr = [
        col for col in col_band if  f"fluxerr_" in col]
      # eflag (error flag when photometry) column in band unique column
      col_eflag = [
        col for col in col_band if  f"eflag_" in col]

      # mag, flux and eflag DataFrame of the frame
      ## each n-th frame dataframe (df_n) has only x (object number) columns
      df_flux = df_n[col_flux]
      df_fluxerr = df_n[col_fluxerr]
      df_catmag = df_n[col_catmag]
      df_catmagerr = df_n[col_catmagerr]
      df_eflag = df_n[col_eflag]


      # Concatenate magnitude and flux in all frames
      for (_, mag), (_, magerr), (_, flux), (_, fluxerr), (_, eflag)in zip(
        df_catmag.iteritems(), df_catmagerr.iteritems(),
        df_flux.iteritems(), df_fluxerr.iteritems(), df_eflag.iteritems()):

        mag = mag.values[0]
        magerr = magerr.values[0]
        flux = flux.values[0]
        fluxerr = fluxerr.values[0]
        eflag = eflag.values[0]
        # print(f"mag, magerr, flux, fluxerr, eflag = {mag},{magerr},{flux},{fluxerr},{elag}")
        # Skip bad data
        if (flux > 0) and (magmin < mag < magmax) and (eflag < eflag_th):
          magzpt = mag + 2.5*np.log10(flux)
          magzpt_list_frame.append(magzpt)

          maginsterr = 2.5*log10err(flux, fluxerr)
          magzpterr = adderr(magerr, maginsterr)
          magzpterr_list_frame.append(magzpterr)


      magzpt_median_frame = np.median(magzpt_list_frame) 
      N = len(magzpt_list_frame)
      # Consider photometric error (magzpterr_list_frame)
      # and standard deviation (magzpt_std_frame)
      magzpt_std_frame = np.std(magzpt_list_frame)
      # which ?
      err = adderr(adderr(magzpterr_list_frame)/N, magzpt_std_frame)
      err = adderr(adderr(magzpterr_list_frame)/N, magzpt_std_frame/np.sqrt(N))
      magzpterr_median_frame = err

      #print(
      #  f"median magzpt of {n}-th frame\n"
      #  f" ({magzpt_median_frame}+-{magzpterr_median_frame}, "
      #  f"N={len(magzpt_list_frame)})"
      #)

      # Save in magzpt list
      magzpt_list.append(magzpt_median_frame)
      magzpterr_list.append(magzpterr_median_frame)

    
    # Insert magzpt, magzpterr list
    df.insert(0, f"magzpt_{band}", magzpt_list)
    df.insert(0, f"magzpterr_{band}", magzpterr_list)

    # 2. median magzpt corrected magnitude
    s_mag = df[f"magzpt_{band}"] - 2.5*np.log10(df[f"flux_{band}"])
    s_magerr = adderr_series(
      s_maginsterr, df[f"magzpterr_{band}"])
    df.insert(0, f"mag_{band}_median", s_mag)
    df.insert(0, f"magerr_{band}_median", s_magerr) 
  # Calculate median magzpt and its error finish ==============================


  # p8 Calculate object color using CTG and CTI ===============================
  # 1. instrumental color 
  #    ex) g_r_inst, g_rerr_inst
  #     2. median magzpt corrected color (i.e. do not consider colortemp)
  #        ex) g_r_median, g_rerr_median
  # 3. CTG, CTI corrected color 
  #    from color_inst = color_cat*CTG + CTI
  #    color_cat = (color_inst - CTI)/CTG
  #    ex) g_r_ccor, g_rerr_ccor
  for band in bands:
    band_l, band_r = band4cterm(band, bands)

    # 1. instrumental color
    s_color_r = df[f"mag_{band_l}_inst"] - df[f"mag_{band_r}_inst"]
    s_colorerr_r = adderr_series(
      df[f"magerr_{band_l}_inst"], df[f"magerr_{band_r}_inst"])
    # Do not insert when already exists
    try:
      df.insert(0, f"{band_l}_{band_r}_inst", s_color_r)
      df.insert(0, f"{band_l}_{band_r}err_inst", s_colorerr_r) 
    except:
      pass

    # 2. median magzpt corrected color (i.e. do not consider color term)
    s_color = df[f"mag_{band_l}_median"] - df[f"mag_{band_r}_median"]
    s_colorerr = adderr_series(
      df[f"magerr_{band_l}_median"], df[f"magerr_{band_r}_median"])
    # Do not insert when already exists
    try:
      df.insert(0, f"{band_l}_{band_r}_median", s_color)
      df.insert(0, f"{band_l}_{band_r}err_median", s_colorerr) 
    except:
      pass

    # 3. CTG, CTI corrected color
    # color_inst = color_cat*CTG + CTI
    #    color_inst = color_cat*CTG + CTI
    #    color_cat = (color_inst - CTI)/CTG
    s_color_c = (
      (df[f"mag_{band_l}_inst"] - df[f"mag_{band_r}_inst"]
      - df[f"{band_l}_{band_r}_CTI"])/df[f"{band_l}_{band_r}_CTG"]
      )
    # Consider error of color_raw, CTG and CTI
    s_colorerr_c = adderr_series(
      s_colorerr_r, df[f"{band_l}_{band_r}_CTGerr"], 
      df[f"{band_l}_{band_r}_CTIerr"])
    # Do not insert when already exists
    try:
      df.insert(0, f"{band_l}_{band_r}_ccor", s_color_c)
      df.insert(0, f"{band_l}_{band_r}err_ccor", s_colorerr_c) 
    except:
      pass
  ## Calculate object color using CTG and CTI finish ==========================


  # p9 Calculate CT ===========================================================
  for band in bands:
    CT_list, CTerr_list = [], []
    for n in range(len(df)):
      mag_diff_list, mag_differr_list = [], []
      col_cat_list, col_caterr_list = [], []
      # Use n-th frame dataframe
      df_n = df.loc[n:n]
      col_n = df_n.columns.tolist()
      # Use
      # flux, mag_cat, mag_cat_l, mag_cat_r and their errors
      # and eflag
 
      # Band unique column
      col_band = [
        col for col in col_n if (len(col)>18) and f"_{band}" in col]
      # Mag column in band unique column
      col_catmag = [
        col for col in col_band if f"{band}Mean" in col and f"Err" not in col]
      # left Mag column in band unique column
      col_catmag_l = [
        col for col in col_band if f"{band_l}Mean" in col and f"Err" not in col]
      # right Mag column in band unique column
      col_catmag_r = [
        col for col in col_band if f"{band_r}Mean" in col and f"Err" not in col]
      # MagErr column in band unique column
      col_catmagerr = [
        col for col in col_band if f"{band}Mean" in col and f"Err" in col]
      # left MagErr column in band unique column
      col_catmagerr_l = [
        col for col in col_band if f"{band_l}Mean" in col and f"Err" in col]
      # right MagErr column in band unique column
      col_catmagerr_r = [
        col for col in col_band if f"{band_r}Mean" in col and f"Err" in col]
      # Flux column in band unique column
      col_flux = [
        col for col in col_band if  f"flux_" in col]
      # Fluxerr column in band unique column
      col_fluxerr = [
        col for col in col_band if  f"fluxerr_" in col]
      # eflag (error flag when photometry) column in band unique column
      col_eflag = [
        col for col in col_band if  f"eflag_" in col]

      # mag, flux and eflag DataFrame of the frame
      ## each n-th frame dataframe (df_n) has only x (object number) columns
      df_flux = df_n[col_flux]
      df_fluxerr = df_n[col_fluxerr]
      df_catmag = df_n[col_catmag]
      df_catmagerr = df_n[col_catmagerr]
      df_catmag_l = df_n[col_catmag_l]
      df_catmagerr_l = df_n[col_catmagerr_l]
      df_catmag_r = df_n[col_catmag_r]
      df_catmagerr_r = df_n[col_catmagerr_r]
      df_eflag = df_n[col_eflag]

      # Concatenate magnitude and flux in all frames
      for ((_, mag), (_, magerr), (_, mag_l), (_, magerr_l), 
        (_, mag_r), (_, magerr_r), (_, flux), (_, fluxerr), (_, eflag)) in zip(
        df_catmag.iteritems(), df_catmagerr.iteritems(),
        df_catmag_l.iteritems(), df_catmagerr_l.iteritems(),
        df_catmag_r.iteritems(), df_catmagerr_r.iteritems(),
        df_flux.iteritems(), df_fluxerr.iteritems(), df_eflag.iteritems()):

        mag = mag.values[0]
        magerr = magerr.values[0]
        mag_l = mag_l.values[0]
        magerr_l = magerr_l.values[0]
        mag_r = mag_r.values[0]
        magerr_r = magerr_r.values[0]
        flux = flux.values[0]
        fluxerr = fluxerr.values[0]
        eflag = eflag.values[0]

        #print(
        #  f"mag, magerr, mag_l, magerr_l, mag_r, magerr_r, flux, fluxerr, eflag"
        #  f"\n = {mag},{magerr},{mag_l},{magerr_l},{mag_r},{magerr_r},"
        #  f"{flux},{fluxerr},{eflag}")

        # Skip bad data
        if (flux > 0) and (magmin < mag < magmax) and (eflag < eflag_th):

          magzpt = mag + 2.5*np.log10(flux)
          magzpt_list_frame.append(magzpt)
          maginsterr = 2.5*log10err(flux, fluxerr)
          magzpterr = adderr(magerr, maginsterr)
          magzpterr_list_frame.append(magzpterr)

          # mag_diff (mag_inst - mag_cat)
          mag_inst = -2.5*np.log10(flux)
          mag_insterr = 2.5*log10err(flux, fluxerr)
          mag_diff = mag_inst - mag
          mag_differr = adderr(mag_insterr, magerr)
          mag_diff_list.append(mag_diff)
          mag_differr_list.append(mag_differr)

          # col_cat (mag_l - mag_r)
          col_cat = mag_l - mag_r
          col_caterr = adderr(magerr_l, magerr_r)
          col_cat_list.append(col_cat)
          col_caterr_list.append(col_caterr)

      # Fit and obtain CT for each frame
      # Weighted fit
      params_w, _ = curve_fit(
        linear_fit, col_cat_list, mag_diff_list, sigma=mag_differr_list)
      # Do not use magzpt
      CT_frame, _ = params_w[0], params_w[1]
      CTerr_frame = 0

      #Save in CT list 
      CT_list.append(CT_frame)
      CTerr_list.append(CTerr_frame)


    # Add to the obj band DataFrame
    # Fix error calculation!!
    s_CT = pd.Series(CT_list, name="CT")
    s_CTerr = pd.Series(CTerr_list, name="CTerr")
    # Do not insert when already exists
    try:
      df.insert(0, f"{band}_CT", s_CT)
      df.insert(0, f"{band}_CTerr", s_CTerr)
    except:
      pass

  # Calculate CT finish =======================================================


  # p10 Plot CT histogram =====================================================
  for idx,band in enumerate(bands):
    color = mycolor[idx]
    mark = mymark[idx]
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.hist(df[f"{band}_CT"], bins=100, label=f"{band}")
    ax.set_xlabel("Color temp (slope)")
    ax.set_ylabel("N frame")
    out = f"{band}_CT_hist.png"
    out = os.path.join(outdir, out)
    plt.savefig(out)
  # Plot CT finish ============================================================


  # p11 Remove outlier (nan,inf,larg error/eflag) after all calculateion ======
  # Convert inf to nan
  df = df.replace([np.inf, -np.inf], np.nan)
  # Drop nan 
  df = df.dropna(how="any", axis=0)
  N_nan = np.sum(df.isnull().sum())
  assert N_nan==0, f"Nan N={N_nan}"
  # Drop by magnitude error and eflag
  N_bef = len(df)
  for band in bands:
    band_l, band_r = band4cterm(band, bands)
    df = df[df[f"magerr_{band}_inst"] < err_th]
    df = df[df[f"magerr_{band}_median"] < err_th]
    df = df[df[f"eflag_{band}"] < eflag_th]
  df = df.reset_index(drop=True)
  N_aft = len(df)
  N_rm = N_bef -N_aft 
  print(f"Final dataframe {N_aft} ({N_rm} by eflag)")
  # Check
  N_nan = np.sum(df.isnull().sum())
  assert N_nan==0, f"Nan N={N_nan}"
  ## Remove outlier finish ====================================================


  # p12 Calculate time in second and save for periodic analysis ===============
  for band in bands:
    df[f"t_sec_{band}"] = df[f"t_mjd_{band}"]*24*3600.
    df[f"t_sec_{band}"] -= df.at[0, f"t_sec_{band}"]

    df_temp = df[[f"t_sec_{band}", f"mag_{band}_median", f"magerr_{band}_median"]]
    df_temp = df_temp.rename(
      columns={f't_sec_{band}':'t_second', f"mag_{band}_median": "mag", 
         f"magerr_{band}_median": "magerr"})
    df_temp.to_csv(f"{band}_mag_{args.obj}.csv", sep=" ", index=False)
  # Calculate time in second and save for periodic analysis finish ============


  # p13 Plot object mag/color light curve =====================================
  # ax1, 3, (5) magnitude (inst, median_magzpt_corrected, CT corrected)
  # ax2, 4, 6     color (inst, median_magzpt_corrected, CTG corrected)
  fig, ax1, ax2, ax3, ax4, ax5, ax6 = myfigure_ver(n=6)
  ax1.set_title("Raw (instrumental)")
  ax3.set_title("Median corrected")
  ax5.set_title("CT/CTG corrected")

  ax1.set_ylabel("magnitude [mag]")
  ax3.set_ylabel("magnitude [mag]")
  ax5.set_ylabel("magnitude [mag]")
  ax2.set_ylabel("color [mag]")
  ax4.set_ylabel("color [mag]")
  ax6.set_ylabel("color [mag]")

  for idx,ax in enumerate(fig.axes):
    ax.invert_yaxis()
    ax.set_xlabel("Elapsed time [s]")
  
  for idx,band in enumerate(bands):
    band_l, band_r = band4cterm(band, bands)
    print(f"{band}, {band_l}, {band_r}")
    mark = mymark[idx]

    # 1. instrumental
    ## magnitude
    ax1.errorbar(
      df[f"t_sec_{band}"], df[f"mag_{band}_inst"], df[f"magerr_{band}_inst"], 
      fmt="o", ms=10, lw=1, marker=mark, label=f"{band}")
    ## color
    c_mean = np.mean(df[f"{band_l}_{band_r}_inst"])
    c_std = np.std(df[f"{band_l}_{band_r}_inst"])
    label_inst = f"{band_l}-{band_r} = {c_mean:.2f}+-{c_std:.2f}"
    ax2.errorbar(
      df[f"t_sec_{band}"], df[f"{band_l}_{band_r}_inst"], 
      df[f"{band_l}_{band_r}err_inst"], label=label_inst,
      ms=10, lw=1, fmt="o", marker=mark)

    # 2. median magzpt corrected
    ## magnitude
    ax3.errorbar(
      df[f"t_sec_{band}"], df[f"mag_{band}_median"], 
      df[f"magerr_{band}_median"], fmt="o", ms=10, lw=1, marker=mark,
      label=f"{band}")
    ## color
    c_mean = np.mean(df[f"{band_l}_{band_r}_median"])
    c_std = np.std(df[f"{band_l}_{band_r}_median"])
    label_median = f"{band_l}-{band_r} = {c_mean:.2f}+-{c_std:.2f}"
    ax4.errorbar(
      df[f"t_sec_{band}"], df[f"{band_l}_{band_r}_median"], 
      df[f"{band_l}_{band_r}err_median"], label=label_median,
      ms=10, lw=1, fmt="o", marker=mark)

    # 3. cterm corrected
    ## magnitude
    ## color

    # std ??
    c_mean = np.mean(df[f"{band_l}_{band_r}_ccor"])
    c_std = np.std(df[f"{band_l}_{band_r}_ccor"])
    label_ccor = f"{band_l}-{band_r} = {c_mean:.2f}+-{c_std:.2f}"
    ax6.errorbar(
      df[f"t_sec_{band}"], df[f"{band_l}_{band_r}_ccor"], 
      df[f"{band_l}_{band_r}err_ccor"], label=label_ccor,
      ms=10, lw=1, fmt="o", marker=mark)

  for ax in fig.axes:
    ax.legend()

  out = f"objlc_{args.obj}.png"
  out = os.path.join(outdir, out)
  fig.savefig(out, dpi=200)
  # Plot object mag/color light curve finish ==================================
  

  # p14 plot magzpt ===========================================================
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.invert_yaxis()
  ax.set_xlabel("Elapsed time [s]")
  ax.set_xlabel("MJD")
  ax.set_ylabel("magzpt [mag]")
  for band in bands:
    ax.errorbar(
      df[f"t_sec_{band}"], df[f"magzpt_{band}"], df[f"magzpterr_{band}"], 
      label=f"{band} magzpt", ms=2, fmt="o")
  ax.legend()
  out = f"magzptlc_{args.obj}.png"
  out = os.path.join(outdir, out)
  fig.savefig(out, dpi=200)
  # plot magzpt finish =========================================================


  # p15 Save photometric result csv ===========================================
  # Save neo magnitude in SDSS system
  # Convert to SDSS
  key_sdss = {
    "g":"mag_g", "gerr":"magerr_g", 
    "r":"mag_g", "rerr":"magerr_r", 
    "i":"mag_g", "ierr":"magerr_i", 
    "z":"mag_g", "zerr":"magerr_z", 
    }
  from Tonry2012 import PS2SDSS
  df = PS2SDSS(df, key0=key_sdss)
  df = df.rename(
    columns={"neomag_g":"g_temp", "neomagerr_g":"gerr_temp", 
             "neomag_r":"r_temp", "neomagerr_r":"rerr_temp", 
             "neomag_i":"i_temp", "neomagerr_i":"ierr_temp", 
             "neomag_z":"z_temp", "neomagerr_z":"zerr_temp"})
  df = df.rename(
    columns={"g_SDSS":"mag_g", "gerr_SDSS":"magerr_g", 
             "r_SDSS":"mag_r", "rerr_SDSS":"magerr_r", 
             "i_SDSS":"mag_i", "ierr_SDSS":"magerr_i", 
             "z_SDSS":"mag_z", "zerr_SDSS":"magerr_z"})

  col_out = []
  for band in bands:
    band_l, band_r = band4cterm(band, bands)
    print(f"{band}, {band_l}, {band_r}")
    # Rename g_r_median, g_rerr_median to g_r, g_rerr etc
    df = df.rename(columns={f"{band_l}_{band_r}": f"{band_l}_{band_r}", 
        f"{band_l}_{band_r}err": f"{band_l}_{band_r}err"})
    col_out.append(f"{band_l}_{band_r}")
    col_out.append(f"{band_l}_{band_r}err")


  # Save in Pan-STARRS system
  # Final used colors are CTG, CTI corrected ones (g_r_ccor etc.)
  # Original df (g,r,i) has : 
  #  r_ierr_ccor', 'r_i_ccor', 'g_rerr_ccor', 'g_r_ccor'
  # Rename g_r_ccor to g_r
  # Use column in output csv
  col_use = []
  for band in bands:
    band_l, band_r = band4cterm(band, bands)
    try:
      df = df.rename(
        columns={f"{band_l}_{band_r}_ccor": f"{band_l}_{band_r}",
        f"{band_l}_{band_r}err_ccor": f"{band_l}_{band_r}err"})
      col_use.append(f"{band_l}_{band_r}")
      col_use.append(f"{band_r}_{band_l}")
      col_use.append(f"{band_l}_{band_r}err")
      col_use.append(f"{band_r}_{band_l}err")
    except:
      pass

  # Add reverse color
  df = add_color_reverse(df, bands)
  
  df = df[col_use]
  df["obj"] = args.obj
  df["g_g"] = 0.
  df["g_gerr"] = 0.

  bands = "".join(bands)
  out = f"{args.obj}_magall_{bands}.csv"
  df.to_csv(out, sep=" ", index=False)
  # Save photometric result csv finish  ======================================== 


