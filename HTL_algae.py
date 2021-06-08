# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:03:04 2021

@author: Jack Smith
"""

# HTL Model converted from EGS's Excel "Simplified HTL EGS rev1" on 6/3

import TEA_LCA_Data as D
import UnivFunc as UF
import algae_cult_placeholder as ACP

def HTL_algae(biomass_array, pathway_ID):
    
    return_array = UF.createEmptyFrame()    
    
    match_list = [[UF.input_or_output, D.tl_output],
                 [UF.substance_name, 'Algae AFDW']]
    
    algae_afdw_qty = UF.returnPintQty(biomass_array, match_list)
    
    percent_solids = 0.2
    protein_content = 0.377  
    carb_content = 0.23
    lipid_content = 0.251
    ash_content = 0.142
    
    drying_heat = 1662      # kJ/kg AFDW
    process_heat = 1974     # kJ/kg AFDW
    process_elec = 404      # kJ/kg AFDW
    
    diesel_yield = 0.691    # kg Diesel/kg Biocrude
    naptha_yield = 0.1367   # kg Naptha/kg Biocrude
    hydrogen_yield = 0.057  # kg Hydrogen/kg Biocrude
    
    biocrude_yield = ((0.85*lipid_content) + (0.45*protein_content)
                 + (0.22*carb_content) + (0*ash_content))       # kg Biocrude/kg AFDW
    
    biochar_yield = ((0*lipid_content)+(0*protein_content)
                     +(0.41*carb_content)+(0.18*ash_content))   # kg Biochar/kg AFDW
    
    biocrude_produced = biocrude_yield * algae_afdw_qty
    
    return_array.loc[0] = UF.getWriteRow('Algae AFDW', D.conv, 
                                      D.tl_input, algae_afdw_qty)
    
    scale4 = D.TEA_LCA_Qty('LNG', drying_heat, 'MJ/kg')
    scale5 = D.TEA_LCA_Qty('LNG', process_heat, 'MJ/kg')
    
    return_array.loc[1] = UF.getWriteRow('LNG', D.conv, 
                                      D.tl_input, (scale4.qty * algae_afdw_qty)
                                      +(scale5.qty * algae_afdw_qty))
    
    scale0 = D.TEA_LCA_Qty('Electricity', process_elec, 'MJ/kg')
    return_array.loc[2] = UF.getWriteRow('Electricity', D.conv, 
                                      D.tl_input, scale0.qty * algae_afdw_qty)
  
    scale1 =  D.TEA_LCA_Qty('Capital Cost', 10539.41, 'dollars*year/kg')
    return_array.loc[3] = UF.getWriteRow('Capital Cost', D.conv, 
                                      D.tl_input, scale1.qty*algae_afdw_qty)
    
    scale2 = D.TEA_LCA_Qty('Land Capital Cost', 0.000001, 'dollars')
    return_array.loc[4] = UF.getWriteRow('Land Capital Cost', D.conv, 
                                      D.tl_input, scale2.qty)
    
    scale3 = D.TEA_LCA_Qty('Labor', 0.000001, 'dollars/yr')
    return_array.loc[5] = UF.getWriteRow('Labor', D.conv, 
                                      D.tl_input, scale3.qty)
    
    if pathway_ID == 0:
        
        return_array.loc[6] = UF.getWriteRow('Biocrude', D.conv, 
                                      D.tl_output, biocrude_produced)
    
    if pathway_ID == 1:
        
        return_array.loc[6] = UF.getWriteRow('Diesel', D.conv, 
                                      D.tl_output, biocrude_produced*diesel_yield)
    if pathway_ID == 2:
        
        return_array.loc[6] = UF.getWriteRow('Naptha', D.conv, 
                                      D.tl_output, biocrude_produced*naptha_yield)
    
    if pathway_ID == 3:
        
        return_array.loc[6] = UF.getWriteRow('Hydrogen', D.conv, 
                                      D.tl_output, biocrude_produced*hydrogen_yield)
    
    if pathway_ID >= 4:
        
        print('Undefined Pathway ID, expects integer between 0 and 3 for')
        print('End fuel products of Biocrude, Diesel, Naptha, and Hydrogen')
        print('for 0,1,2 and 3 respectively')
        return
    
    return_array.loc[7] = UF.getWriteRow('Biochar', D.conv, 
                                      D.tl_output, biochar_yield*algae_afdw_qty)
    
    
    return return_array
    
def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    biomass_IO_array = ACP.grow_algae(land_area_val)
    pathway_ID = 3
    return HTL_algae(biomass_IO_array, pathway_ID)

if __name__ == "__main__":
    output = main()
