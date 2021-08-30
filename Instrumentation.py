# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:02:53 2021

@author: Jack Smith
"""
import UnivFunc as UF
import TEA
import LifeCycleAssessment as L
import time

ol = ['']

def meta(runs):
    
    total = 0
    
    for i in range(runs):
        
        duration = execute()
        total += duration
    
    print('Total Execution Time: ', total,'seconds')
    print('Over',runs,'executions')
    print('Average runtime:')
    return total/runs


def execute():
    
    tic = time.perf_counter()
    
    results_array = UF.createEmptyFrame()
    
    prod = ['Ethanol']
    coprods = ['DDGS','Corn Stover']
    
    biomass_IO = UF.Collect_IndepVars_Loop('CornCult', 0, 0, 0, 0, 0, 0, 0, 0)
    results_array = results_array.append(biomass_IO, ignore_index=True)
    conversion_IO = UF.Collect_IndepVars_Loop('StarchFerm', 0, 0, 1, biomass_IO,'Corn Grain', 1, 0, 0)
    results_array = results_array.append(conversion_IO, ignore_index=True)

    
############################## PARTITION ##############################

    # biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', 0, 0, 0, 0, 0, 0, 0, 0)
    # results_array = results_array.append(biomass_IO, ignore_index=True)
    # conversion_IO = UF.Collect_IndepVars_Loop('HexExt', 0, 1, 1, biomass_IO, 'Soybeans', 1, 0, 0)
    # results_array = results_array.append(conversion_IO, ignore_index=True)
    # upgrading_IO = UF.Collect_IndepVars_Loop('HydroProc', 0, 1, 1, conversion_IO, 'Soybean Oil', 2, 0, 0)    
    # # upgrading_IO = UF.Collect_IndepVars_Loop('Transest', 0, 1, 1, conversion_IO, 'Soybean Oil', 2, 0, 0)
    # results_array = results_array.append(upgrading_IO, ignore_index=True)
    
    # prod = ['Biodiesel, Produced']
    # coprods = ['Soybean Meal','Glycerin']
    
    # prod = ['Jet-A']
    # coprods = ['LPG, Produced', 'Diesel, Produced', 'Gasoline, Produced']

############################## PARTITION ##############################

    IO_array = UF.consolidateIO(results_array)
    
    # LCAMetrics = L.LCAMetrics(IO_array)

    # MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Biodiesel', 9001, ol)
    # MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', 9001, ol)
    # MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Corn Grain EtOH', 9001, ol)
    
    toc = time.perf_counter()
    
    return toc - tic
    
    # return MFSP.magnitude * 26.95
    # return MFSP.magnitude * 37.75
    # return MFSP.magnitude * 46
    # return LCAMetrics

# land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
# yield_value = 3017  # Not actually used (need to remove - 6/24)

# biomass_IO = SC.grow_soybean(land_area_val, yield_value)

# output = TEA.calc_NPV(biomass_IO)

# output = UF.collectIndepVars('SoyCult')
# output = UF.DayCentFips()

# output = UF.External_Data('Practice Set (Python)')

#output = UF.collectEconIndepVars('Corn Grain EtOH')
# corn_stover_25 = UF.DayCentYields('stover_yield_Mg_ha', 1)
# corn_stover_50 = UF.DayCentYields('stover_yield_Mg_ha', 2)
# corn_stover_75 = UF.DayCentYields('stover_yield_Mg_ha', 3)

# corn_grain = UF.DayCentYields('corn_yield_Mg_ha', 0)

# soy_yield = UF.DayCentYields('soy_yield_Mg_ha', 0)