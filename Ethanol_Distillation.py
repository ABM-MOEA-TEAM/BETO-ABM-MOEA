# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 09:13:40 2020

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Corn_Stover_Cultivation as CSC
import Corn_Stover_Ethanol as CSE

def distillation(biomass_IO_array):

    # This variable can be selected from an array which corresponds to 
    # ethanol composition of different post-fermentation beers. 

    ethanol_percentage = 0.05329    

    return_array = UF.createEmptyFrame()    
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Corn Beer']]
    
    corn_beer_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    return_array.loc[0] = UF.getWriteRow('Electricity', D.conv, 
                                      D.tl_input, 0.0167*corn_beer_qty)
    
    return_array.loc[1] = UF.getWriteRow('Heat', D.conv,
                                      D.tl_input, 0.52011*corn_beer_qty)
    
    return_array.loc[2] = UF.getWriteRow('Gasoline', D.conv,
                                      D.tl_input, 0.00036864*corn_beer_qty)
    
    return_array.loc[3] = UF.getWriteRow('Ethanol', D.conv,
                                      D.tl_output, (0.053294*corn_beer_qty)+(0.00036864*corn_beer_qty))
    
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_IO_array = CSC.grow_stover(land_area_val,yearly_precip)
    return distillation(biomass_IO_array)

if __name__ == "__main__":
    output = main()