# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 07:51:35 2021

@author: Jack Smith
"""

import pandas as pd
# import PM_Corn_Starch_EtOH as PM_CE
import numpy as np
import matplotlib.pyplot as plt

def PlotDistr(data, binnum):
    
    plt.hist(data, bins = binnum)
    plt.show()

    return

def MonteCarloEx(distr_type, mean, std_dev, n, low, high):
    return_obj = 0
    
    if distr_type == 'Normal':
        print('Building Normal Distribution')
        print('Using', mean, 'as mean value')
        print('Using', std_dev, 'as distribution standard deviation')
        print('Populating', n, 'samples')
        print('Not using -low- or -high- ;' , low, high)
        return_obj = np.random.normal(mean, std_dev, n)
    if distr_type == 'Uniform':
        print('Building Uniform Distribution')
        print('Using', low, 'as lower bound of distribution')
        print('Using', high, 'as upper bound of distribution')
        print('Populating', n, 'samples')
        print('Not using -mean-, -std_dev- ;', mean, std_dev)
        return_obj = np.random.uniform(low, high, n)
    if (distr_type != 'Normal' and distr_type != 'Uniform'):
        print('Unrecognized Distribution type, expected')
        print('Normal')
        print('Uniform')
    
    return return_obj
