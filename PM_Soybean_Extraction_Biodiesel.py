# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:48:27 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd
import numpy as np
import time

import TEA
import LifeCycleAssessment as L

import os
from pathlib import Path

toc = time.perf_counter()

results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
biomass_yield = 1

# ol = ['']

fip = 1001
ol = ['Arable Land Value ($/ha)', 'Grid Electricity Price ($/MJ)', 'Grid Electricity GHG (g/MJ)']
# ol = ['Arable Land Value ($/ha)']
# ol = ['Grid Electricity Price ($/MJ)']

results_array = UF.createEmptyFrame()
#ds_results_array = UF.createEmptyFrame()

yield_value = 3017.1329604

#UF.Collect_IndepVars_Loop(tab_string, yield_value, geospatial_indicator, 
#downstream_indicator, tl_array, input_substance_string, step_ID, DayCent_read_string, fips)

biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0, fip)
# biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array = results_array.append(biomass_IO, ignore_index=True)
conversion_IO = UF.Collect_IndepVars_Loop('HexExtSoy', 0, 1, 1, biomass_IO,'Soybeans', 1, 0, fip)
results_array = results_array.append(conversion_IO, ignore_index=True)
# upgrading_IO = UF.Collect_IndepVars_Loop('Transest', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, 0)
upgrading_IO = UF.Collect_IndepVars_Loop('HydroProcOil', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, fip)
results_array = results_array.append(upgrading_IO, ignore_index=True)
IO_array = UF.consolidateIO(results_array)

cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv'),
              Path(cwd + '/output.xlsx')]

pathname = path_list[0]

# prod = UF.returnProdlist(pathname)
# coprods = UF.returnCoProdlist(pathname)

# prod = ['Biodiesel, Produced']
# coprods = ['Soybean Meal','Glycerin']

prod = ['Jet-A']
coprods = ['LPG, Produced', 'Diesel, Produced', 
            'Gasoline, Produced']

# NPV = TEA.calc_NPV(IO_array, prod, coprods, 'Soy Biodiesel', 9001, ol)

MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Biodiesel', fip, ol)
MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', fip, ol)

# MFSP = TEA.quick_MFSP(IO_array, prod, coprods, 'Soy Jet', 1, ol)

LCAs = L.LCAMetrics(IO_array, ol, fip)

# print(MFSP.magnitude * 37.75)
print(MFSP.magnitude * 46)
print(LCAs)


#Output_NPV_Value = TEA.calc_NPV(IO_array, prod, coprods, 'Soy Biodiesel')

# IO_array.to_excel(path_list[1])

# ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)

# NPV_Biomass = TEA.calc_NPV(biomass_IO)
# NPV_Conversion = TEA.calc_NPV(conversion_IO)  #5.46680706628588
# NPV_Upgrading = TEA.calc_NPV(upgrading_IO)

# Biomass_Conversion_array = UF.createEmptyFrame()
# Conversion_Upgrading_array = UF.createEmptyFrame()

# Biomass_Conversion_array = Biomass_Conversion_array.append(biomass_IO, ignore_index=True)
# Biomass_Conversion_array = Biomass_Conversion_array.append(conversion_IO, ignore_index=True)

# Conversion_Upgrading_array = Conversion_Upgrading_array.append(conversion_IO, ignore_index=True)
# Conversion_Upgrading_array = Conversion_Upgrading_array.append(upgrading_IO, ignore_index=True)

# NPV_BC_Consolidated = UF.consolidateIO(Biomass_Conversion_array)
# NPV_CU_Consolidated = UF.consolidateIO(Conversion_Upgrading_array)

# NPV_Biomass_Conversion = TEA.calc_NPV(NPV_BC_Consolidated)
# NPV_Conversion_Upgrading = TEA.calc_NPV(NPV_CU_Consolidated)

# DayCent_Yield_List = UF.DayCentYields('soy_yield_Mg_ha', 0)  


