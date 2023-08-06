#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handmade Pan-STARRS catalog handling script using SQLite.

The options are 
  1. create
    create new table
  2. insert
    insert objects to database
  3. extract
    extract objects from database

Use photometric quality flag (ratio of weighted masked pixels) 
gQfPerfect etc. to select good quality data. 
This leads to avoid selection of saturated stars(?).

Note: known bug:
  When no object returned, `NameError: name 'warnings' is not defined` happens.

History:
  Column number is 24.(2021/03/10)
  Column number is 29.(2021/04/03) add gQfPerfect etc.
"""
from argparse import ArgumentParser as ap
import os
import sys
import sqlite3
from contextlib import closing
import time
from astroquery.mast import Catalogs
from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
import pandas as pd


def hmsdms2deg(ra, dec):
  """Convert hmsdms to degree

  Parameters
  ----------
  ra : str
    right acsension in hms
  dec : str
    declination in dms
  
  Returns
  --------
  ra : str
    right acsension in degree
  dec : str
    declination in degree
  """
  radec = f"{ra} {dec}"
  c = SkyCoord(radec, unit=(u.hourangle, u.degree))
  radec = c.to_string("decimal")
  ra = radec.split(" ")[0]
  dec = radec.split(" ")[1]
  return ra, dec


def create_table(db, table):
  """Create table in db

  Parameters
  ----------
  db : str
    path of sqlite3 database
  table : str
    table name of sqlite3 database
  """

  with closing(sqlite3.connect(db)) as conn:
    c = conn.cursor()
    sql = (
      f"CREATE TABLE IF NOT EXISTS"\
      f" {table}("\
      f"objID int unique, objinfoFlag int, qualityFlag int,"\
      f"raMean real, decMean real, raMeanErr real, decMeanErr real,"\
      f"nStackDetections int, nDetections int,"\
      f"gQfPerfect real, gMeanPSFMag real, gMeanPSFMagErr real, gFlags int,"\
      f"rQfPerfect real, rMeanPSFMag real, rMeanPSFMagErr real, rFlags int,"\
      f"iQfPerfect real, iMeanPSFMag real, iMeanPSFMagErr real, iFlags int,"\
      f"zQfPerfect real, zMeanPSFMag real, zMeanPSFMagErr real, zFlags int,"\
      f"yQfPerfect real, yMeanPSFMag real, yMeanPSFMagErr real, yFlags int)"
    )
    c.execute(sql)
    conn.commit()


def query_ps(ra, dec, radius, magmin, magmax):
  """
  Query Pan-STARRS catalog and output as pandas.DataFrame.
  Extract bright and high quality objects.

  Parameters
  ----------
  ra, dec : float
    right ascension, declination of field in degree
  radius : int
    radius of filed of view in degree
  magmin, magmax : float
    the brightest/faintest magnitude to be considered (g-band)

  Return
  ------
  df : pandas.DataFrame
    result DataFrame
  """

  radec = SkyCoord(ra=ra, dec=dec, unit=(u.degree, u.degree))
  columns= ["objID", "objinfoFlag", "qualityFlag", 
           "raMean", "decMean", "raMeanErr", "decMeanErr",
           "nStackDetections", "nDetections",
           "gQfPerfect", "gMeanPSFMag", "gMeanPSFMagErr", "gFlags",
           "rQfPerfect", "rMeanPSFMag", "rMeanPSFMagErr", "rFlags",
           "iQfPerfect", "iMeanPSFMag", "iMeanPSFMagErr", "iFlags",
           "zQfPerfect", "zMeanPSFMag", "zMeanPSFMagErr", "zFlags",
           "yQfPerfect", "yMeanPSFMag", "yMeanPSFMagErr", "yFlags"]

  # Criteria for error and quality
  magerr_min = 1e-10
  magerr_max = 0.1
  magQ_min = 0.85

  dr = "dr2"
  tabletype = "mean"
  t0 = time.time()
  res = Catalogs.query_criteria(
    coordinates=radec, radius=radius, catalog="PANSTARRS", 
    gMeanPSFMag=[("lte", magmax),("gte", magmin)], 
    rMeanPSFMag=[("lte", magmax),("gte", magmin)],
    iMeanPSFMag=[("lte", magmax),("gte", magmin)],
    gMeanPSFMagErr=[("lte", magerr_max),("gte", magerr_min)],
    rMeanPSFMagErr=[("lte", magerr_max),("gte", magerr_min)],
    iMeanPSFMagErr=[("lte", magerr_max),("gte", magerr_min)],
    gQfPerfect=[("gte", magQ_min)],
    grfPerfect=[("gte", magQ_min)],
    gifPerfect=[("gte", magQ_min)],
    table=tabletype, data_release=dr, columns=columns,
    timeout=6000) 
  t1 = time.time()
  print(f"query time : {t1-t0}s")

  # Avoid int64 error for objID
  ID_str = [str(res[i]["objID"]) for i in range(len(res))]
  res["objID"] = ID_str

  df = res.to_pandas()
  return df


def insert_ps(db, table, df):
  """Insert Pan-STARES catalog and output pandas.Data.

  Parameters
  ----------
  db : str
    path of sqlite3 database
  table : str
    table name of sqlite3 database
  df : pandas.DataFrame
    DataFrame to be inserted
  """

  n_col = 29
  with closing(sqlite3.connect(db)) as conn:
    c = conn.cursor()
    spots = ",".join(["?"]*n_col)
    sql = ( 
      f"INSERT OR IGNORE INTO {table}"\
      f"(objID, objinfoFlag, qualityFlag,"\
      f"raMean, decMean, raMeanErr, decMeanErr,"\
      f"nStackDetections, nDetections,"\
      f"gQfPerfect, gMeanPSFMag, gMeanPSFMagErr, gFlags,"\
      f"rQfPerfect, rMeanPSFMag, rMeanPSFMagErr, rFlags,"\
      f"iQfPerfect, iMeanPSFMag, iMeanPSFMagErr, iFlags,"\
      f"zQfPerfect, zMeanPSFMag, zMeanPSFMagErr, zFlags,"\
      f"yQfPerfect, yMeanPSFMag, yMeanPSFMagErr, yFlags) values({spots})"
    )
    for idx, row in df.iterrows():
      data = row.to_numpy()
      assert len(data)==n_col, "Invalid columns number!!" 
      print(data)
      c.execute(sql, data)
    conn.commit()


def extract_ps(db, table, ra, dec, radius, magmin, magmax):
  """Extract Pan-STARES catalog data and return as pandas.DataFrame.

  Parameters
  ----------
  db : str
    path of sqlite3 database
  table : str
    table name of sqlite3 database
  ra, dec : float
    right ascension, declination of field in degree.
  radius : int
    radius of filed of view in degree
  magmin, magmax : float
    the brightest/faintest magnitude to be considered (g-band)

  Return
  ------
  df : pandas.DataFrame
    extracted DataFrame
  """

  with closing(sqlite3.connect(db)) as conn:
    c = conn.cursor()
    sql = ( 
      f"SELECT "\
      f"objID, objinfoFlag, qualityFlag,"\
      f"raMean, decMean, raMeanErr, decMeanErr,"\
      f"nStackDetections, nDetections,"\
      f"gQfPerfect, gMeanPSFMag, gMeanPSFMagErr, gFlags,"\
      f"rQfPerfect, rMeanPSFMag, rMeanPSFMagErr, rFlags,"\
      f"iQfPerfect, iMeanPSFMag, iMeanPSFMagErr, iFlags,"\
      f"zQfPerfect, zMeanPSFMag, zMeanPSFMagErr, zFlags,"\
      f"yQfPerfect, yMeanPSFMag, yMeanPSFMagErr, yFlags from {table}"\
      f" WHERE raMean > {ra-radius} and raMean < {ra+radius}"\
      f" and decMean > {dec-radius} and decMean < {dec+radius}"\
      f" and gMeanPSFMag > {magmin} and gMeanPSFMag < {magmax}"
    )
    df = pd.read_sql_query(sql=sql, con=conn)
    conn.commit()
  return df


if __name__=="__main__":
  parser = ap(description="handling Pan-STARRS database test")
  parser.add_argument(
    "action", choices=["dbstart", "insert", "extract", "first"], 
    help="actions to be done")
  parser.add_argument(
    "--table", type=str, 
    help="table name")
  parser.add_argument(
    "--ra", default=120, type=float, 
    help="center of right ascention in degree")
  parser.add_argument(
    "--dec", default=0, type=float, 
    help="center of declination in degree")
  parser.add_argument(
    "--radius", default=0.05, type=float, 
    help="object search radius in degree")
  parser.add_argument(
    "--magmin", default=14., type=float, 
    help="minimum magnitude")
  parser.add_argument(
    "--magmax", default=17., type=float, 
    help="maximum magnitude")
  parser.add_argument(
    "--dbdir",  type=str, default=None,
    help="database directory name")
  args = parser.parse_args()


  if args.dbdir:
    db = os.path.join(args.dbdir, "ps.db")
  else:
    # Default database directory
    db4movphot = "~/db4movphot"
    os.makedirs(db4movphot, exist_ok=True)
    db = os.path.join(db4movphot, "ps.db")

  # Create database itself
  if args.action=="dbstart":
    if os.path.exists(db):
      print(f"Already exists {db}")
      sys.exit()
    else:
      conn = sqlite3.connect(db)
      conn.close()
      print(f"Database {db} creation successfully finished!")


  # Create new table
  if args.action=="create":
    table = args.table
    create_table(db, table)
    print(f"Successfully created '{db}/{table}' !")


  # Insert stars in a table
  if args.action=="insert":
    table = args.table
    df = query_ps(
      args.ra, args.dec, args.radius, args.magmin, args.magmax)
    print("Query result:")
    print(df)
    insert_ps(db, table, df)
    print(f"{len(df)} objects successfully inserted to '{db}/{table}' !")


  # Extract stars to check
  if args.action=="extract":
    table = args.table
    df = extract_ps(
      db, table, args.ra, args.dec, args.radius, args.magmin, args.magmax)
    print(f"{len(df)} objects extracted from '{db}/{table}' !")
    print("raw df")
    print(df)
    
    df["b_qualityFlag"] = [format(x, "08b") for x in df["qualityFlag"]]
    df["b_objinfoFlag"] = [format(x, "031b") for x in df["objinfoFlag"]]
    print(df[["b_qualityFlag", "b_objinfoFlag"]])
     

    # object IDed with knwon quasar
    # xxxx1xx means the object is known quasar
    N = 31
    n = 3
    for i in range(len(df)):
      if df.at[i, "b_objinfoFlag"][N-n]=="1":
        print("known quasar")
   

    # object IDed with knwon quasar
    # bad data 3-12 characters (quasar, moving objects etc.)
    N = 31
    n_list = [i for i in range(3, 13)]
    for i in range(len(df)):
      for n in n_list:
        if df.at[i, "b_objinfoFlag"][N-n]=="1":
          print("quasar or moving objects or ...")
          print(f"{i}th character, n_row={i+1}, objID={df.at[i, 'objID']}"
                f"gmag={df.at[i, 'gMeanPSFMag']}")

    #  # good
    #  N = 31
    #  n = 27
    #  for i in range(len(df)):
    #    if df.at[i, "b_objinfoFlag"][N-n]=="1":
    #      print("GOOD")

   
