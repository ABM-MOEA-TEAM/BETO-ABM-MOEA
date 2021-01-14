# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:40:09 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Soy_Cultivation as SC
import Soy_Diesel as SD

def upgrade_soy_diesel(biomass_IO_array):
    
    results_array = UF.createEmptyFrame()
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'FAMEs and Glycerol']]      # Grab the total amount of soybeans sent to plant
    
    FAME_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Electricity'],0.56852,'MJ/kg')
    
    results_array.loc[0] = UF.getWriteRow('Electricity', D.conv, 
                                      D.tl_input, scale1.qty*FAME_qty)
    results_array.loc[1] = UF.getWriteRow('FAMEs and Glycerol', D.conv, 
                                      D.tl_input, FAME_qty)
    results_array.loc[2] = UF.getWriteRow('Glycerol', D.conv, 
                                      D.tl_output, 0.01779*FAME_qty)
    results_array.loc[3] = UF.getWriteRow('Methanol', D.conv, 
                                      D.tl_output, 0.05139*FAME_qty)
    results_array.loc[4] = UF.getWriteRow('Biodiesel', D.conv, 
                                      D.tl_output, 0.87163*FAME_qty)
    results_array.loc[5] = UF.getWriteRow('Electricity', D.conv,
                                      D.tl_output, 0.000001*FAME_qty)
    
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = SC.grow_soy(land_area_val, yearly_precip)
    conversion_IO_array = SD.diesel_soy(biomass_IO_array)
    return upgrade_soy_diesel(conversion_IO_array)

if __name__ == "__main__":
    output = main()