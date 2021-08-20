# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 10:06:23 2021

@author: Jack Smith
"""

# Algae Cultivation and Processing PM

import LifeCycleAssessment as L
import TEA
import TEA_LCA_Data as D
import UnivFunc as UF

import pandas as pd
import os
from pathlib import Path

prod = ['Algal Biomass, Whole']
coprods = ['']

results_array = UF.createEmptyFrame()

biomass_IO = UF.Collect_IndepVars_Loop('AlgaeCult', 0, 0, 0, 0, 0, 0, 0, 0)
results_array.append(biomass_IO)

IO_array = UF.consolidateIO(results_array)

MBSP = TEA.calc_MBSP(biomass_IO, prod, coprods, 'Algae HEFA', 1001)
cult_LCA = L.LCAMetrics_cult(biomass_IO)