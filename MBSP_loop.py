# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:44:28 2021

@author: Jack Smith
"""

# 63 Year normalized data-set crop production feed loop

import LifeCycleAssessment as L
import TEA_LCA_Data as D
import TEA
import pandas as pd
import LifeCycleAssessment
import UnivFunc as UF

import os
from pathlib import Path

cwd = os.getcwd()

path_list = [Path(cwd + '/normalized_corn_yields.xlsx')] # Presumably will all be in this file

excel_read = pd.read_excel(path_list[0])

corn_yields = []

MBSPs       = []

ol = ['']

for i in range(len(excel_read)):
    rows = excel_read.loc[i]
    corn_yields.append(rows['Corn Yields'])
    

def get_MBSP(yield_value):
    
    prod = ['Corn Grain']
    coprods = ['Corn Stover']
    
    biomass_IO = UF.Collect_IndepVars_Loop('CornCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
    
    MBSP = TEA.calc_MBSP(biomass_IO, prod, coprods, 'Corn Grain EtOH', 9001, ol)
    print(MBSP.magnitude * 16.1)
    
    return MBSP.magnitude * 16.1

def execute():

    j = 0    

    # for i in range(800):
    for i in range(len(corn_yields)):
    
        yield_value = corn_yields[i]
        add_value   = get_MBSP(yield_value)
        MBSPs.append(add_value)
        
        if i % 100 == 0:
            j += 1
            
        if j == 5:
            print('Through first 500 entries')
        if j == 10:
            print('Through first 1000 entries')
        if j == 15:
            print('Through first 1500 entries')
        if j == 20:
            print('Through 2000 entries')
        if j == 25:
            print('Through 2500 entries')
        if j == 30:
            print('Through 3000 entries')
        if j == 40:
            print('Through 4000 entries')
        if j == 50:
            print('Through 5000 entries')
        if j == 60:
            print('Through 6000 entries')
        if j == 65:
            print('Almost done')
        
    return MBSPs

    
    
    
    
    
    
    
    
    
    