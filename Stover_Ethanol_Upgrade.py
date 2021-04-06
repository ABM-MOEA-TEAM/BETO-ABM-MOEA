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
                 [UF.substance_name, 'Corn Beer']]  
    
    corn_beer_qty = UF.returnPintQty(biomass_IO_array, match_list)
    # 26295.56 kg Corn Beer/ha-yr
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Electricity'],0.01666,'MJ/kg')
    results_array.loc[0] = UF.getWriteRow('Electricity', D.upgrading, 
                                      D.tl_input, scale1.qty*corn_beer_qty)
    
    results_array.loc[1] = UF.getWriteRow('Corn Beer', D.upgrading, 
                                      D.tl_input, corn_beer_qty)
    results_array.loc[3] = UF.getWriteRow('Water', D.upgrading, 
                                      D.tl_output, 0.798688*corn_beer_qty)
    results_array.loc[4] = UF.getWriteRow('Ethanol', D.upgrading, 
                                      D.tl_output, 0.054367*corn_beer_qty)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Electricity'], 0.185244,'MJ/kg')
    results_array.loc[5] = UF.getWriteRow('Electricity', D.upgrading,
                                      D.tl_output, scale5.qty*corn_beer_qty) 
    
    # Humbird has 41 MW produced and 28 MW consumed - leaving 13 MW available
    # to be returned to the grid.  This ratio was used to determine the 
    # electricity produced from burning the lignin
    # 3326.61 MJ consumed, thus 4871.1 MJ produced
    
    results_array.loc[6] = UF.getWriteRow('Gasoline', D.upgrading, 
                                      D.tl_input, 0.001073185*corn_beer_qty)
    
    capex = D.TEA_LCA_Qty('Capital Cost', 2758*(1**0.6), 'dollars') 
    # 3355 Corresponds to TCI/ha's_reqd, and the 1 corresponds to the economies
    # of scale. "1" is a placeholder for the ratio of plant throughput to Humbird
    
    results_array.loc[7] = UF.getWriteRow('Capital Cost', D.upgrading, 
                                      D.tl_input, capex.qty)
                                                                                # !! Placeholder - need to back out actual electricty
                                                                                # produced per kg of corn beer from burner.
    # results_array.loc[5] = UF.getWriteRow('Atmospheric CO2', D.conv,          # Must remember to be consistent with In/Out
    #                                   D.tl_output, 0.049379*corn_beer_qty)    # CO2 flows (count up front and end? not at all?)
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yield_value = 5563.08
    biomass_IO_array = CSC.grow_stover(land_area_val, yield_value)
    conversion_IO_array = CSE.ethanol_stover(biomass_IO_array)
    return upgrade_stover_ethanol(conversion_IO_array)

if __name__ == "__main__":
    output = main()
