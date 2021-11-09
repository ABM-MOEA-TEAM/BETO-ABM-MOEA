# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 16:59:39 2021

@author: Jack Smith
"""

from multiprocessing import Pool
import numpy as np
import All_US_data as AUD
import time


# def waitplease():
#     toc = time.perf_counter()
#     time.sleep(2)
#     return_obj = np.random.randint(0,100)
#     tic = time.perf_counter()
#     print(tic-toc,'seconds')
#     return return_obj

def linear():
    toc = time.perf_counter()
    list_out = []
    for i in range(3):
        list_out.append(np.random.randint(0,100))
    tic = time.perf_counter()
    print(tic-toc, 'seconds')
    return list_out

def my_random(dummy_variable):
    toc = time.perf_counter()
    time.sleep(1)
    tic = time.perf_counter()
    print(tic-toc, 'seconds')
    return np.random.rand(1)[0]

def my_random_parallel(number_of_elements):
    
    my_pool = Pool(2)
    my_random_array = my_pool.map(my_random, range(1, number_of_elements+1))  
    my_random_array = np.array(my_random_array)
    return_obj = my_random_array
    
    return return_obj

number_of_elements_selected = 3

if __name__ == '__main__':
    toc = time.perf_counter()
    my_random_array_generated = my_random_parallel(number_of_elements_selected)
    tic = time.perf_counter()
    print(tic-toc, 'seconds')