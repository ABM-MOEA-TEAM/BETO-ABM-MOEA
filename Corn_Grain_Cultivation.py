# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:37:17 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

def grow_corn(size,yearly_precip):
 
    return_array = UF.createEmptyFrame()    
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Collected'], 17.69, 'kg/ha/yr')
       
    return_array.loc[0] = UF.getWriteRow('Corn Seed', D.biomass_production, 
                                      D.tl_input, scale1.qty*size.qty)
    
    # The operation above, then, writes in to the return array the amount of 
    # corn seed needed, scaled up by 17.69 kg/ha/yr (fixes units, but inelegant)
    
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
    
    scale7 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 253236, 'kg/in/ha/yr')
    
    return_array.loc[6] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_input, scale7.qty*yearly_precip.qty*size.qty)
          
    scale8 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Left'], 327.24, 'kg/in/ha/yr')
    
    return_array.loc[7] = UF.getWriteRow('Corn Stover Left', D.biomass_production, 
                                      D.tl_output, scale8.qty*yearly_precip.qty*size.qty)
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 322.759, 'kg/in/ha/yr')
    
    return_array.loc[8] = UF.getWriteRow('Corn Grain', D.biomass_production, 
                                      D.tl_output, scale9.qty*yearly_precip.qty*size.qty)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 2300, 'dollars/ha/yr')
    
    return_array.loc[9] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale10.qty*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha/yr')
    
    return_array.loc[10] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 33.33333, 'dollars/ha/yr')
    
    return_array.loc[11] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 252875, 'kg/in/ha/yr') # Total water eventually returned
    
    return_array.loc[12] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_output, scale13.qty*yearly_precip.qty*size.qty)
    
    return return_array
    
def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    return grow_corn(land_area_val, yearly_precip)

if __name__ == "__main__":
    output = main()