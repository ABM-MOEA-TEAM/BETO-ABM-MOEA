# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 17:01:10 2021

@author: jacks074
"""

import geopandas as gpd
import geoplot 

import matplotlib.pyplot as plt

# from mapclassify import Quantiles, User_Defined

import pandas as pd
import seaborn as sns

# import numpy as np; np.random.seed(42)

# import mapclassify

import os
from pathlib import Path
cwd = os.getcwd()

path_list = [Path(cwd + '/readme_MFSP_data.csv')]


# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# boroughs = gpd.read_file(geoplot.datasets.get_path('nyc_boroughs'))

# collisions = gpd.read_file(geoplot.datasets.get_path('nyc_injurious_collisions'))

geoData = gpd.read_file('https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson')

geoData.id = geoData.id.astype(str).astype(int)

StateToRemove = ['02', '15', '72']
geoData = geoData[~geoData.STATE.isin(StateToRemove)]

# geoplot.polyplot(geoData, figsize=(20, 4))

data = pd.read_csv('https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/unemployment-x.csv')
mfsp_data = pd.read_csv(path_list[0])

#sns.distplot( data["rate"], hist=True, kde=False, rug=False );

fullData = geoData.merge(mfsp_data, left_on=['id'], right_on=['id'])

# Initialize the figure
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1, figsize=(16, 12))

# Set up the color sheme:
import mapclassify as mc
scheme = mc.EqualIntervals(fullData['mfsp'], k=8)
res = mc.Pooled(mfsp_data, k=8)

# Map
geoplot.choropleth(fullData, 
    hue="mfsp", 
    linewidth=.15,
    scheme=scheme, cmap='plasma_r',             # magma, viridis, mako, rocket, turbo, inferno, heat
    legend=True,                                        # Can also type in nonsense for this argument to get
    edgecolor='black',                                  # a very long list of all possible color palettes
    ax=ax);

ax.set_title('MFSP by County - $/kg', fontsize=15);