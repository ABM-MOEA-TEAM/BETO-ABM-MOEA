# -*- coding: utf-8 -*-
"""
Created on Tue May  4 01:03:05 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF


def grow_miscanthus(land_area_val):

    return UF.Collect_IndepVars_Loop('MiscCult', 0, 0, 0, 0, 0, 0, 0,0)
    # tab_string = 'MiscCult'
    
    # vars_list = UF.collectIndepVars(tab_string)
    
    # for i in range(len(vars_list)):
    #     name_list = []
    #     val_list = []
        
    #     val_list = vars_list[i]
    #     name_list = vars_list[i-1]
    #     I_O_list = vars_list[i-2]
    #     unit_list = vars_list[i-3]
        
    #     quad_list = list(zip(name_list, val_list, I_O_list, unit_list))    

    # size = 0  # ! Need to change this to pull from excel sheet
    # return_array = UF.createEmptyFrame()
    # output_name_list = []
    # output_value_list = []
    # output_units_list = []
    
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
    # Miscanthus_Yield = scale0.qty*size.qty
    
    # j = 0
    # i = 1
    # while j < len(quad_list):
    #     rows = quad_list[j]
    #     if rows[0] == 'In' and rows[1] == 'kg/ha/yr':
            
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
    #                                     rows[2],'ha**-1/yr')  # Need a guess on the mass of 1 plug
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
            
    #     if rows[0] == 'In' and rows[1] == 'kg/kg Miscanthus':
    #         if rows[3] == 'LNG':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                         rows[2],'')
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                         D.tl_input, scale_value.qty*Miscanthus_Yield*D.HHV_dict['LNG'].qty) 
    #             i += 1
                
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                         rows[2],'kg/kg')
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                         D.tl_input, scale_value.qty*Miscanthus_Yield)    
    #             i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'm3/ha/yr':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                     rows[2],'m**3/ha/yr')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
            
    #     if rows[0] == 'In' and rows[1] == 'MJ/kg Miscanthus':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                 rows[2],'MJ/kg')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*Miscanthus_Yield) 
    #         i += 1
        
    #     if rows[1] == '%':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict['Atmospheric CO2'],
    #                                     rows[2],'kg/kg')
    #         return_array.loc[i] = UF.getWriteRow('Atmospheric CO2', D.biomass_production,
    #                                     D.tl_input, (44/12)*scale_value.qty*Miscanthus_Yield/100) 
    #         i += 1    
    #     j += 1
            
    # return return_array

def grow_Misc(size, yield_value):
 
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
    # yield_value = 28016.44
    return grow_miscanthus(land_area_val)

if __name__ == "__main__":
    output = main()