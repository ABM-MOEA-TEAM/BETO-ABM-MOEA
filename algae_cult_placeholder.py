# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:06:48 2021

@author: jacks074
"""

# Placeholder algae "growth" loop

import TEA_LCA_Data as D
import UnivFunc as UF

def grow_algae(land_area_val):
    
    size = land_area_val
    
    return_array = UF.createEmptyFrame()    
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Algae AFDW'], 55792, 'kg/ha/yr') 
       
                    # Just using the daily mass flow of the plant until we 
                    # decide what to scale this off of (ha's of algae probably
                    # doesn't make sense, hm?)
    
    return_array.loc[0] = UF.getWriteRow('Algae AFDW', D.biomass_production, 
                                      D.tl_output, scale1.qty*size.qty)
    
    return return_array


def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    return grow_algae(land_area_val)

if __name__ == "__main__":
    output = main()