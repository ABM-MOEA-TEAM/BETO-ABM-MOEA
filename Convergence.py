# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 17:56:36 2022

@author: Jack Smith
"""

# Convergence Test

import UnivFunc as UF
import time

import TEA
import LifeCycleAssessment as L

import numpy as np

pdf = np.random.normal(1,0.3,100000)

def TestConvergence(runs):
    
    toc = time.perf_counter()
    return_obj = 0
    
    mfsp = []
    ghgs = []
    mods = []
    
    for i in range(runs):
        
        results_array = UF.createEmptyFrame()
        
        fip = 1001
        ol = ['Arable Land Value ($/ha)', 'Grid Electricity Price ($/MJ)', 'Grid Electricity GHG (g/MJ)']
        
        results_array = UF.createEmptyFrame()
        
        yield_value = 3017.1329604
        
        modifier = np.random.choice(pdf)
        
        yield_value = yield_value * modifier
        
        biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', yield_value, 1, 0, 0, 0, 0, 0, fip)
        results_array = results_array.append(biomass_IO, ignore_index=True)
        conversion_IO = UF.Collect_IndepVars_Loop('HexExtSoy', 0, 1, 1, biomass_IO,'Soybeans', 1, 0, fip)
        results_array = results_array.append(conversion_IO, ignore_index=True)
        upgrading_IO = UF.Collect_IndepVars_Loop('HydroProcOil', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, fip)
        results_array = results_array.append(upgrading_IO, ignore_index=True)
        IO_array = UF.consolidateIO(results_array)
        
        
        prod = ['Jet-A']
        coprods = ['LPG, Produced', 'Diesel, Produced', 
                    'Gasoline, Produced']
        
        
        MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', fip, ol)
        LCAs = L.LCAMetrics(IO_array, ol, fip)
        
        # Clobber past run results
        biomass_IO = 0
        conversion_IO = 0
        upgrading_IO = 0
        results_array = 0
        IO_array = 0
        
        if i % 100 == 0:
            print('...')
        
        mfsp.append(MFSP.magnitude)
        ghgs.append(LCAs[1])
        mods.append(modifier)
        
    return_obj = [[],[],[]]
    return_obj = [mfsp, ghgs,mods]
    tic = time.perf_counter()
    print(tic-toc, 'seconds elapsed')
    
    return return_obj

