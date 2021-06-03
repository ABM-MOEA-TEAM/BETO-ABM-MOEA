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
                                      D.tl_output, (0.05329162*corn_beer_qty)
                                      +(0.001073185*corn_beer_qty))
                                      # 0.05329... is ratio of BM to ethanol out
                                      # divided by 4.727 (corn beer to BM)
                                      # second term is just gasoline denat. term
                                      
    ratio_total_burnable_BM = 0.461171
    total_burnable_BM = (ratio_total_burnable_BM/4.727)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Electricity'], total_burnable_BM*1.89863,'MJ/kg')
    
    results_array.loc[5] = UF.getWriteRow('Electricity', D.upgrading,
                                      D.tl_output, scale5.qty*corn_beer_qty) 
    
    # Humbird has 41 MW produced and 28 MW consumed - leaving 13 MW available
    # to be returned to the grid.  This ratio was used to determine the 
    # electricity produced from burning the lignin
    # 3326.61 MJ consumed, thus 4871.1 MJ produced
    
    results_array.loc[6] = UF.getWriteRow('Gasoline', D.upgrading, 
                                      D.tl_input, 0.001073185*corn_beer_qty)
    
    capex = D.TEA_LCA_Qty('Capital Cost', 4496.84, 'dollars') 
    # Total Capital Cost (Equip and Working Capital) divided by full prod rate
    # times the Gallons per ha produced.  The '1' above corresponds to the 
    # ratio of the plant to Humbirds' 61 MMGal/yr rate
    
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
