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


# scheme = mc.Quantiles(fullData['readme'], k=8)

# scheme = mc.UserDefined(fullData['readme'], [0,0.2,3000,6000,10000,14000,18000,20000])
# scheme = mc.UserDefined(fullData['readme'], [0.002,6000,25000,50000,100000,200000,350000])
# scheme = mc.UserDefined(fullData['readme'], [2.5,2.75,3,3.25,3.5,3.75,4,4.5,101])
# scheme = mc.UserDefined(fullData['readme'], [4,4.5,5,5.5,6,7,99])
# scheme = mc.UserDefined(fullData['readme'], [0.1,4000,6000,8000,10000,12000,14000])
# scheme = mc.UserDefined(fullData['readme'], [41,42,43,44,45,46,50])
scheme = mc.UserDefined(fullData['readme'], [400000,500000,750000,1000000,1500000,2000000,2500000,3500000])
# scheme = mc.UserDefined(fullData['readme'], [25,50,75,100,150,200,250])
# scheme = mc.UserDefined(fullData['readme'], [33,35,37,40,42,44,46,999])
# scheme = mc.UserDefined(fullData['readme'], [5,7.5,10,12.5,15,20,25,999])
# scheme = mc.UserDefined(fullData['readme'], [38.091,38.25,38.5,38.75])
# scheme = mc.UserDefined(fullData['readme'], [8,10,12,14,16,18,20])

# scheme = mc.UserDefined(fullData['readme'], [0.1,10000,25000,50000,100000,150000,200000,350000])

