# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 12:41:40 2020

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF


def grow_soy(land_area_val, yearly_precip):
    
    size = land_area_val
    precip = yearly_precip 
    
    return_array = UF.createEmptyFrame()
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Soybean Seed'],233.514,'kg/ha/yr')
    
    return_array.loc[0] = UF.getWriteRow('Soybean Seed', D.biomass_production,
                                         D.tl_input, scale1.qty*size.qty)
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Nitrogen in Fertilizer'],16.81,'kg/ha/yr')
    return_array.loc[1] = UF.getWriteRow('Nitrogen in Fertilizer', D.biomass_production,
                                         D.tl_input, scale2.qty*size.qty)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Phosphorus in Fertilizer'],8.8,'kg/ha/yr')
    return_array.loc[2] = UF.getWriteRow('Phosphorus in Fertilizer', D.biomass_production,
                                         D.tl_input, scale3.qty*size.qty)
    
    scale4 = D.TEA_LCA_Qty(D.substance_dict['Potassium in Fertilizer'],38.97,'kg/ha/yr')
    return_array.loc[3] = UF.getWriteRow('Potassium in Fertilizer', D.biomass_production,
                                         D.tl_input, scale4.qty*size.qty)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Ag Lime (CaCO3)'],224,'kg/ha/yr')
    return_array.loc[4] = UF.getWriteRow('Ag Lime (CaCO3)', D.biomass_production,
                                         D.tl_input, scale5.qty*size.qty)
    
    scale6 = D.TEA_LCA_Qty(D.substance_dict['Herbicide'],12.26,'kg/ha/yr')
    return_array.loc[5] = UF.getWriteRow('Herbicide', D.biomass_production,
                                         D.tl_input, scale6.qty*size.qty)
    
    # scale7 = D.TEA_LCA_Qty(D.substance_dict['Atmospheric CO2'],5908.22,'kg/ha/yr')      # Really, this should scale
    # return_array.loc[6] = UF.getWriteRow('Atmospheric CO2', D.biomass_production,       # with expected Biomass Production
    #                                      D.tl_input, scale7.qty*size.qty)
    
    scale7 = D.TEA_LCA_Qty(D.substance_dict['Ag Lime (CaCO3)'],224,'kg/ha/yr')
    return_array.loc[6] = UF.getWriteRow('Ag Lime (CaCO3)', D.biomass_production,
                                         D.tl_input, scale7.qty*size.qty)
    
    scale8 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],4678, 'm**3/ha/yr')
    return_array.loc[7] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                         D.tl_input, scale8.qty*size.qty*precip.qty)
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Soybeans'],108.8, 'kg/in/yr/ha')
    return_array.loc[8] = UF.getWriteRow('Soybeans', D.biomass_production,
                                         D.tl_output, scale9.qty*size.qty*precip.qty)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 681.7, 'dollars/ha')         # From AltJet
    
    return_array.loc[9] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale10.qty*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 0.001, 'dollars/ha') #16549
    
    return_array.loc[10] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 61.75, 'dollars/ha/yr')
    
    return_array.loc[11] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 4665, 'm**3/yr/ha')
    
    return_array.loc[12] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_output, scale13.qty*size.qty)
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    return grow_soy(land_area_val, yearly_precip)

if __name__ == "__main__":
    output = main()