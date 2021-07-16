# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 09:13:05 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Soy_Cultivation as SC

def Hexane_Extraction(biomass_IO_array):
    
    return UF.Collect_IndepVars_Loop('HexExt', 0, 0, 1, biomass_IO_array, 
                                     'Soybeans', 1, 0)
    # match_list = [[UF.input_or_output, D.tl_output],
    #              [UF.substance_name, 'Soybeans']]      
    
    # soybean_qty = UF.returnPintQty(biomass_IO_array, match_list)

    # tab_string = 'HexExt'
    
    # vars_list = UF.collectIndepVars(tab_string)
    
    # for i in range(len(vars_list)):
    #     name_list = []
    #     val_list = []
        
    #     val_list = vars_list[i]
    #     name_list = vars_list[i-1]
    #     I_O_list = vars_list[i-2]
    #     unit_list = vars_list[i-3]
        
    #     quad_list = list(zip(name_list, val_list, I_O_list, unit_list))
    #     # Zip together the names, values, I/O's and Units
        
    #     #print(quad_list)
        
    # return_array = UF.createEmptyFrame()
    # output_name_list = []
    # output_value_list = []
    # output_units_list = []
    
    # output_name_list.append('Soybeans')
    # output_value_list.append(soybean_qty)
    # output_units_list.append('kg/yr')
    
    
    # scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
    #                                     output_units_list[0])
    # return_array.loc[0] = UF.getWriteRow(output_name_list[0], D.conv,
    #                                     D.tl_input, scale0.qty)
    
    # j = 0
    # i = 1
    # while j < len(quad_list):
    #     rows = quad_list[j]
    #     if rows[0] == 'In' and rows[1] == 'dollars/kg soy':
          
    #         if rows[3] == 'Labor': # As the other two $'s are not /yr
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'dollars/kg')
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                     D.tl_input, scale_value.qty*soybean_qty)
                
    #             i += 1
                
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'dollars*yr/kg')
    #             # Might be better just to overwrite this entirely at the end? 
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                         D.tl_input, scale_value.qty*soybean_qty)
    #             i += 1
            
    #     if rows[0] == 'In' and rows[1] == 'kg/kg soy':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'')
    #         # Might be better just to overwrite this entirely at the end? 
            
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                     D.tl_input, scale_value.qty*soybean_qty)
    #         i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'MJ/kg soy':
            
    #         if rows[3] == 'LNG':
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'MJ/kg')
    #             # Might be better just to overwrite this entirely at the end? 
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                         D.tl_input, scale_value.qty*soybean_qty)
    #             i += 1
            
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'MJ/kg')
    #             # Might be better just to overwrite this entirely at the end? 
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                         D.tl_input, scale_value.qty*soybean_qty)
    #             i += 1

        
    #     if rows[0] == 'Out' and rows[1] == 'kg/kg soy':
            
    #         scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'')
    #         # Might be better just to overwrite this entirely at the end? 
            
    #         return_array.loc[i] = UF.getWriteRow(rows[3], D.conv,
    #                                     D.tl_output, scale_value.qty*soybean_qty)
    #         i += 1

    #     j += 1
    
    # return return_array

def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    yield_value = 3698
    biomass_IO_array = SC.grow_soybean(land_area_val, yield_value)
    #print(biomass_IO_array)
    return Hexane_Extraction(biomass_IO_array)

if __name__ == "__main__":
    output = main()