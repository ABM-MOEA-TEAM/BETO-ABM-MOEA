# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 16:58:22 2020

@author: jacks074
"""

# Corn Stover Conversion - Ethanol
import TEA_LCA_Data as D
import UnivFunc as UF

stover_ethanol_inputs_dict = {}
stover_ethanol_inputs_dict['Corn Stover'] = D.TEA_LCA_Qty(
    D.substance_dict['Corn Stover'],5563,'kg/yr/ha') 
stover_ethanol_inputs_dict['Water'] = D.TEA_LCA_Qty(
    D.substance_dict['Water'],42587,'kg/yr/ha')
stover_ethanol_inputs_dict['Sulfuric Acid'] = D.TEA_LCA_Qty(
    D.substance_dict['Sulfuric Acid'],173,'kg/yr/ha')
stover_ethanol_inputs_dict['Ammonia'] = D.TEA_LCA_Qty(
    D.substance_dict['Ammonia'],65.24,'kg/yr/ha')
stover_ethanol_inputs_dict['Glucose'] = D.TEA_LCA_Qty(
    D.substance_dict['Glucose'],140,'kg/yr/ha')
stover_ethanol_inputs_dict['Sulfur Dioxide'] = D.TEA_LCA_Qty(
    D.substance_dict['Sulfur Dioxide'],0.9,'kg/yr/ha')
stover_ethanol_inputs_dict['Corn Steep Liquor'] = D.TEA_LCA_Qty(
    D.substance_dict['Corn Steep Liquor'],80.68,'kg/yr/ha')
stover_ethanol_inputs_dict['Corn Oil'] = D.TEA_LCA_Qty(
    D.substance_dict['Corn Oil'],0.74,'kg/yr/ha')
stover_ethanol_inputs_dict['Ammonium Sulfate'] = D.TEA_LCA_Qty(
    D.substance_dict['Ammonium Sulfate'],1.04,'kg/yr/ha')
stover_ethanol_inputs_dict['Potassium Phosphate'] = D.TEA_LCA_Qty(
    D.substance_dict['Potassium Phosphate'],1.49,'kg/yr/ha')
stover_ethanol_inputs_dict['Magnesium Sulfate'] = D.TEA_LCA_Qty(
    D.substance_dict['Magnesium Sulfate'],0.22,'kg/yr/ha')
stover_ethanol_inputs_dict['Calcium Chloride'] = D.TEA_LCA_Qty(
    D.substance_dict['Calcium Chloride'],0.28,'kg/yr/ha')
stover_ethanol_inputs_dict['Diammonium Phosphate'] = D.TEA_LCA_Qty(
    D.substance_dict['Diammonium Phosphate'],8.7,'kg/yr/ha')
stover_ethanol_inputs_dict['Corn Steep Liquor'] = D.TEA_LCA_Qty(
    D.substance_dict['Corn Steep Liquor'],7,'kg/yr/ha')
stover_ethanol_inputs_dict['Lime'] = D.TEA_LCA_Qty(
    D.substance_dict['Lime'],71,'kg/yr/ha')
stover_ethanol_inputs_dict['Sodium Hydroxide'] = D.TEA_LCA_Qty(
    D.substance_dict['Sodium Hydroxide'],137,'kg/yr/ha')
stover_ethanol_inputs_dict['Gasoline'] = D.TEA_LCA_Qty(
    D.substance_dict['Gasoline'],10,'kg/yr/ha')

stover_ethanol_outputs_dict = {}

return_array2 = UF.createEmptyFrame()

corn_beer_output = D.TEA_LCA_Qty(D.substance_dict['Corn Beer'], 26296, 'kg/yr/ha')



def ethanol_stover(biomass_IO_array):

    crop_inputs = stover_ethanol_inputs_dict
    crop_outputs = stover_ethanol_outputs_dict

    match_list = [[UF.input_or_output, D.tl_output],
                  [UF.substance_name, 'Corn Stover']]
    corn_stover_out_qty = UF.returnPintQty(biomass_IO_array, match_list)
    
    return_array2.loc[0] = UF.getWriteRow('Corn Stover', D.conv, 
                                      D.tl_input, corn_stover_out_qty)    


    return_array2.loc[1] = UF.getWriteRow('Corn Beer', D.conv, 
                                      D.tl_output, corn_beer_output.qty)
    
    
    row_count = 2
    
    for key in crop_inputs:
        pint_qty = crop_inputs[key].qty 
        return_array2.loc[row_count] = UF.getWriteRow(key, D.conv, 
                                                  D.tl_input, pint_qty)
        row_count += 1

        
    # Scale crop outputs
    for key in crop_outputs:
        pint_qty = crop_outputs[key].qty
        return_array2.loc[row_count] = UF.getWriteRow(key, D.conv, 
                                                  D.tl_output, pint_qty)
        row_count += 1
        
    
    return return_array2
    