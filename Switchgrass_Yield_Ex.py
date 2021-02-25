# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:02:15 2021

@author: Jack Smith
"""

import csv

import pandas as pd
import pint
import os
from pathlib import Path
cwd = os.getcwd()
ureg = pint.UnitRegistry()
ureg.define('dollars = [money]')

import TEA_LCA_Data as D
import UnivFunc as UF

import TEA
import LCA

# Process steps
import Grow_Grass as GG
import Grow_Grass2 as GG2
import GasFT as GFT
import Hydroprocessing as H
import ProcessModel as PM

# Initializes empty output table
results_array = UF.createEmptyFrame()

path_list = [Path(cwd + '/Ex_Yield_Switchgrass_IA.csv'), 
             Path(cwd + '/Ex_Lookup.csv')]

DayCent_County = 'County'
DayCent_Yield = 'Yield_Mg_hay'
DayCent_Yield_Data = pd.read_csv(path_list[0])

switchgrass_yields_dict = {}

def Collect_DayCent():
    
    DayCent_Scales = []    
    
    for i in range(len(DayCent_Yield_Data)):
        row = DayCent_Yield_Data.loc[i]
        DayCent_Scales.append(row[DayCent_Yield])            
    
    return DayCent_Scales

DayCent_Yields = Collect_DayCent()   

output = UF.createEmptyFrame()


land_area_val = D.TEA_LCA_Qty('Land Area', 100, 'hectare')
biomass_output = D.TEA_LCA_Qty('Woody Biomass', 1, 'kg/yr/ha')  # Fudging the units currently - need to fix
    
def Grassification_GWP(j):
      
    results_array = UF.createEmptyFrame()
    
    Yield = D.TEA_LCA_Qty('Woody Biomass', DayCent_Yields[j]*1000, 'kg/yr/ha')
    
    biomass_IO = GG.growGrassForOneYear(land_area_val, Yield)
    results_array = results_array.append(biomass_IO, ignore_index=True)
    
    # Extraction/Conversion
    conversion_IO = GFT.convertGrassBiomass(land_area_val, results_array)
    results_array = results_array.append(conversion_IO, ignore_index=True)
    
    # Upgrading
    upgrading_IO = H.upgradeGrassProducts(land_area_val,results_array)
    results_array = results_array.append(upgrading_IO, ignore_index=True)
    
    # Process Control Vol IO
    IO_array = UF.consolidateIO(results_array)
   
    # Calculate GHG Impact
    ghg_impact = LCA.calcGHGImpact(IO_array)
         
    return ghg_impact


def Grassification_MFSP(j):
    
    results_array = UF.createEmptyFrame()
    
    Yield = D.TEA_LCA_Qty('Woody Biomass', DayCent_Yields[j]*1000, 'kg/yr/ha')
    
    biomass_IO = GG.growGrassForOneYear(land_area_val, Yield)
    results_array = results_array.append(biomass_IO, ignore_index=True)
    
    # Extraction/Conversion
    conversion_IO = GFT.convertGrassBiomass(land_area_val, results_array)
    results_array = results_array.append(conversion_IO, ignore_index=True)
    
    # Upgrading
    upgrading_IO = H.upgradeGrassProducts(land_area_val,results_array)
    results_array = results_array.append(upgrading_IO, ignore_index=True)
    
    # Process Control Vol IO
    IO_array = UF.consolidateIO(results_array)
       
    # Calculate GHG Impact
    mfsp = TEA.calc_MFSP(IO_array)
    
    return mfsp




f = open('Ex_Lookup.csv','w')

with f:
    
    writer = csv.writer(f)
    writer.writerow(['County','MFSP','GWP'])
    i = 0
    while i < len(DayCent_Yields):

        # MFSP = 1
        # GWP = 2
        
        # MFSP = DayCent_Yields[i]
        # GWP = DayCent_Yields[i]
        
        MFSP = Grassification_MFSP(i)
        GWP = Grassification_GWP(i)
        
        #print(DayCent_Yields[i])
        Output_array = [i,MFSP,GWP]
        writer.writerows([Output_array])
        if(i == 10):
            print('10%....')
        if(i == 20):
            print('20%....')
        if(i == 30):
            print('30%....')
        if(i == 40):
            print('40%....')
        if(i == 50):
            print('50%....')
        if(i == 60):
            print('60%....')
        if(i == 70):
            print('70%....')
        if(i == 80):
            print('80%....')
        if(i == 90):
            print('90%....')
        i += 1
        
        # print(i)
    
