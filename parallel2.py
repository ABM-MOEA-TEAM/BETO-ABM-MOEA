# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 15:28:02 2021

@author: Jack Smith
"""

from multiprocessing import Pool
import os
from pathlib import Path
import pandas as pd
import time
import All_US_data as AUD
import numpy as np


def do_something(x):
    
    # time.sleep(1)
    return x*x
    

if __name__ == '__main__':
    
    toc = time.perf_counter()

    cwd = os.getcwd()
    path_list = [Path(cwd + '/readme_yields.xlsx')] # Presumably will all be in this file
    excel_read = pd.read_excel(path_list[0])
    
    corn_yields = []
    fips_list = []
    input_obj = []
        
    for i in range(len(excel_read)):
        rows = excel_read.loc[i]
        corn_yields.append(rows['Corn'])
        # soy_yields.append(rows['Soy'])
        fips_list.append(rows['FIPS'])
    
    for i in range(len(corn_yields)):
        for j in range(100):
            input_obj.append([corn_yields[i],fips_list[i]])
    # input_obj = [0,1,2,3,4,5]
    # print(input_obj)
    
    with Pool() as p:
        output = p.map(AUD.doit, input_obj)
    
    tic = time.perf_counter()
    print(tic-toc, 'seconds elapsed')
