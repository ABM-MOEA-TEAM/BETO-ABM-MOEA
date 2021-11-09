# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:37:41 2021

@author: Jack Smith
"""

# Soy Checking Sheet

import UnivFunc as UF
import pandas as pd
import numpy as np
import time

import TEA
import LifeCycleAssessment as L

import os
from pathlib import Path

toc = time.perf_counter()

# Create PDF -

pdf = np.random.normal(1,0.25,10000)

ol = ['']

cwd = os.getcwd()

path_list = [Path(cwd + '/readme_yields.xlsx')] # Presumably will all be in this file

excel_read = pd.read_excel(path_list[0])

jet_mfsps = []
fips_list = []
soy_yields = []
pdf_modifier_list = []
used_yield_list = []
fips = []

prod = ['Jet-A']
coprods = ['LPG, Produced', 'Diesel, Produced', 
            'Gasoline, Produced']

for i in range(len(excel_read)):
    rows = excel_read.loc[i]
    fips.append(rows['FIPS'])
    soy_yields.append(rows['Soy'])

for i in range(len(soy_yields)):
    
    for j in range(50):
        
        used_yield = 0
        MFSP = 0
        modifier = 0
        yield_value = soy_yields[i]*1000
        results_array = UF.createEmptyFrame()
        
        if yield_value != 0:
            modifier = np.random.choice(pdf)
            
            used_yield = yield_value * modifier
            
            biomass_IO = UF.Collect_IndepVars_Loop('SoyCult', used_yield, 1, 0, 0, 0, 0, 0, 0)
            results_array = results_array.append(biomass_IO, ignore_index=True)
            conversion_IO = UF.Collect_IndepVars_Loop('HexExtSoy', 0, 1, 1, biomass_IO,'Soybeans', 1, 0, 0)
            results_array = results_array.append(conversion_IO, ignore_index=True)
            upgrading_IO = UF.Collect_IndepVars_Loop('HydroProcOil', 0, 1, 1, conversion_IO,'Soybean Oil', 2, 0, 0)
            results_array = results_array.append(upgrading_IO, ignore_index=True)
            IO_array = UF.consolidateIO(results_array)
            
            MFSP = TEA.calc_MFSP(IO_array, prod, coprods, 'Soy Jet', 1, ol)
            
            tic = time.perf_counter()
            # print(i, j)
            # print(used_yield, yield_value)
            # print(tic - toc, 'Seconds Elapsed')
            # print(MFSP.magnitude * 46)
            # print(LCAs)
        
        fips_list.append(fips[i])
        pdf_modifier_list.append(modifier)
        used_yield_list.append(used_yield)
        if type(MFSP) == int:
            jet_mfsps.append(MFSP)
        else:
            jet_mfsps.append(MFSP.magnitude*133)
        
        if i == 10:
            print('...')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 494:
            print('16% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 1017:
            print('33% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 1541:
            print('50% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 2055:
            print('66% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 2560:
            print('83% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        if i == 3000:
            print('95% Completed')
            tic = time.perf_counter()
            print(tic-toc, 'seconds elapsed')
        
        
