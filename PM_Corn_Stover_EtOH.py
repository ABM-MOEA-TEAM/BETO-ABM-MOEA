# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 12:28:06 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
# import pandas as pd

import TEA
# import LCA

# import os
# from pathlib import Path

results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
biomass_yield = 1

results_array = UF.createEmptyFrame()
#ds_results_array = UF.createEmptyFrame()

DayCent_Yield_List = UF.DayCentYields('corn_yield_Mg_ha', 0)  
DayCent_Fips_List = UF.DayCentFips()

current_fip = DayCent_Fips_List[15]

biomass_IO = UF.Collect_IndepVars_Loop('CornCult', 0, 0, 0, 0, 0, 0, 0, current_fip)
results_array = results_array.append(biomass_IO, ignore_index=True)
# conversion_IO = UF.Collect_IndepVars_Loop('StarchFerm', 0, 1, 1, biomass_IO,'Corn Grain', 1, 0, 0)
# results_array = results_array.append(conversion_IO, ignore_index=True)

IO_array = UF.consolidateIO(results_array)


# prod = ['Ethanol']
# coprods = ['DDGS','Corn Stover']

# # NPV = TEA.calc_NPV(IO_array, prod, coprods, 'Corn Grain EtOH')

# MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Corn Grain EtOH')





