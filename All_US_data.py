# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 01:17:20 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd

import TEA
import LifeCycleAssessment

import os
from pathlib import Path


cwd = os.getcwd()

path_list = [Path(cwd + '/readme_yields.xlsx')] # Presumably will all be in this file

excel_read = pd.read_excel(path_list[0])

corn_yields = []
soy_yields = []

for i in range(len(excel_read)):
    rows = excel_read.loc[i]
    corn_yields.append(rows['Corn'])
    soy_yields.append(rows['Soy'])
    
# Soy Logic for Biodiesel 

j = 0

ol = ['']

prod = ['Biodiesel, Produced']
coprods = ['Soybean Meal','Glycerin']

BD_return_list = []
LC_BD_return = []

for i in range(5):#len(soy_yields)):

    BD_results_array = UF.createEmptyFrame()    

    yield_value = soy_yields[i] * 1000
    
    if yield_value != 0:
        
        biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
        BD_results_array = BD_results_array.append(biomass_IO, ignore_index=True)
        conversion_IO = UF.Collect_IndepVars_Loop('HexExtSoy', 0, 1, 1, biomass_IO,'Soybeans', 1, 0, 0)
        BD_results_array = BD_results_array.append(conversion_IO, ignore_index=True)
        upgrading_IO = UF.Collect_IndepVars_Loop('Transest', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, 0)
        BD_results_array = BD_results_array.append(upgrading_IO, ignore_index=True)
        IO_array = UF.consolidateIO(BD_results_array)
        
        BD_MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Biodiesel', 1, ol)
        LC_BD = LifeCycleAssessment.LCAMetrics(IO_array, ol, 1)
        BD_return_list.append(BD_MFSP.magnitude * 37.75)
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
        BD_return_list.append(30)
        LC_BD_return.append(0)
        
# Soy Logic for Jet

# j = 0

# prod = ['Jet-A']
# coprods = ['LPG, Produced', 'Diesel, Produced', 
#             'Gasoline, Produced']

# jet_return_list = []
# LC_jet_return = []

# for i in range(len(soy_yields)):

#     jet_results_array = UF.createEmptyFrame()

#     yield_value = soy_yields[i] * 1000    
    
#     if yield_value != 0:
#         biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
#         jet_results_array = jet_results_array.append(biomass_IO, ignore_index=True)
#         conversion_IO = UF.Collect_IndepVars_Loop('HexExtSoy', 0, 1, 1, biomass_IO,'Soybeans', 1, 0, 0)
#         jet_results_array = jet_results_array.append(conversion_IO, ignore_index=True)
#         upgrading_IO = UF.Collect_IndepVars_Loop('HydroProc', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, 0)
#         jet_results_array = jet_results_array.append(upgrading_IO, ignore_index=True)
#         IO_array = UF.consolidateIO(jet_results_array)
        
#         jet_MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet')
#         LC_jet = LifeCycleAssessment.LCAMetrics(IO_array)
        
#         jet_return_list.append(jet_MFSP.magnitude * 46)
#         LC_jet_return.append(LC_jet[1])
        
#         if i % 10 == 0:
#             j += 1
#             if j % 5 == 0 and j % 10 != 0:
#                 print('...')
#             if j == 49:
#                 print('16% Completed')
#             if j == 103:
#                 print('33% Completed')
#             if j == 154:
#                 print('50% Completed')
#             if j == 203:
#                 print('66% Completed')
#             if j == 256:
#                 print('83% Completed')
#             if j == 300:
#                 print('99% Completed')
#     else:
#         jet_return_list.append(30)
#         LC_jet_return.append(0)
        
# # Corn Logic for Ethanol

# j = 0

# prod = ['Ethanol']
# coprods = ['DDGS','Corn Stover']

# corn_return_list = []
# LC_corn_return = []

# for i in range(len(corn_yields)):

#     results_array = UF.createEmptyFrame()
    
#     yield_value = corn_yields[i] * 1000

#     if yield_value != 0:
#         biomass_IO = UF.Collect_IndepVars_Loop('CornCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
#         results_array = results_array.append(biomass_IO, ignore_index=True)
#         conversion_IO = UF.Collect_IndepVars_Loop('StarchFerm', 0, 0, 1, biomass_IO,'Corn Grain', 1, 0, 0)
#         results_array = results_array.append(conversion_IO, ignore_index=True)
#         IO_array = UF.consolidateIO(results_array)
        
#         corn_MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Corn Grain EtOH')
#         LC_corn = LifeCycleAssessment.LCAMetrics(IO_array)
        
#         corn_return_list.append(corn_MFSP.magnitude * 26.95)
#         LC_corn_return.append(LC_corn[1])
        
#         if i % 10 == 0:
#             j += 1
#             if j % 5 == 0 and j % 10 != 0:
#                 print('...')
#             if j == 49:
#                 print('16% Completed')
#             if j == 103:
#                 print('33% Completed')
#             if j == 154:
#                 print('50% Completed')
#             if j == 203:
#                 print('66% Completed')
#             if j == 256:
#                 print('83% Completed')
#             if j == 300:
#                 print('99% Completed')
#     else:
#         corn_return_list.append(25)
#         LC_corn_return.append(0)