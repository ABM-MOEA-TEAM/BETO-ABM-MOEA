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
                 [UF.substance_name, 'Corn Stover Collected']]      # Grab the total amount of stover sent to BPP
    
    corn_stover_qty = UF.returnPintQty(biomass_IO_array, match_list)
      
    return_array.loc[0] = UF.getWriteRow('Water', D.conv, 
                                      D.tl_input, 7.655*corn_stover_qty)
    
    return_array.loc[1] = UF.getWriteRow('Sulfuric Acid', D.conv, 
                                      D.tl_input, 0.0532*corn_stover_qty)

    return_array.loc[2] = UF.getWriteRow('Ammonia', D.conv, 
                                      D.tl_input, 0.0117*corn_stover_qty)
    
    return_array.loc[3] = UF.getWriteRow('Glucose', D.conv, 
                                      D.tl_input, 0.0252*corn_stover_qty)
    
    return_array.loc[4] = UF.getWriteRow('Corn Steep Liquor', D.conv, 
                                      D.tl_input, 0.0145*corn_stover_qty)
    
    return_array.loc[5] = UF.getWriteRow('Lime', D.conv, 
                                      D.tl_input, 0.0128*corn_stover_qty)
    
    return_array.loc[6] = UF.getWriteRow('Sodium Hydroxide', D.conv, 
                                      D.tl_input, 0.0246*corn_stover_qty)
    
    return_array.loc[7] = UF.getWriteRow('Gasoline', D.conv, 
                                      D.tl_input, 0.018*corn_stover_qty)
    
    return_array.loc[8] = UF.getWriteRow('Corn Beer', D.conv, 
                                      D.tl_output, 4.727*corn_stover_qty)
    
    return_array.loc[9] = UF.getWriteRow('Ethanol', D.conv,
                                      D.tl_output, 0.25365*corn_stover_qty)
    
    return_array.loc[10] = UF.getWriteRow('Corn Stover Collected', D.conv,
                                      D.tl_input, corn_stover_qty)
    
    return return_array
    
def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = CSC.grow_stover(land_area_val,yearly_precip)
    # addendum_IO_array = UF.createEmptyFrame()
    
    # addendum_IO_array.loc[0] = UF.getWriteRow('Jet-A', D.conv, 
    #                                   D.tl_output, 0*land_area_val.qty)
    
    # addendum_IO_array.loc[1] = UF.getWriteRow('Diesel', D.conv, 
    #                                   D.tl_output, 0*land_area_val.qty)
    
    # addendum_IO_array.loc[2] = UF.getWriteRow('Electricity', D.conv, 
    #                                   D.tl_output, 0*land_area_val.qty)
    
    # biomass_IO_array = biomass_IO_array.append(addendum_IO_array,ignore_index=True)
    return ethanol_stover(biomass_IO_array)

if __name__ == "__main__":
    output = main()