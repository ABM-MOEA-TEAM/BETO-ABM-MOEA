# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:34:04 2021

@author: Jack Smith
"""

import UnivFunc as UF
import TEA_LCA_Data as D

import Soy_Cultivation as SC
import Hexane_Extraction as HE

def Transesterification(conversion_IO_array):
    
    return UF.Collect_IndepVars_Loop('Transest', 0, 0, 1, conversion_IO_array,
                                     'Soybean Oil', 2, 0)
    
    # match_list = [[UF.input_or_output, D.tl_output],
    #              [UF.substance_name, 'Soybean Oil']]      
    
    # soy_oil_qty = UF.returnPintQty(conversion_IO_array, match_list)

    # tab_string = 'Transest'
    
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
    
    # output_name_list.append('Soybean Oil')
    # output_value_list.append(soy_oil_qty)
    # output_units_list.append('kg/yr')
    
    # scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
    #                                     output_units_list[0])
    # return_array.loc[0] = UF.getWriteRow(output_name_list[0], D.upgrading,
    #                                     D.tl_input, scale0.qty)
    
    # j = 0
    # i = 1
    # while j < len(quad_list):
    #     rows = quad_list[j]
    #     if rows[0] == 'In' and rows[1] == 'dollars/kg veg oil':
          
    #         if rows[3] == 'Labor': # As the other two $'s are not /yr
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2], 'dollars/kg')
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.upgrading,
    #                                     D.tl_input, scale_value.qty*soy_oil_qty)
                
    #             i += 1
                
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'dollars*yr/kg')
    #             # Might be better just to overwrite this entirely at the end? 
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.upgrading,
    #                                         D.tl_input, scale_value.qty*soy_oil_qty)
    #             i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'kg/kg veg oil':
    #         if rows[3] == 'LNG':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],
    #                                         rows[2],'')
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.biomass_production,
    #                                         D.tl_input, scale_value.qty*soy_oil_qty*D.HHV_dict['LNG'].qty) 
    #             i += 1
                
    #         else:
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2], '')
                    
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.upgrading,
    #                                         D.tl_input, scale_value.qty*soy_oil_qty)
    #             i += 1
        
    #     if rows[0] == 'In' and rows[1] == 'MJ/kg veg oil':
            
    #         if rows[3] == 'LNG':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'')
               
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.upgrading,
    #                                         D.tl_input, scale_value.qty*soy_oil_qty
    #                                         *D.HHV_dict['LNG'].qty)
    #             i += 1
            
    #         else:
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[3]],rows[2],'MJ/kg')
                
    #             return_array.loc[i] = UF.getWriteRow(rows[3], D.upgrading,
    #                                         D.tl_input, scale_value.qty*soy_oil_qty)
    #             i += 1
                
    #     if rows[0] == 'Out' and rows[1] == 'kg/kg veg oil':
            
    #         if rows[3] == 'Biodiesel Yield Ratio':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict['Biodiesel'],rows[2],'')
                
    #             return_array.loc[i] = UF.getWriteRow('Biodiesel', D.upgrading,
    #                                         D.tl_output, scale_value.qty*soy_oil_qty)
    #             i += 1
            
    #         if rows[3] == 'Glycerin Yield Ratio':
                
    #             scale_value = D.TEA_LCA_Qty(D.substance_dict['Glycerin'],rows[2],'')
                
    #             return_array.loc[i] = UF.getWriteRow('Glycerin', D.upgrading,
    #                                         D.tl_output, scale_value.qty*soy_oil_qty)
    #             i += 1
            
    #     j += 1
        
    # return return_array

def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    yield_value = 3698
    biomass_IO_array = SC.grow_soybean(land_area_val, yield_value)
    conversion_IO_array = HE.Hexane_Extraction(biomass_IO_array)
    #print(biomass_IO_array)
    return Transesterification(conversion_IO_array)

if __name__ == "__main__":
    output = main()