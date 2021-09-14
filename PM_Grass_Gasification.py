# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 11:00:52 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd

import TEA
import LifeCycleAssessment as L

# import Soy_Cultivation as SC
# import Hexane_Extraction as HE
# import Transesterification as T

import os
from pathlib import Path

results_array = UF.createEmptyFrame()

ol = ['']

results_array = UF.createEmptyFrame()

biomass_IO = UF.Collect_IndepVars_Loop('GrassCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array = results_array.append(biomass_IO, ignore_index = True)
conversion_IO = UF.Collect_IndepVars_Loop('GasFT', 0, 0, 1, biomass_IO, 'Woody Biomass', 1, 0, 0)
results_array = results_array.append(conversion_IO, ignore_index = True)
upgrading_IO = UF.Collect_IndepVars_Loop('HydroProc', 0, 0, 1, conversion_IO, 'Syncrude', 2, 0, 0)
results_array = results_array.append(upgrading_IO, ignore_index=True)
IO_array = UF.consolidateIO(results_array)

prod = ['Jet-A']
coprods = ['LPG, Produced', 'Diesel, Produced', 
            'Gasoline, Produced']

# MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', 1, ol)
# LCAs = L.LCAMetrics(IO_array, ol, 1)

# print(MFSP.magnitude * 37.75)
# print(MFSP.magnitude * 46)
# print(LCAs)
