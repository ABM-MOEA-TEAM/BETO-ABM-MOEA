# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:07:21 2021

@author: Jack Smith
"""

# For Loups

# Crop Yield Fors 

import LifeCycleAssessment as L
import TEA_LCA_Data as D
import TEA
import pandas as pd
import LifeCycleAssessment
import UnivFunc as UF

import os
from pathlib import Path


cwd = os.getcwd()

path_list = [Path(cwd + '/readme_yields.xlsx')] # Presumably will all be in this file

excel_read = pd.read_excel(path_list[0])

def yield_to_price(IO_array):
    
    return_value = 0
    
    prod = ['Corn Grain']
    coprods = ['Corn Stover']
    
    path_string = 'Corn Grain EtOH'
    
    MBSP = TEA.calc_MBSP(IO_array, prod, coprods, path_string)
    
    return_value = MBSP.magnitude * 20

    
    return return_value

def loops():
    
    return_list = []
    j = 0
    
    corn_yields = []
    soy_yields = []
    
    for i in range(len(excel_read)):
        rows = excel_read.loc[i]
        corn_yields.append(rows['Corn'])
        soy_yields.append(rows['Soy'])
    
    # Soy Cultivation Bits
    
    j = 0
    
    prod = ['Soybeans']
    coprods = ['']
    
    BD_return_list = []
    LC_BD_return = []
    
    for i in range(len(soy_yields)):
    
        BD_results_array = UF.createEmptyFrame()    
    
        yield_value = soy_yields[i] * 1000
        
        if yield_value != 0:
            
            biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
            BD_results_array = BD_results_array.append(biomass_IO, ignore_index=True)
            IO_array = UF.consolidateIO(BD_results_array)
            
            BD_MBSP = TEA.calc_MBSP(IO_array, prod, coprods, 'Soy Biodiesel')
            LC_BD = LifeCycleAssessment.LCAMetrics_cult(IO_array)
            BD_return_list.append(BD_MBSP.magnitude * 20)
            LC_BD_return.append(LC_BD[1])
            
            if i % 10 == 0:
                j += 1
                if j % 5 == 0 and j % 10 != 0:
                    print('...')
                if j == 49:
                    print('16% Completed')
                if j == 103:
                    print('33% Completed')
                if j == 154:
                    print('50% Completed')
                if j == 203:
                    print('66% Completed')
                if j == 256:
                    print('83% Completed')
                if j == 300:
                    print('99% Completed')
        
        else: 
            BD_return_list.append(100)
            LC_BD_return.append(0)
            
    # Corn Logic 
    
    j = 0
    
    prod = ['Corn Grain']
    coprods = ['Corn Stover']
    
    corn_return_list = []
    LC_corn_return = []
    
    for i in range(len(corn_yields)):
    
        results_array = UF.createEmptyFrame()
        
        yield_value = corn_yields[i] * 1000
    
        if yield_value != 0:
            biomass_IO = UF.Collect_IndepVars_Loop('CornCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
            results_array = results_array.append(biomass_IO, ignore_index=True)
            IO_array = UF.consolidateIO(results_array)
            
            corn_MBSP = TEA.calc_MBSP(IO_array, prod, coprods, 'Corn Grain EtOH')
            LC_corn = LifeCycleAssessment.LCAMetrics_cult(IO_array)
            
            corn_return_list.append(corn_MBSP.magnitude * 20)
            LC_corn_return.append(LC_corn[1])
            
            if i % 10 == 0:
                j += 1
                if j % 5 == 0 and j % 10 != 0:
                    print('...')
                if j == 49:
                    print('16% Completed')
                if j == 103:
                    print('33% Completed')
                if j == 154:
                    print('50% Completed')
                if j == 203:
                    print('66% Completed')
                if j == 256:
                    print('83% Completed')
                if j == 300:
                    print('99% Completed')
        else:
            corn_return_list.append(100)
            LC_corn_return.append(0)
        
    # return_list = list(zip(BD_return_list, LC_BD_return, corn_return_list, LC_corn_return))
        
    return_list = [BD_return_list,LC_BD_return,corn_return_list,LC_corn_return]
    return return_list