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
    
    
    results_array.loc[0] = UF.getWriteRow('FAMEs and Glycerol', D.upgrading, 
                                      D.tl_input, FAME_qty)
    
    glycerol_yield = 0.003455039
    results_array.loc[1] = UF.getWriteRow('Glycerol', D.upgrading, 
                                      D.tl_output, (glycerol_yield/0.19424)*FAME_qty)
    results_array.loc[2] = UF.getWriteRow('Methanol', D.upgrading, 
                                      D.tl_output, 0.0070434*FAME_qty)
    
    biodiesel_yield = 0.169296933
    results_array.loc[3] = UF.getWriteRow('Biodiesel', D.upgrading, 
                                      D.tl_output, (biodiesel_yield/0.19424)*FAME_qty)
        
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Electricity'],5.5166,'MJ/kg')
    results_array.loc[4] = UF.getWriteRow('Electricity', D.upgrading, 
                                      D.tl_input, scale1.qty*FAME_qty)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], (451.61/718.3),'dollars*yrs/kg') 
    results_array.loc[5] = UF.getWriteRow('Capital Cost', D.upgrading,
                                      D.tl_input, scale3.qty*FAME_qty)
    
    return results_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yield_value = 3698
    biomass_IO_array = SC.grow_soy(land_area_val,yield_value)
    conversion_IO_array = SD.diesel_soy(biomass_IO_array)
    return upgrade_soy_diesel(conversion_IO_array)

if __name__ == "__main__":
    output = main()