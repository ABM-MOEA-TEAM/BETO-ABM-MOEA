# -*- coding: utf-8 -*-
"""
Created on Tue May  4 01:03:05 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF

def grow_Miscanthus(size, yield_value):
 
    return_array = UF.createEmptyFrame()    
 
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Rhizome Plugs'], 0.00057358, 'kg/ha/yr')
    return_array.loc[0] = UF.getWriteRow('Rhizome Plugs', D.biomass_production, 
                                      D.tl_input, scale1.qty*size.qty*yield_value)
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Nitrogen in Fertilizer'], 0.004, 'kg/ha/yr')
    return_array.loc[1] = UF.getWriteRow('Nitrogen in Fertilizer', D.biomass_production,
                                      D.tl_input, scale2.qty*size.qty*yield_value)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Phosphorus in Fertilizer'], 0.00075, 'kg/ha/yr')
    return_array.loc[2] = UF.getWriteRow('Phosphorus in Fertilizer', D.biomass_production,
                                      D.tl_input, scale3.qty*size.qty*yield_value)
    
    scale4 = D.TEA_LCA_Qty(D.substance_dict['Potassium in Fertilizer'], 0.004, 'kg/ha/yr')
    return_array.loc[3] = UF.getWriteRow('Potassium in Fertilizer', D.biomass_production,
                                      D.tl_input, scale4.qty*size.qty*yield_value)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Ag Lime (CaCO3)'], 452, 'kg/ha/yr')
    return_array.loc[4] = UF.getWriteRow('Ag Lime (CaCO3)', D.biomass_production,
                                      D.tl_input, scale5.qty*size.qty)
    
    scale6 = D.TEA_LCA_Qty(D.substance_dict['Herbicide'], 61.29, 'kg/ha/yr')
    return_array.loc[5] = UF.getWriteRow('Herbicide', D.biomass_production,
                                      D.tl_input, scale6.qty*size.qty)

    scale7 = D.TEA_LCA_Qty(D.substance_dict['Miscanthus'], 1, 'kg/ha/yr')
    return_array.loc[6] = UF.getWriteRow('Miscanthus', D.biomass_production, 
                                      D.tl_output, scale7.qty*yield_value*size.qty)

    scale8 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 1049, 'dollars/ha') #597.7
    return_array.loc[7] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale8.qty*size.qty)
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha') #16549
    return_array.loc[8] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale9.qty*size.qty)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 33.33, 'dollars/ha/yr')
    return_array.loc[9] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale10.qty*size.qty)
    
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yield_value = 28016.44
    return grow_Miscanthus(land_area_val, yield_value)

if __name__ == "__main__":
    output = main()