geoplot.choropleth(fullData,
                   linewidth = 0.1,
                   edgecolor = 'black',
                   hue = 'readme',
                   cmap = 'plasma_r',
                   scheme = scheme,
                   legend = True,
                    # legend_labels=['NA - No Yield Data',
                    #                   '0 - 10,000 Tonnes Soybean per Hectare',
                    #                   '10,000 - 25,000 Tonnes Soybean per Hectare', 
                    #                   '25,000 - 50,000 Tonnes Soybean per Hectare', 
                    #                   '50,000 - 100,000 Tonnes Soybean per Hectare', 
                    #                   '100,000 - 150,000 Tonnes Soybean per Hectare', 
                    #                   '150,000 - 200,000 Tonnes Soybean per Hectare',
                    #                   '200,000 - 350,000 Tonnes Soybean per Hectare',
                    #                   '350,000 + Tonnes Soybean per Hectare'],
                   # legend_labels=['< $5.00/GGE',
                   #                  '5.00 - 7.50 $/GGE',
                   #                  '7.50 - 10.00 $/GGE', 
                   #                  '10.00 - 12.50 $/GGE', 
                   #                  '12.50 - 15.00 $/GGE', 
                   #                  '15.00 - 20.00 $/GGE', 
                   #                  '20.00 - 25.00 $/GGE',
                   #                  '> 25.00 $/GGE',
                   #                  'NA - No Yield Data'],
                   # legend_labels=[   '< 33 g CO2 eq / MJ',
                   #                    '33 - 35 g CO2 eq / MJ', 
                   #                    '35 - 37 g CO2 eq / MJ', 
                   #                    '37 - 40 g CO2 eq / MJ', 
                   #                    '40 - 42 g CO2 eq / MJ', 
                   #                    '42 - 44 g CO2 eq / MJ',
                   #                    '44 - 46 g CO2 eq / MJ',
                   #                    '> 46 g CO2 eq / MJ',
                   #                    'N/A - No Yield Data'],
                   # legend_labels=[   '< 25 g CO2 eq / MJ',
                   #                    '25 - 50 g CO2 eq / MJ', 
                   #                    '50 - 75 g CO2 eq / MJ', 
                   #                    '75 - 100 g CO2 eq / MJ', 
                   #                    '100 - 150 g CO2 eq / MJ', 
                   #                    '150 - 200 g CO2 eq / MJ',
                   #                    '200 - 250 g CO2 eq / MJ',
                   #                    '> 250 g CO2 eq / MJ'],
                    legend_labels=['< $400,000 per 100 ha',
                                      '400,000 - 500,000 $/100 ha',
                                      '500,000 - 750,000 $/100 ha', 
                                      '750,000 - 1,000,000 $/100 ha', 
                                      '1.000,000 - 1,500,000 $/100 ha', 
                                      '1,500,000 - 2,000,000 $/100 ha', 
                                      '2,000,000 - 2,500,000 $/100 ha',
                                      '2,500,000 - 3,500,000 $/100 ha',
                                      # '> 3,500,000 $/100 ha'],
                                      'N/A No Land Data'],
                   # legend_labels=['< $2.50/GGE',
                   #                  '2.50 - 2.75 $/GGE',
                   #                  '2.75 - 3.00 $/GGE', 
                   #                  '3.25 - 3.50 $/GGE', 
                   #                  '3.50 - 3.75 $/GGE', 
                   #                  '3.75 - 4.00 $/GGE', 
                   #                  '4.00 - 4.50 $/GGE',
                   #                  '4.50 + $/GGE',
                   #                  'NA - No Yield Data'],
                   # legend_labels=[   '< 41 g CO2 eq / MJ',
                   #                   '41 - 42 g CO2 eq / MJ', 
                   #                   '42 - 43 g CO2 eq / MJ', 
                   #                   '43 - 44 g CO2 eq / MJ', 
                   #                   '44 - 45 g CO2 eq / MJ', 
                   #                   '45 - 46 g CO2 eq / MJ',
                   #                   '46 + g CO2 eq / MJ',
                   #                   'NA - No Yield Data'], 
                       # legend_labels=['NA - No Yield Data',
                       #               '0 - 4,000 Tonnes Corn Grain per Hectare',
                       #               '4,000 - 6,000 Tonnes Corn Grain per Hectare', 
                       #               '6,000 - 8,000 Tonnes Corn Grain per Hectare', 
                       #               '8,000 - 10,000 Tonnes Corn Grain per Hectare', 
                       #               '10,000 - 12,000 Tonnes Corn Grain per Hectare', 
                       #               '12,000 - 14,000 Tonnes Corn Grain per Hectare',
                       #               '14,000 + Tonnes Corn Grain per Hectare'],
                   # legend_labels = ['0.00 - 0.10 $/kg',
                   #                '0.10 - 0.20 $/kg',
                   #                '0.20 - 0.30 $/kg',
                   #                '0.30 - 0.40 $/kg',
                   #                '0.40 - 0.50 $/kg',
                   #                '0.50 - 1.00 $/kg',
                   #                'NA - No Yield Data'],
                    # legend_labels = [   '0.00 - 0.20 $ / GGE',
                    #                     '0.20 - 0.40 $ / GGE',
                    #                     '0.40 - 0.60 $ / GGE',
                    #                     '0.60 - 0.80 $ / GGE',
                    #                     '0.80 - 1.00 $ / GGE',
                    #                     '1.00 - 2.00 $ / GGE',
                    #                     '2.00 - 3.00 $ / GGE',
                    #                     '3.00 + $/GGE',
                    #                     'No Data Available'],
                    # legend_labels=['NA - No Yield Data',
                    #                 '0 - 3,000 Tonnes CO2 eq',
                    #                 '3,000 - 6,000 Tonnes CO2 eq', 
                    #                 '6,000 - 10,000 Tonnes CO2 eq', 
                    #                 '10,000 - 14,000 Tonnes CO2 eq', 
                    #                 '14,000 - 16,000 Tonnes CO2 eq', 
                    #                 '16,000 - 18,000 Tonnes CO2 eq',
                    #                 '18,000 - 20,000 Tonnes CO2 eq',
                    #                 '20,000 + Tonnes CO2 eq'
                    #                 ],
                    # legend_labels=['NA - No Yield Data',
                    #                 '0 - 6,000 Tonnes Corn Grain',
                    #                 '6,000 - 25,000 Tonnes Corn Grain', 
                    #                 '25,000 - 50,000 Tonnes Corn Grain', 
                    #                 '50,000 - 100,000 Tonnes Corn Grain', 
                    #                 '100,000 - 200,000 Tonnes Corn Grain', 
                    #                 '200,000 - 350,000 Tonnes Corn Grain',
                    #                 # '350,000 - 500,000 Tonnes Corn Grain',
                    #                 '350,000 + Tonnes Corn Grain'
                    #                 ],
                    
                    # legend_labels=['< $4.00/GGE',
                    #                 '4.00 - 4.50 $/GGE',
                    #                 '4.50 - 5.00 $/GGE', 
                    #                 '5.00 - 5.50 $/GGE', 
                    #                 '5.50 - 6.00 $/GGE', 
                    #                 '6.00 - 7.00 $/GGE', 
                    #                 '7.00 + $/GGE',
                    #                 'NA - No Yield Data'],
                    
                   ax = ax)

ax.set_title('County Level Land Cost Data - Ece Set - $/100 hectare', fontsize=15);
# ax.set_title('Corn EtOH GHG - Energy Allocation - Post-Combustion', fontsize=15);