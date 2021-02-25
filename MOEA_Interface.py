# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 22:56:44 2021

@author: Jack Smith
"""

import pandas as pd
import os
import pint
from pathlib import Path

cwd = os.getcwd()   # Obtains the current working directory


def Collect_DayCent():
    path_list = [Path(cwd + '/DayCent_switchgrass_CountyData.csv'),
                 Path(cwd + '/LCA_Inventory.csv'),
                 Path(cwd + '/Substances.csv')]      
    
    # Array of file names. In the future, this will include all Daycent .csv's (hence the array)
    # Edited the DayCent .csv - removed the first row to simplify the read

    DayCent_Yield_ha = 'yield_Mg_ha'    # New string to match to column in DayCent .csv
    DayCent_GHG_ha = 'ghg_MgCO2e_ha'    # Looks like this does not include CH4, N20, etc. Ask, also SOC mechanism
    DayCent_N2O_ha = 'dN2ON_kgN_ha'     # Clarity on dN2ON and iN2ON?
    DayCent_CH4_ha = 'kgCH4_ox_ha'     
    DayCent_SOC_ha = 'dSOC_MgC_ha'      # Again, just find distinction of 'd' prefix

    DayCent_data = pd.read_csv(path_list[0])
    
    Yield_list = []
    for i in range(len(DayCent_data)):
        row = DayCent_data.loc[i]
        Yield_list.append(row[DayCent_Yield_ha])

    GHG_list = []
    for i in range(len(DayCent_data)):
        row = DayCent_data.loc[i]
        GHG_list.append(row[DayCent_GHG_ha])

    N2O_list = []
    for i in range(len(DayCent_data)):
        row = DayCent_data.loc[i]
        N2O_list.append(row[DayCent_N2O_ha])
        
    CH4_list = []
    for i in range(len(DayCent_data)):
        row = DayCent_data.loc[i]
        CH4_list.append(row[DayCent_CH4_ha])

    SOC_list = []
    for i in range(len(DayCent_data)):
        row = DayCent_data.loc[i]
        SOC_list.append(row[DayCent_SOC_ha])
    
    print('Done')
    return Yield_list#, GHG_list, N2O_list, CH4_list, SOC_list

# Outputting all as an aggregated Tuple to see what duration of run looks like. Can units be left off?

def main():
    
    Yield_list = []
    GHG_list = []
    N2O_list = []
    CH4_list = []
    SOC_list = []
    
    return Collect_DayCent()

if __name__ == "__main__":
    output = main()
# 