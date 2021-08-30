# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 09:40:49 2021

@author: Jack Smith
"""

import geopandas as gpd
import geoplot
import mapclassify as mc
import matplotlib.pyplot as plt

import pandas as pd

import os
from pathlib import Path
cwd = os.getcwd()

path_list = [Path(cwd + '/readme_MFSP_data.csv')]

geoData = gpd.read_file('https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/US-counties.geojson')

geoData.id = geoData.id.astype(str).astype(int)

StateToRemove = ['02', '15', '72']
geoData = geoData[~geoData.STATE.isin(StateToRemove)]

mfsp_data = pd.read_csv(path_list[0])

fullData = geoData.merge(mfsp_data, left_on=['id'], right_on=['id'])

fig, ax = plt.subplots(1, 1, figsize=(16, 12))


scheme = mc.Quantiles(fullData['readme'], k=8)

# scheme = mc.UserDefined(fullData['readme'], [0.1,0.2,0.3,0.4,0.5,1])
# scheme = mc.UserDefined(fullData['readme'], [43,44,45.5,48,160,161])


geoplot.choropleth(fullData,
                   linewidth = 0.1,
                   edgecolor = 'black',
                   hue = 'readme',
                   cmap = 'plasma_r',
                   scheme = scheme,
                   legend = True,
                   # legend_labels = ['0.00 - 0.10 $/kg',
                   #                '0.10 - 0.20 $/kg',
                   #                '0.20 - 0.30 $/kg',
                   #                '0.30 - 0.40 $/kg',
                   #                '0.40 - 0.50 $/kg',
                   #                '0.50 - 1.00 $/kg',
                   #                'NA - No Yield Data'],
                    # legend_labels = ['0.00 - 6.50 $ / GGE',
                    #                    '6.50 - 14.00 $ / GGE',
                    #                    '14.00 - 16.00 $ / GGE',
                    #                    '16.00 - 18.00 $ / GGE',
                    #                    '18.00 - 22.00 $ / GGE',
                    #                    '22.00 - 189.00 $ / GGE',
                    #                    'NA - No Yield Data'],
                    # legend_labels=['0 - 43 gCO2eq/MJ',
                    #                 '43 - 44 gCO2eq/MJ', 
                    #                 '44 - 45.5 gCO2eq/MJ', 
                    #                 '45.5 - 48 gCO2eq/MJ', 
                    #                 '48 - 161 gCO2eq/MJ', 
                    #                 'NA - No Yield Data'],

                   ax = ax)

ax.set_title('Soy Total Tonnes Produced', fontsize=15);
# ax.set_title('Corn EtOH GHG - Energy Allocation - Post-Combustion', fontsize=15);