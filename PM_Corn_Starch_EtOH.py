# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:18:14 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd

import TEA
# import LCA

import os
from pathlib import Path

cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv'),
              Path(cwd + '/output.xlsx')]

# DayCent_Yield_List = UF.DayCentYields('corn_yield_Mg_ha', 0)  

prod = ['Ethanol']
coprods = ['DDGS','Corn Stover']

output_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [], 'MFSP ($/kg)' : []})

j = 0

# for i in range(len(DayCent_Yield_List)):
    
results_array = UF.createEmptyFrame()

# yield_value = DayCent_Yield_List[i]*1000

# biomass_IO = UF.Collect_IndepVars_Loop('CornCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
biomass_IO = UF.Collect_IndepVars_Loop('CornCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array = results_array.append(biomass_IO, ignore_index=True)
conversion_IO = UF.Collect_IndepVars_Loop('StarchFerm', 0, 0, 1, biomass_IO,'Corn Grain', 1, 0, 0)
results_array = results_array.append(conversion_IO, ignore_index=True)

IO_array = UF.consolidateIO(results_array)

# NPV = TEA.calc_NPV(IO_array, prod, coprods, 'Corn Grain EtOH')

MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Corn Grain EtOH')
    
#     append_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [yield_value], 
#                                  'MFSP ($/kg)' : [MFSP.magnitude * 26.95]})

#     output_frame = output_frame.append(append_frame, ignore_index = True)
    
#     if i % 10 == 0:
#         j += 1
#         if j % 5 == 0 and j % 10 != 0:
#             print('...')
#         if j == 10:
#             print('16% Completed')
#         if j == 20:
#             print('33% Completed')
#         if j == 30:
#             print('50% Completed')
#         if j == 40:
#             print('66% Completed')
#         if j == 50:
#             print('83% Completed')
#         if j == 60:
#             print('99% Completed')
            
# output_frame.to_excel(path_list[1])


