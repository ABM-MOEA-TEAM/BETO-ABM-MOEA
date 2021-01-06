# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 15:40:59 2020

@author: jacks074
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Soy_Cultivation as SC

def diesel_soy(biomass_IO_array):
    
    results_array = UF.createEmptyFrame()
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Soybeans']]      # Grab the total amount of soybeans sent to plant
    
    soybean_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    results_array.loc[0] = UF.getWriteRow('Soybeans', D.conv, 
                                      D.tl_input, soybean_qty)
    results_array.loc[1] = UF.getWriteRow('Hexane Loss', D.conv, 
                                      D.tl_input, 0.00676*soybean_qty)
    results_array.loc[2] = UF.getWriteRow('Sodium Hydroxide', D.conv, 
                                      D.tl_input, 0.03429*soybean_qty)
    results_array.loc[3] = UF.getWriteRow('Phosphoric Acid (H3PO4)', D.conv, 
                                      D.tl_input, 0.00141*soybean_qty)
    results_array.loc[4] = UF.getWriteRow('Methanol', D.conv, 
                                      D.tl_input, 0.02596*soybean_qty)
    results_array.loc[5] = UF.getWriteRow('Steam', D.conv, 
                                      D.tl_input, 0.41301*soybean_qty)
    results_array.loc[6] = UF.getWriteRow('FAMEs and Glycerol', D.conv, 
                                      D.tl_output, 0.19424*soybean_qty)
    
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = SC.grow_soy(land_area_val, yearly_precip)
    
    return diesel_soy(biomass_IO_array)

if __name__ == "__main__":
    output = main()