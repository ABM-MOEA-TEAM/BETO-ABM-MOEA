# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:11:55 2020

@author: Jack Smith
"""
#   This File represents the conversion of the "Bounded Rain Cellulosic Ethanol" PM 
#   Agricultural Growth and Conversion steps.  

import TEA_LCA_Data as D
import UnivFunc as UF
    
stover_collected = 0.5 


def grow_stover(size,yield_value):
    
#    scales = stover_scaling_dict
 
    return_array = UF.createEmptyFrame()    

    ############    INPUTS    ###############    
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'], 17.69, 'kg/ha/yr')
       
    return_array.loc[0] = UF.getWriteRow('Corn Seed', D.biomass_production, 
                                      D.tl_input, scale1.qty*size.qty)
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Nitrogen in Fertilizer'], 161.37, 'kg/ha/yr')
    
    return_array.loc[1] = UF.getWriteRow('Nitrogen in Fertilizer', D.biomass_production,
                                      D.tl_input, scale2.qty*size.qty)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Phosphorus in Fertilizer'], 15.65, 'kg/ha/yr')
    
    return_array.loc[2] = UF.getWriteRow('Phosphorus in Fertilizer', D.biomass_production,
                                      D.tl_input, scale3.qty*size.qty)
    
    scale4 = D.TEA_LCA_Qty(D.substance_dict['Potassium in Fertilizer'], 76.09, 'kg/ha/yr')
    
    return_array.loc[3] = UF.getWriteRow('Potassium in Fertilizer', D.biomass_production,
                                      D.tl_input, scale4.qty*size.qty)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Ag Lime (CaCO3)'], 452, 'kg/ha/yr')
    
    return_array.loc[4] = UF.getWriteRow('Ag Lime (CaCO3)', D.biomass_production,
                                      D.tl_input, scale5.qty*size.qty)
    
    scale6 = D.TEA_LCA_Qty(D.substance_dict['Herbicide'], 1.21, 'kg/ha/yr')
    
    return_array.loc[5] = UF.getWriteRow('Herbicide', D.biomass_production,
                                      D.tl_input, scale6.qty*size.qty)

    scale7 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 838.39, 'kg/ha/yr') 
    
    return_array.loc[6] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_input, scale7.qty*yield_value*size.qty)
   # 4/6 - the rain values are still scaling wrt to the yield, don't know what to set this to

    scale8 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Collected'], 1, 'kg/ha/yr')
    
    return_array.loc[7] = UF.getWriteRow('Corn Stover Collected', D.biomass_production, 
                                      D.tl_output, scale8.qty*yield_value*size.qty)
   # 4/6 - Removed the scalar for "stover collected" - hope to put back in before push

    scale9 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Left'], 1, 'kg/ha/yr')
    
    return_array.loc[8] = UF.getWriteRow('Corn Stover Left', D.biomass_production, 
                                      D.tl_output, scale9.qty*yield_value*size.qty)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 2.255, 'kg/ha/yr')
    
    return_array.loc[9] = UF.getWriteRow('Corn Grain', D.biomass_production, 
                                      D.tl_output, scale10.qty*yield_value*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 597.7, 'dollars/ha') #597.7
    
    return_array.loc[10] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha') #16549
    
    return_array.loc[11] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 33.33, 'dollars/ha/yr')
    
    return_array.loc[12] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale13.qty*size.qty)
    
    scale14 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 836.18, 'kg/ha/yr') # Total water eventually returned
    
    return_array.loc[13] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_output, scale14.qty*yield_value*size.qty)
    
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    yield_value = 5563.08
    return grow_stover(land_area_val, yield_value)

if __name__ == "__main__":
    output = main()