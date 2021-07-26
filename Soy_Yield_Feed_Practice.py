# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 14:25:14 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF


import TEA
import pandas as pd

# import Soy_Cultivation as SC
# import Hexane_Extraction as HE
# import Transesterification as T

import os
from pathlib import Path

results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
biomass_yield = 1

results_array = UF.createEmptyFrame()
#ds_results_array = UF.createEmptyFrame()

cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv'),
              Path(cwd + '/output.xlsx')]

pathname = path_list[0]

# prod = ['Biodiesel, Produced']
# coprods = ['Soybean Meal','Glycerin']

prod = ['Jet-A']
coprods = ['LPG, Produced', 'Diesel, Produced', 
            'Gasoline, Produced']

DayCent_Yield_List = UF.DayCentYields('soy_yield_Mg_ha', 0)  

output_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [], 'MFSP ($/kg)' : []})

j = 0

for i in range(10):#range(len(DayCent_Yield_List)):
    
    results_array = UF.createEmptyFrame()
    
    yield_value = DayCent_Yield_List[i] * 1000 

    biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0)
    results_array = results_array.append(biomass_IO, ignore_index=True)
    conversion_IO = UF.Collect_IndepVars_Loop('HexExt', 0, 0, 1, biomass_IO,'Soybeans', 1, 0)
    results_array = results_array.append(conversion_IO, ignore_index=True)
    upgrading_IO = UF.Collect_IndepVars_Loop('HydroProc', 0, 0, 1, conversion_IO,'Soybean Oil', 2, 0)
    # upgrading_IO = UF.Collect_IndepVars_Loop('Transest', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0)
    results_array = results_array.append(upgrading_IO, ignore_index=True)
    IO_array = UF.consolidateIO(results_array)

    MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Biodiesel')
    
    append_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [yield_value], 
                                 'MFSP ($/kg)' : [MFSP.magnitude * 46]})

    output_frame = output_frame.append(append_frame, ignore_index = True)
    
    if i % 10 == 0:
        j += 1
        if j % 5 == 0 and j % 10 != 0:
            print('...')
        if j == 10:
            print('16% Completed')
        if j == 20:
            print('33% Completed')
        if j == 30:
            print('50% Completed')
        if j == 40:
            print('66% Completed')
        if j == 50:
            print('83% Completed')
        if j == 60:
            print('99% Completed')
            
# output_frame.to_excel(path_list[1])