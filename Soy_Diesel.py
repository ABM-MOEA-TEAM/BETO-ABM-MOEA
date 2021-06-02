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
    
    # Depending on the feedstock type, if statements filter the scaling values
    # (Chance to stop a nonsensical extraction ask - i.e. corn "extraction")
    
    results_array.loc[0] = UF.getWriteRow('Soybeans', D.conv, 
                                      D.tl_input, 1*soybean_qty)
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
    results_array.loc[7] = UF.getWriteRow('Soybean Meal', D.conv,
                                      D.tl_output, 0.73261*soybean_qty)
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['LNG'],0.2258,'MJ/kg')
    results_array.loc[8] = UF.getWriteRow('LNG', D.conv,
                                      D.tl_input, soybean_qty*scale1.qty)
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 0.0000001, 'dollars')
    results_array.loc[9] = UF.getWriteRow('Land Capital Cost', D.conv,
                                      D.tl_input, scale2.qty)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 0.000001, 'dollars/yr')
    results_array.loc[10] = UF.getWriteRow('Labor', D.conv,
                                      D.tl_input, scale3.qty)
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yield_value = 3698
    biomass_IO_array = SC.grow_soy(land_area_val, yield_value)
    
    return diesel_soy(biomass_IO_array)

if __name__ == "__main__":
    output = main()