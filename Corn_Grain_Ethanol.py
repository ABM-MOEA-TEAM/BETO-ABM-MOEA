# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:52:28 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Corn_Grain_Cultivation as CGC

def ethanol_grain(biomass_IO_array):
    
    return_array = UF.createEmptyFrame()
    
    match_val = [[UF.input_or_output, D.tl_output],
                  [UF.substance_name,'Corn Grain']]
    
    corn_qty = UF.returnPintQty(biomass_IO_array, match_val)
     
    return_array.loc[0] = UF.getWriteRow('Corn Grain', D.conv,
                                      D.tl_input, 1*corn_qty)
    
    return_array.loc[1] = UF.getWriteRow('Sodium Hydroxide', D.conv,
                                      D.tl_input, 0.004971396*corn_qty)
    
    return_array.loc[2] = UF.getWriteRow('Lime', D.conv,
                                      D.tl_input, 0.001181735*corn_qty)
    
    return_array.loc[3] = UF.getWriteRow('Urea', D.conv,
                                      D.tl_input, 0.001977827*corn_qty)
    
    return_array.loc[4] = UF.getWriteRow('Alpha-Amylase', D.conv,
                                      D.tl_input, 0.000693479*corn_qty)
    
    return_array.loc[5] = UF.getWriteRow('Glucoamylase', D.conv,
                                      D.tl_input, 0.001001655*corn_qty)
    
    return_array.loc[6] = UF.getWriteRow('Sulfuric Acid', D.conv,
                                      D.tl_input, 0.001977827*corn_qty)
    
    return_array.loc[7] = UF.getWriteRow('Yeast', D.conv,
                                      D.tl_input, 0.000186876*corn_qty)
    
    return_array.loc[8] = UF.getWriteRow('Corn Beer', D.conv,
                                      D.tl_output, 3.511894562*corn_qty)
    
    scale1 = D.TEA_LCA_Qty('Capital Cost', 0.2066, 'dollars*yr/kg')
    return_array.loc[9] = UF.getWriteRow('Capital Cost', D.conv,
                                      D.tl_input, scale1.qty*corn_qty)
    return return_array


def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = CGC.grow_corn(land_area_val,yearly_precip)
    
    return ethanol_grain(biomass_IO_array)

if __name__ == "__main__":
    output = main()