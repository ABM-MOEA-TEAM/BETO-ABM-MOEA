# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:37:17 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    
biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'],10974,'kg/ha/yr')

def grow_corn(size,biomass_yield):
 
    return_array = UF.createEmptyFrame()    
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'], 17.69, 'kg/ha/yr')
       
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
    
    scale7 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 4678, 'm**3/ha/yr')
    
    return_array.loc[6] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,       # needed?
                                      D.tl_input, scale7.qty*size.qty)                       # 34 is avg precip
    
    return_array.loc[7] = UF.getWriteRow('Corn Stover', D.biomass_production,              #
                                      D.tl_output, 0.886776927*biomass_yield.qty*size.qty)
    
    return_array.loc[8] = UF.getWriteRow('Corn Grain', D.biomass_production,                    #
                                      D.tl_output, biomass_yield.qty*size.qty)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 2300, 'dollars/ha') #2300
    
    return_array.loc[9] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale10.qty*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 0.001, 'dollars/ha') #16549
    
    return_array.loc[10] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 33.3333333, 'dollars/ha/yr')
    
    return_array.loc[11] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 4665, 'm**3/ha/yr') # Total water eventually returned
    
    return_array.loc[12] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,      #
                                      D.tl_output, scale13.qty*size.qty)
    
    return return_array
    
def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'],10974,'kg/ha/yr')
    return grow_corn(land_area_val, biomass_yield)

if __name__ == "__main__":
    output = main()