#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Common functions for movinv object photometry.
  (error calculation, DataFrame handling, object orbit prediction etc.)
"""
import os
import datetime
from functools import wraps
import time
import pandas as pd
from scipy import interpolate
from scipy.spatial import KDTree
import astropy.io.fits as fits
from astropy.time import Time
from astropy.wcs import WCS as wcs
import numpy as np


def nowstr():
  """Return time in string.
  """
  now = datetime.datetime.now()
  now = datetime.datetime.strftime(now, "%Y%m%dT%H%M%S")
  return now


def adderr(*args):
  """Calculate error
  """
  return np.sqrt(np.sum(np.square(args)))


def log10err(val, err):
  return err/val/np.log(10)


def adderr_series(*args):
  """
  Input : pandas.Series 
  Return : pandas.Series
  """ 
  for i,x in enumerate(args):
    assert type(x)==type(pd.Series()), "Input type should be Series"
    if i==0:
      temp = x.map(np.square)
    else:
      temp += x.map(np.square)
  err_s = temp.map(np.sqrt)
  return err_s


def get_filename(file_path):
  return file_path.split("/")[-1].split(".")[0]


def calc_xy(df, w, kwd_ra="raMean", kwd_dec="decMean"):
  """Calculate pixel x and y from ra and dec.

  Parameters
  ----------
  df : pandas.DataFrame
    input DataFrame which should have ra and dec
  w : astropy.wcs.WCS
    wcs information
  kwd_ra, kwd_dec : str, optional
    keyword of ra, dec in input df (optimaized for PS catalog)

  Return
  ------
  df : pandas.DataFrame
    output DataFrame which have x and y
  """

  x_list, y_list = [], []
  for idx, row in df.iterrows():
    x, y  = w.all_world2pix(row[kwd_ra], row[kwd_dec], 0)
    x_list.append(x)
    y_list.append(y)
  df_coo = pd.DataFrame(dict(x=x_list, y=y_list), dtype=float)
  df_con = pd.concat([df, df_coo], axis=1)
  return df_con


def calc_radec(df, w):
  """Calculate ra and dec using wcs information.

  Parameters
  ----------
  df : pandas.DataFrame
    input DataFrame which should have x and y
  w : astropy.wcs.WCS
    wcs information

  Return
  ------
  df : pandas.DataFrame
    output DataFrame which have ra and dec
  """
  ra_list, dec_list = [], []
  for idx, row in df.iterrows():
    cra, cdec  = w.all_pix2world(row["x"], row["y"], 0)
    ra_list.append(cra)
    dec_list.append(cdec)
  
  df["ra"] = ra_list
  df["dec"] = dec_list
  return df
 
def remove_edge(df, radius, nx, ny):
  """Remove objects close to edge.

  Parameters
  ----------
  df : pandas.DataFrame
    input DataFrame which contains x, y
  radius : float
    removal threshold in pixel
  nx, ny : int
    number of pixels

  Return
  ------
  df : pandas.DataFrame
    close objects removed DataFrame
  """

  # Remove objects in edge region.
  df = df[(df["x"] > radius) & (df["x"] < (nx - radius))]
  df = df[(df["y"] > radius) & (df["y"] < (ny - radius))]
  df = df.reset_index(drop=True)
  return df


def remove_close(df, radius):
  """Remove close objects.

  Parameters
  ----------
  df : pandas.DataFrame
    input DataFrame which contains x, y
  radius : float
    removal threshold in pixel

  Return
  ------
  df : pandas.DataFrame
    close objects removed DataFrame
  """

  # Remove close objects.
  data = list(zip(df["x"], df["y"]))
  tree = KDTree(data, leafsize=10)
  res = tree.query_pairs(radius)
  idx_rm = [elem for inner in res for elem in inner]
  idx_rm = list(set(idx_rm))
  return df.drop(index=df.index[idx_rm])


def modify_ref(df_ref, key_objID):
  """
  Modify reference dataframe to 1 liner style using objID.
  Extract flux and fluxerr of each objects.
  [objID_ra, objID_dec, objID_flux, objID_fluxerr ...]
  """
  col_use = ["flux", "fluxerr", "eflag",
             "objinfoFlag", "qualityFlag", 
             "raMean", "decMean", "raMeanErr", "decMeanErr",
             "nStackDetections", "nDetections",
             "gQfPerfect", "gMeanPSFMag", "gMeanPSFMagErr", 
             "rQfPerfect", "rMeanPSFMag", "rMeanPSFMagErr", 
             "iQfPerfect", "iMeanPSFMag", "iMeanPSFMagErr", 
             "zQfPerfect", "zMeanPSFMag", "zMeanPSFMagErr", 
             "yQfPerfect", "yMeanPSFMag", "yMeanPSFMagErr", ]
  df_ref["objID"] = df_ref["objID"].astype(str)
  temp_list = []
  for idx,row in df_ref.iterrows():
    objID = row[key_objID]
    s_temp = df_ref.loc[idx, col_use]
    df_temp = pd.DataFrame([s_temp])
    df_temp = df_temp.add_suffix(f"_{objID}")
    df_temp = df_temp.reset_index(drop=True)
    temp_list.append(df_temp)
  df_mod = pd.concat(temp_list, axis=1)
  return df_mod 


def concat_allband(res_allband, bands):
  """
  Concatenate multi-bands DataFrame 
  and remove common raws (catalog ra, dec, magnitude etc.)

  Parameters
  ----------
  res_allband : list
    all bands photometry result
  bands : list
    all bands used as suffix like ["g", "r", "i"]
  """
  res_all = []
  for df,band in zip(res_allband,bands):
    df_temp = df.add_suffix(f"_{band}")
    res_all.append(df_temp)
  df = pd.concat(res_all, axis=1)
  return df


def extract_obj(df_all, bands):
  """Extract object data.

  Parameters
  ----------
  df_all : pandas.DataFrame
    all photometry result
  bands : list
    3 band used as suffix like ["g", "r", "i"]

  Return
  ------
  df_obj : pandas.DataFrame
    object DataFrame
  """

  # 18 is objID length (Pan-STARRS catalog)
  columns = df_all.columns.tolist()
  col_obj = [col for col in columns if (len(col)<18)]
  df_obj = df_all[col_obj]
  return df_obj


def time_keeper(func):
  """Decorator to measure time.
  """
  # To take over docstring etc.
  @wraps(func)
  def wrapper(*args, **kargs):
    t0 = time.time()
    result = func(*args, **kargs)
    t1 = time.time()
    t_elapse = t1 - t0
    print(f"[time keeper] t_elapse = {t_elapse:.03f} s (func :{func.__name__})")
    return result
  return wrapper


## Orbit prediction start =====================================================
class Orbit:
  """
  Time should be in days.
  Ra and Dec should be in degree.
  """
  def __init__(self, **kargs):
    self.t = kargs["t"]
    self.ra = kargs["ra"]
    self.dec = kargs["dec"]
    self.f_ra = interpolate.interp1d(
            self.t, self.ra, kind='linear', fill_value='extrapolate')
    self.f_dec = interpolate.interp1d(
            self.t, self.dec, kind='linear', fill_value='extrapolate')


  def calcloc(self, obstime):
    # ra, dec in degree
    return self.f_ra(obstime), self.f_dec(obstime)


def obtain_objorb(hdr_kwd, flist, fitsdir, slist):
  """
  Predict orbit of moving object by fitting.
  The function is for 2-d fits and optimized for murikabushi and TriCCS.

  Parameters
  ----------
  hdr_kwd : dict
    header keyword
  flist : str
    path of fits file list
  fitsdir : str
    path of fits file directory
  slist : str
    path of standard file (x, y, nfits, nframe) 

  Return
  ------
  orb : neoorb class
    neo orbit
  """

  t_standard, ra_standard, dec_standard = [], [], []
  x_s, y_s, nframe = [], [], []
  with open(slist, "r") as f_s:
    # skip header
    f_s = f_s.readlines()[1:]
    for line in f_s:
      splitline = line.split()
      x_s.append(int(splitline[0]))
      y_s.append(int(splitline[1]))
      nframe.append(int(splitline[2].split("\n")[0]))

  with open(flist, "r") as f:
    lines = f.readlines()
    for (x,y,i) in zip(x_s,y_s,nframe):
        
      tfits = lines[i-1].split("\n")[0]
      tfits = os.path.join(fitsdir, tfits)
      src = fits.open(tfits)[0]
      hdr = src.header
        
      if hdr_kwd["datetime"]:
        exp_start = hdr[hdr_kwd["datetime"]]
      else:
        exp_start = f"{hdr[hdr_kwd['date']]}T{hdr[hdr_kwd['time']]}"

      exp_frame = hdr[hdr_kwd["exp"]]
      obs_start = datetime.datetime.strptime(
        exp_start, "%Y-%m-%dT%H:%M:%S.%f")
      obs_center = obs_start + datetime.timedelta(seconds=exp_frame/2.0)
      obs_center = datetime.datetime.strftime(
        obs_center, "%Y-%m-%dT%H:%M:%S.%f")
      t = Time(str(obs_center), format='isot', scale='utc')
      t = t.mjd
      w = wcs(tfits)
      cra, cdec  = w.all_pix2world(x, y, 0)
      t_standard.append(t)
      ra_standard.append(cra)
      dec_standard.append(cdec)
  orb = Orbit(t=t_standard, ra=ra_standard, dec=dec_standard)
  return orb


## Orbit prediction end =======================================================

