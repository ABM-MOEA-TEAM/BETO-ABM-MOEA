# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:29:30 2021

@author: Jack Smith
"""

import UnivFunc as UF
import time

import TEA
import LifeCycleAssessment as L

tic = time.perf_counter()

results_array = UF.createEmptyFrame()

ol = ['']

results_array = UF.createEmptyFrame()

biomass_IO = UF.Collect_IndepVars_Loop('MiscCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array = results_array.append(biomass_IO, ignore_index = True)
conversion_IO = UF.Collect_IndepVars_Loop('GasFT', 0, 0, 1, biomass_IO, 'Miscanthus', 1, 0, 0)
results_array = results_array.append(conversion_IO, ignore_index = True)
upgrading_IO = UF.Collect_IndepVars_Loop('HydroProcSyn', 0, 0, 1, conversion_IO, 'Syncrude', 2, 0, 0)
results_array = results_array.append(upgrading_IO, ignore_index=True)
IO_array = UF.consolidateIO(results_array)

prod = ['Jet-A']
coprods = ['Diesel, Produced', 
            'Gasoline, Produced']

MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', 1, ol)
LCAs = L.LCAMetrics(IO_array, ol, 1)

print(MFSP.magnitude * 46)
print(LCAs)

toc = time.perf_counter()
print(toc-tic, 'seconds')