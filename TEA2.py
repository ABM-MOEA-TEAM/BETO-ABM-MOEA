# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:06:08 2021

@author: Jack Smith
"""

import scipy.optimize as s_opt
import TEA_LCA_Data as D
import UnivFunc as UF

#   Attempt to regenerate TEA module so that I understand it

#   Primary function of the TEA script is to produce the minimum fuel selling price. min crop SP?

def calcOPEX(tl_array):
    inputs_cost = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost)
            if in_or_out == D.tl_input:
                inputs_cost += (LCA_val * mag)
   
    return inputs_cost

def NPV_goalcal():
    return

def calc_MFSP():

    MFSP = -9001
    print('Executed')

    price_per_MJ = 0.50
    NPV_goal = 0.85

    MFSP = s_opt.minimize_scalar(lambda price_per_MJ: NPV_goal)

    return MFSP

