#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Color photmetry plot functions
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle


# Color
mycolor = ["#AD002D", "#1e50a2", "#006e54", "#ffd900", 
           "#EFAEA1", "#69821b", "#ec6800", "#afafb0", "#0095b9", "#89c3eb"] 
mycolor = mycolor*100

# Linestyle
myls = ["solid", "dashed", "dashdot", "dotted", (0, (5, 3, 1, 3, 1, 3)), 
        (0, (4,2,1,2,1,2,1,2))]
myls = myls*100


# Marker
mymark = ["o", "^", "x", "D", "+", "v", "<", ">", "h", "H"]
mymark = mymark*100


def myfigure(n):
  if n == 2:
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_axes([0.10, 0.15, 0.35, 0.8])
    ax2 = fig.add_axes([0.6, 0.15, 0.35, 0.8])
    return fig, ax1, ax2
  if n == 4:
    fig = plt.figure(figsize=(16, 10))
    ax1 = fig.add_axes([0.1, 0.6, 0.35, 0.35])
    ax2 = fig.add_axes([0.6, 0.6, 0.35, 0.35])
    ax3 = fig.add_axes([0.1, 0.10, 0.35, 0.35])
    ax4 = fig.add_axes([0.6, 0.10, 0.35, 0.35])
    return fig, ax1, ax2, ax3, ax4
  if n == 6:
    fig = plt.figure(figsize=(16, 18))
    ax1 = fig.add_axes([0.1, 0.72, 0.35, 0.25])
    ax2 = fig.add_axes([0.6, 0.72, 0.35, 0.25])
    ax3 = fig.add_axes([0.1, 0.4, 0.35, 0.25])
    ax4 = fig.add_axes([0.6, 0.4, 0.35, 0.25])
    ax5 = fig.add_axes([0.1, 0.08, 0.35, 0.25])
    ax6 = fig.add_axes([0.6, 0.08, 0.35, 0.25])
    return fig, ax1, ax2, ax3, ax4, ax5, ax6


def plot_photregion(
  image, stddev, df, radius, out, df0=None):
  """Plot region of circle photometry.

  Parameters
  ----------
  image : array-like
    object extracted image
  stddev : float
    image background standard deviation
  df : pandas.DataFrame
    finally used objects DataFrame
  radius : float
    aperture radius of circle photometry in pixel
  out : str
    output png filename
  df0 : pandas.DataFrame
    original objects DataFrame
  """
  
  vmin  = np.median(image)-1.5*stddev
  vmax  = np.median(image)+10.0*stddev
  ny, nx = image.shape
  fig = plt.figure(figsize=(12,int(12*ny/nx)))

  ax = fig.add_subplot(111)
  ax.imshow(image, cmap='gray', vmin=vmin, vmax=vmax)
  ax.scatter(
    df['x'], df['y'], color="blue", s=50, lw=3, facecolor="None", alpha=0.5,
    label="Final used (green photometry radius)")
  ax.add_collection(PatchCollection(
    [Circle((x,y), radius) for x,y in zip(df['x'], df['y'])],
    color="green", ls="dotted", lw=2, facecolor="None", 
    label="Photometry circle"))

  if df0 is not None:
    ax.scatter(
      df0['x'], df0['y'], color="red", s=400, linewidth=3, 
      facecolor="None", alpha=0.5, label="Original")
  
  ax.set_xlim([0, nx])
  ax.set_ylim([0, ny])
  ax.legend().get_frame().set_alpha(1.0)
  ax.invert_yaxis()
  plt.tight_layout()
  plt.savefig(out, dpi=100)
  plt.close()

