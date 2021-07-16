# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 00:47:04 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

def grow_corn(land_area_val):
    
    return UF.Collect_IndepVars_Loop('CornCult', 0, 0, 0, 0, 0, 0, 0)
    
    # tab_string = 'CornCult'
    
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
    # stover_collection_percentage = 0
    # # While loop runs through the list of quads to grab the ha's & outputs 
    
    # i = 0
    # while i < len(quad_list):
    #     rows = quad_list[i]
        
    #     if rows[3] == 'Stover Collected':
    #         stover_collection_percentage = rows[2]
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
    # if stover_collection_percentage == 0:
    #     print('Error - expected non-zero argument for stover collection %')
    
    # scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
    #                                     output_units_list[0])        
    # return_array.loc[0] = UF.getWriteRow(output_name_list[0], D.biomass_production,
    #                                     D.tl_output, scale0.qty*size.qty)
    
    # corn_grain_yield = scale0.qty*size.qty
    
    # scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[1]],output_value_list[1],
    #                                     output_units_list[1])        
    # return_array.loc[1] = UF.getWriteRow(output_name_list[1], D.biomass_production,
    #                                     D.tl_output, scale1.qty*size.qty
    #                                     *stover_collection_percentage/100)
    # corn_stover_yield = scale1.qty*size.qty*stover_collection_percentage/100
    
    # j = 0
    # i = 2
    # while j < len(quad_list):
    #     rows = quad_list[j]
    #     if rows[0] == 'In' and rows[1] == 'kg/ha/yr':

    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],rows[1])
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty)
    #         i += 1
            
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
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'],
    #                                     rows[2]/1695.433,'kg/ha/yr')
    #         return_array.loc[i] = UF.getWriteRow('Corn Seed', D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
    
    #     if rows[0] == 'In' and rows[1] == 'm3/ha/yr':
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                     rows[2],'m**3/ha/yr')
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'MJ/ha/yr':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                 rows[2],rows[1])
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                     D.tl_input, scale_value.qty*size.qty) 
    #         i += 1
        
    #     if rows[3] == 'Carbon Content':
            
    #         carbon_content = rows[2]
            
    #         return_array.loc[i] = UF.getWriteRow('Atmospheric CO2', D.biomass_production,
    #                                     D.tl_input, ((carbon_content/100)*
    #                                                  (44/12)*(corn_grain_yield + corn_stover_yield)))
    #         # print(corn_grain_yield)
    #         # print(corn_stover_yield)
    #         i += 1
           
    #     j += 1
        
    # return return_array

def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    return grow_corn(land_area_val)

if __name__ == "__main__":
    output = main()