# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 17:03:23 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

import Corn_Stover_Cultivation as CSC
import Corn_Stover_Ethanol as CSE

def upgrade_stover_ethanol(biomass_IO_array):
    
    results_array = UF.createEmptyFrame()
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Corn Beer']]      # Grab the total amount of soybeans sent to plant
    
    corn_beer_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Electricity'],0.01666,'MJ/kg')
    
    results_array.loc[0] = UF.getWriteRow('Electricity', D.upgrading, 
                                      D.tl_input, scale1.qty*corn_beer_qty)
    results_array.loc[1] = UF.getWriteRow('Corn Beer', D.upgrading, 
                                      D.tl_input, corn_beer_qty)
    results_array.loc[3] = UF.getWriteRow('Water', D.upgrading, 
                                      D.tl_output, 0.798688*corn_beer_qty)
    results_array.loc[4] = UF.getWriteRow('Ethanol', D.upgrading, 
                                      D.tl_output, 0.053663*corn_beer_qty)
    results_array.loc[5] = UF.getWriteRow('Electricity', D.upgrading,
                                      D.tl_output, 0.005*corn_beer_qty)  
    
    capex = D.TEA_LCA_Qty('Capital Cost', 3355.11, 'dollars')                   # Corresponds to TCI/ha's_reqd
    
    results_array.loc[6] = UF.getWriteRow('Capital Cost', D.upgrading, 
                                      D.tl_input, capex.qty)
                                                                                # !! Placeholder - need to back out actual electricty
                                                                                # produced per kg of corn beer from burner.
    # results_array.loc[5] = UF.getWriteRow('Atmospheric CO2', D.conv,          # Must remember to be consistent with In/Out
    #                                   D.tl_output, 0.049379*corn_beer_qty)    # CO2 flows (count up front and end? not at all?)
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = CSC.grow_stover(land_area_val, yearly_precip)
    conversion_IO_array = CSE.ethanol_stover(biomass_IO_array)
    return upgrade_stover_ethanol(conversion_IO_array)

if __name__ == "__main__":
    output = main()
