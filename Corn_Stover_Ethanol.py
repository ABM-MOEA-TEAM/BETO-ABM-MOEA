# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:58:22 2020

@author: jacks074
"""

# Corn Stover Conversion - Ethanol
import TEA_LCA_Data as D
import UnivFunc as UF
import Corn_Stover_Cultivation as CSC

def ethanol_stover(biomass_IO_array):
    
    return_array = UF.createEmptyFrame()    
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Corn Stover']]      # Grab the total amount of stover sent to BPP
    
    corn_stover_qty = 0.5*UF.returnPintQty(biomass_IO_array, match_list)
      
    return_array.loc[0] = UF.getWriteRow('Water', D.conv, 
                                      D.tl_input, 7.655*corn_stover_qty)
    
    return_array.loc[1] = UF.getWriteRow('Sulfuric Acid', D.conv, 
                                      D.tl_input, 0.031041*corn_stover_qty)

    return_array.loc[2] = UF.getWriteRow('Ammonia', D.conv, 
                                      D.tl_input, 0.013723*corn_stover_qty)
    
    return_array.loc[3] = UF.getWriteRow('Glucose', D.conv, 
                                      D.tl_input, 0.0252*corn_stover_qty)
    
    return_array.loc[4] = UF.getWriteRow('Corn Steep Liquor', D.conv, 
                                      D.tl_input, 0.015684*corn_stover_qty)
    
    return_array.loc[5] = UF.getWriteRow('Lime', D.conv, 
                                      D.tl_input, 0.01374*corn_stover_qty)
    
    return_array.loc[6] = UF.getWriteRow('Sodium Hydroxide', D.conv, 
                                      D.tl_input, 0.024668*corn_stover_qty)

    return_array.loc[7] = UF.getWriteRow('Corn Beer', D.conv, 
                                      D.tl_output, 4.727*corn_stover_qty)
    
    return_array.loc[8] = UF.getWriteRow('Corn Stover', D.conv,
                                      D.tl_input, corn_stover_qty)
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Electricity'], 0.519228,'MJ/kg')
    return_array.loc[9] = UF.getWriteRow('Electricity', D.conv,
                                      D.tl_input, scale9.qty*corn_stover_qty)
    # 2888.51 MJ/ha from summing electricity inputs in Excel Model Blocks
    
    scale10 = D.TEA_LCA_Qty('Land Capital Cost', 0.000001, 'dollars')
    return_array.loc[10] = UF.getWriteRow('Land Capital Cost', D.conv, 
                                      D.tl_input, scale10.qty)
    
    scale3 = D.TEA_LCA_Qty('Labor', 0.000001, 'dollars/yr')
    return_array.loc[11] = UF.getWriteRow('Labor', D.conv, 
                                      D.tl_input, scale3.qty)
    
    return return_array
    
def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yield_value = 5563.08
    biomass_IO_array = CSC.grow_stover(land_area_val,yield_value)
   
    return ethanol_stover(biomass_IO_array)

if __name__ == "__main__":
    output = main()