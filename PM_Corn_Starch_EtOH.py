# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:18:14 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd
import MonteCarloEx as MCE


import TEA
import LifeCycleAssessment

import os
from pathlib import Path

cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv'),
              Path(cwd + '/output.xlsx')]

# DayCent_Yield_List = UF.DayCentYields('corn_yield_Mg_ha', 0)  

prod = ['Ethanol']
coprods = ['DDGS','Corn Stover']

# ol = ['SolarPV Utility Electricity Cost ($/MJ)', 'Arable Land Value ($/ha)']
# ol = ['SolarPV Utility Electricity Cost ($/MJ)']
# ol = ['Arable Land Value ($/ha)']
ol = ['']

output_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [], 'MFSP ($/kg)' : []})

j = 0
    
results_array = UF.createEmptyFrame()

# yield_value = DayCent_Yield_List[i]*1000
# yield_value = 15000 #10974
  
# yield_values_list = MCE.MonteCarloEx('Normal', 10974, 3000, 1000, 0, 0)
# output_obj = []

# for i in range(1000):
    
    # results_array = UF.createEmptyFrame()
    
    # yield_value = yield_values_list[i]
    
# biomass_IO = UF.Collect_IndepVars_Loop('CornCult', yield_value, 1, 0, 0, 0, 0, 0, 0)
biomass_IO = UF.Collect_IndepVars_Loop('CornCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array = results_array.append(biomass_IO, ignore_index=True)
conversion_IO = UF.Collect_IndepVars_Loop('StarchFerm', 0, 0, 1, biomass_IO,'Corn Grain', 1, 0, 0)
results_array = results_array.append(conversion_IO, ignore_index=True)

IO_array = UF.consolidateIO(results_array)

# NPV = TEA.calc_NPV(IO_array, prod, coprods, 'Corn Grain EtOH', 9001, ol)

MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Corn Grain EtOH', 1003, ol) 
LCAs = LifeCycleAssessment.LCAMetrics(IO_array, ol, 1)
    
print(MFSP.magnitude * 26.95)   
print(LCAs)
    
    # print('and')
    
    # prod = ['Corn Grain']
    # coprods = ['Corn Stover']

    # append_obj = [[MFSP.magnitude*26.95],[yield_value]]
    # output_obj.append(append_obj)
    # output_obj.append(LCAs[1])    
    # coprods = ['']
    
    # MBSP = TEA.calc_MBSP(biomass_IO, prod, coprods, 'Corn Grain EtOH', 1, ol)
    # print(MBSP.magnitude * 20)  # Assumed HHV for Corn Grain
    
    # MBSP is produced by loop to be of unit $/MJ
    # So we scale by MJ/kg (MJ/kg * $/MJ = $/kg)
    
    #     append_frame = pd.DataFrame({'DayCent Yields (kg/ha)' : [yield_value], 
    #                                  'MFSP ($/kg)' : [MFSP.magnitude * 26.95]})
    
    #     output_frame = output_frame.append(append_frame, ignore_index = True)
        
    # if i % 10 == 0:
    #         j += 1
    # if j == 1:
    #     print('10% complete')
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


