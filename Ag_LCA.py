# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 03:08:47 2021

@author: Jack Smith
"""
# This module provides the GWP of a specific crop at the farm gate
# it is simply the "calcGHG" loop from the LCA.py file

import TEA_LCA_Data as D
import UnivFunc as UF

# Calculate GHG Impact by energy allocation (reminder--need to add calculations 
# for allocation by mass, economic allocation, as well as system expansion displacement credits)
def calcGHGImpactAg(tl_array):
    
    corn_grain_out = 0
    corn_stover_out = 0
    switchgrass_out = 0
    soybean_out = 0
    mass_allocation_ratio = 1
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        in_or_out = row_vals[UF.input_or_output]
        subst_name = row_vals[UF.substance_name]
        
        if 'Woody Biomass' in subst_name and in_or_out == D.tl_output:
            switchgrass_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Woody Biomass'],    
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Corn Grain' in subst_name and in_or_out == D.tl_output:
            corn_grain_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Grain'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
            
        if 'Soybeans' in subst_name and in_or_out == D.tl_output:
            soybean_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Soybeans'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Corn Stover Collected' in subst_name and in_or_out == D.tl_output:
            corn_stover_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Stover Collected'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    
    total_kg = switchgrass_out + corn_grain_out + corn_stover_out + soybean_out 

    if corn_stover_out != 0 and corn_grain_out != 0: # I think this conditional has to follow "total_kg" assignment
        total_kg = corn_stover_out
        print('Allocation Performed')
        mass_allocation_ratio = (corn_stover_out / (corn_stover_out + corn_grain_out))    
    
    GHG_impact = 0
    
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
                                      D.LCA_GHG_impact)
            GHG_impact += (LCA_val * mag)
   
    GHG_impact_kg = (GHG_impact * mass_allocation_ratio)/total_kg
    
    return GHG_impact_kg
   