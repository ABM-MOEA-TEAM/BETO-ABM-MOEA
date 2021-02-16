# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:48:21 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF

import Corn_Grain_Cultivation as CGC
import Corn_Grain_Ethanol as CGE

def upgrade_grain_ethanol(biomass_IO_array):
    
    results_array = UF.createEmptyFrame()
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Corn Beer']]      
    
    corn_beer_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Electricity'],0.01666,'MJ/kg')
    
    results_array.loc[0] = UF.getWriteRow('Electricity', D.conv, 
                                      D.tl_input, scale1.qty*corn_beer_qty)
    results_array.loc[1] = UF.getWriteRow('Corn Beer', D.conv, 
                                      D.tl_input, corn_beer_qty)
    results_array.loc[3] = UF.getWriteRow('Water', D.conv, 
                                      D.tl_output, 0.798688*corn_beer_qty)
    results_array.loc[4] = UF.getWriteRow('Gasoline', D.conv,
                                      D.tl_input, 0.0050526*corn_beer_qty)
    results_array.loc[4] = UF.getWriteRow('Ethanol', D.conv, 
                                      D.tl_output, (0.0959998*corn_beer_qty)+(0.0050526*corn_beer_qty))
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Electricity'], 0.005, 'MJ/kg')
    
    results_array.loc[5] = UF.getWriteRow('Electricity', D.conv,
                                      D.tl_output, scale2.qty*corn_beer_qty)         # !! Placeholder - need to back out actual electricty
                                                                                # produced per kg of corn beer from burner.
    # results_array.loc[5] = UF.getWriteRow('Atmospheric CO2', D.conv,          # Must remember to be consistent with In/Out
    #                                   D.tl_output, 0.049379*corn_beer_qty)    # CO2 flows (count up front and end? not at all?)
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = CGC.grow_corn(land_area_val, yearly_precip)
    conversion_IO_array = CGE.ethanol_grain(biomass_IO_array)
    return upgrade_grain_ethanol(conversion_IO_array)

if __name__ == "__main__":
    output = main()
