#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:24:51 2021

@author: asya

Script that generates and plots surface density by drawing a Voronoi diagram from particle coordinates
and colouring each Voronoi region by the mean density of itself and its nearest neigbours.

Examples and further documentation may be found in the accompanying README.md
"""

import sys
import copy
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LogNorm
from scipy.spatial import Voronoi,ConvexHull,KDTree

## input parameters -----------------------------------------------------------------------------------------------------
points = np.load(sys.argv[1])

# probabilities for each particle to represent a star, such that each density is
# the sum of probabilities in that area divided by the area
probs = np.load(sys.argv[2])

# number of nearest neighbours (including original point)
# must be >= 2
n_neighbors = 2

lower_limit = 1e-6

## ----------------------------------------------------------------------------------------------------------------------

def RGBtoHex(vals, rgbtype=1):
    """ Converts RGB values to Hex values

    Parameters
    ----------
    vals : tuple
        An RGB/RGBA tuple.
    rgbtype : int, optional
        Valid values are:
            1   - Inputs are in the range 0 to 1
            256 - Inputs are in the range 0 to 255.
        The default is 1.

    Raises
    ------
    Exception
        Invalid input parameter.

    Returns
    -------
    str
        Hex value corresponding to input.

    """
    if len(vals)!=3 and len(vals)!=4:
        raise Exception("RGB or RGBA inputs to RGBtoHex must have three or four elements!")
    if rgbtype!=1 and rgbtype!=256:
        raise Exception("rgbtype must be 1 or 256!")

    #Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
    if rgbtype==1:
        vals = [255*x for x in vals]

    #Ensure values are rounded integers, convert to hex, and concatenate
    return '#' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])

## Initialise Voronoi diagram and KDTree ---------------------------------------------------------------------------------
t0 = time.time()
vor = Voronoi(points)
kdt = KDTree(points);

## Determine Colours of Each Region --------------------------------------------------------------------------------------
den = np.zeros(vor.npoints)
for i, reg_num in enumerate(vor.point_region):
    print('finding nearest neighbours...\t\t\t{0:06.2f}%'.format(i/len(vor.point_region)*100),end='\r')
    nbrs_idx = kdt.query(points[i],k=n_neighbors)[1];

    neighborhood_area = 0
    neighborhood_probability = 0
    for idx in nbrs_idx:
        reg_idx = vor.point_region[idx]
        indices = vor.regions[reg_idx]
        prob = probs[idx]
        if -1 in indices: # some regions may be open
            neighborhood_area += np.inf
            neighborhood_probability += prob
        else:
            neighborhood_area += ConvexHull(vor.vertices[indices]).volume
            neighborhood_probability += prob
    den[i] = neighborhood_probability/neighborhood_area

# normalised to central density = 1
den /= max(den)

# remove particles below given limit
den = np.ma.masked_where(den <= lower_limit, den).filled(0)

# normalize chosen colormap
colormap = copy.copy(cm.get_cmap('magma'))
colormap.set_bad(colormap(0))
mapper = cm.ScalarMappable(norm=LogNorm(vmax=max(den),vmin=lower_limit), cmap=colormap)


## Generate Figure -------------------------------------------------------------------------------------------------------
print('\ngenerating figure...')
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

#uncomment the following to see regions outlined:
#voronoi_plot_2d(vor,ax,show_vertices=False,show_points=False,line_colors='k',line_width=0.1)

ax.set_xlim(-5,5); ax.set_ylim(-5,5); ax.set_xticks(np.arange(-4,4.1,2)); ax.set_yticks(np.arange(-4,4.1,2))
ax.set_aspect((ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0]))

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.67])
cbr = fig.colorbar(mapper,cax=cbar_ax)
cbr.set_label('$\Sigma$',fontsize=10)

ax.set_xlabel('[deg]',fontsize=10)
ax.set_ylabel('[deg]',fontsize=10)

## Colorize each region --------------------------------------------------------------------------------------------------
N = len(vor.point_region)
t1 = time.time()
for r in range(N):
    region = vor.regions[vor.point_region[r]]
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        ax.fill(*zip(*polygon),RGBtoHex(mapper.to_rgba(den[r])),edgecolor=RGBtoHex(mapper.to_rgba(den[r])),linewidth=0.25)
    print('estimated time to completion: {1:03.0f} minutes\t{0:06.2f}%'.format((r+1)/N*100,(time.time()-t1)/60/(r+1)*(N-r-1)),end='\r')

# ----------------------------------------------------------------------------------------------
print('\nsaving image...\r')
plt.savefig('images/{}neighbors'.format(n_neighbors),dpi=300,bbox_inches = 'tight',pad_inches=0.02)
print('image saved!\t')
