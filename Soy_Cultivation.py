# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 12:41:40 2020

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF

def grow_soybean(land_area_val, yield_value): # Need to remove yield arg I think
   
    return UF.Collect_IndepVars_Loop('SoyCult', 1, 1, 0, 0, 0, 0, 'Soy')
    
    # tab_string = 'SoyCult'
    
    # vars_list = UF.collectIndepVars(tab_string)
    
    # for i in range(len(vars_list)):
    #     name_list = []
    #     val_list = []
        
    #     val_list = vars_list[i]
    #     name_list = vars_list[i-1]
    #     I_O_list = vars_list[i-2]
    #     unit_list = vars_list[i-3]
        
    #     quad_list = list(zip(name_list, val_list, I_O_list, unit_list))
        
    #     # Not sure about this zip function, as it goes through four iterations
    #     # of the quad list for some reason; reordering the arguments each time.
        
    #     #print(quad_list)
    #     # There is probably a more elegant way to do this, but this seems
    #     # to be general enough to work with currently (6/23)
    
    # size = 0  # ! Need to change this to pull from excel sheet
    # return_array = UF.createEmptyFrame()
    # output_name_list = []
    # output_value_list = []
    # output_units_list = []
    
    # # While loop runs through the list of quads to grab the ha's & outputs 
    
    # i = 0
    # while i < len(quad_list):
    #     rows = quad_list[i]
    #     if rows[0] == 'Out':
    #           output_name_list.append(rows[3])
    #           output_value_list.append(rows[2])
    #           output_units_list.append(rows[1])
    #     if rows[1] == 'ha':
    #         size = D.TEA_LCA_Qty(D.substance_dict['Land Area'], rows[2], 'hectare')
    #     i += 1
        
    # # Now we have the biomass production output substances and values
    # # print(output_units_list)
    # # print(output_units_list[0])
    # # print(size.qty)
    
    # if len(output_name_list) == 0:
    #     print('Error - No Out Substances Found From Excel Sheet')
    #     return
    # if size == 0:
    #     print('Error - No land Area Argument Detected, expects ha')
    #     return 
    
    # scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
    #                                     output_units_list[0])        
    # return_array.loc[0] = UF.getWriteRow(output_name_list[0], D.biomass_production,
    #                                     D.tl_output, scale0.qty*size.qty)
    # soybean_yield = scale0.qty*size.qty
    
    # #print(soybean_yield)
    
    # j = 0
    # i = 1
    # while j < len(quad_list):
    #     rows = quad_list[j]
    #     if rows[0] == 'In' and rows[1] == 'kg/ha/yr':
            
    #         # print('Triggered')
    #         # print(temp_units)
    #         # print(temp_units[0])

    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],rows[1])
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty)
    #         i += 1
            
    #     # And now a million exceptions for different unit types
        
    #     if rows[0] == 'In' and rows[1] == 'dollars/ha/yr':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],rows[1])
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty)
    #         i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'dollars/ha':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],rows[1])
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty)
    #         i += 1
        
    #     if rows[0] == 'In' and rows[1] == '#/ha/yr':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                     rows[2]*0.00194595,'kg/ha/yr')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
            
    #     if rows[0] == 'In' and rows[1] == 'kg/kg soy':
    #         if rows[3] == 'LNG':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                         rows[2],'')
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                         D.tl_input, scale_value.qty*soybean_yield*D.HHV_dict['LNG'].qty) 
    #             i += 1
                
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                         rows[2],'kg/kg')
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                         D.tl_input, scale_value.qty*soybean_yield)    
    #             i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'm3/ha/yr':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                     rows[2],'m**3/ha/yr')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
            
    #     if rows[0] == 'In' and rows[1] == 'MJ/kg soy':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                 rows[2],'MJ/kg')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*soybean_yield) 
    #         i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'kg C/kg soy':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict['Atmospheric CO2'],
    #                                     rows[2],'kg/kg')
    #         return_array.loc[i] = UF.getWriteRow('Atmospheric CO2', D.biomass_production,
    #                                     D.tl_input, (44/12)*scale_value.qty*soybean_yield) 
    #         i += 1    
        
    #     j += 1
            
    # return return_array



def grow_soy(land_area_val, yield_value):
    
    size = land_area_val
    
    return_array = UF.createEmptyFrame()
    
    soybean_seed = 120000 # per ha
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Soybean Seed'],0.00194595*soybean_seed,'kg/ha/yr')
    
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
    
    scale6 = D.TEA_LCA_Qty(D.substance_dict['Glyphosate'],12.26,'kg/ha/yr')
    return_array.loc[5] = UF.getWriteRow('Glyphosate', D.biomass_production,
                                         D.tl_input, scale6.qty*size.qty)
    
    # scale7 = D.TEA_LCA_Qty(D.substance_dict['Atmospheric CO2'],5908.22,'kg/ha/yr')      # Really, this should scale
    # return_array.loc[6] = UF.getWriteRow('Atmospheric CO2', D.biomass_production,       # with expected Biomass Production
    #                                      D.tl_input, scale7.qty*size.qty)
    
    
    scale8 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],4678, 'm**3/ha/yr')
    return_array.loc[6] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                         D.tl_input, scale8.qty*size.qty)
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Soybeans'],1, 'kg/yr/ha')
    return_array.loc[7] = UF.getWriteRow('Soybeans', D.biomass_production,
                                         D.tl_output, scale9.qty*size.qty*yield_value)
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 681.7, 'dollars/ha')         # From AltJet
    
    return_array.loc[8] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale10.qty*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha') #16549
    
    return_array.loc[9] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 61.75, 'dollars/ha/yr')
    
    return_array.loc[10] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 4665, 'm**3/ha/yr')
    
    return_array.loc[11] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_output, scale13.qty*size.qty)
    return return_array

def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    yield_value = 3698
    return grow_soybean(land_area_val, yield_value)

if __name__ == "__main__":
    output = main()