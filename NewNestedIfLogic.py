# -*- coding: utf-8 -*-
"""
Created on Wed Aug 4 21:32:15 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import pandas as pd
import numpy as np
import UnivFunc as UF
# import math 



import os
from pathlib import Path
cwd = os.getcwd()

# String Reads for Results Data Frame
substance_name = 'Substance_Name'
process_name = 'Process_Name'
input_or_output = 'In_or_out'
magnitude = 'Magnitude'
units = 'Units'
I_O = 'I/O'
name = 'Name'
base_value = 'Base Value'

def newNestedIfLogic(tab_string, yield_value, geospatial_indicator,
                     downstream_indicator, tl_array, input_substance_string,
                     which_step, DayCent_read_string, fips):
    
    # QUESTION LIST
    # How do you address combination output flows? (ethanol and denaturant)
    # Can you think of any downstream case which will need to consume more
    # than a single input string?
        # If it is, the "isinstance(thingy, str) could be a great way to 
        # determine if a list was given or a single input string
        # How decide which one is main substance amount?
    # What do I do about the Nitrous Emissions scaled from Nitrogen Placed?
    # Maybe make a tier-two type thing - goes through first round and then does
    # others? (Like nitrous or ethanol and fuel denaturant)
    # Is there any way to parse through the units string, find out if 'ha' is
    # present and, if so, just perform the scale by size operation?
    # How do we handle situations in which the geospatial read-in values are
    # of the "main (exception logic) substances" - like the inputs to the 
    # downstream processing bits?
    
    # Want to change "DayCent_read_string" to be column for External Data read
    
    # Still suppressing "geospatial and downstream" instances
    
    # Breakdown the old loop such that the main "unit read" logic is not
    # repeated three times. There really is only one or two things that 
    # change with each of the different branches.  
    
    # (Name String, Independent Variable, Unit, Input or Output (or Em?))
    
    # So the highest priority argument (first read) will be the IO column.
    # I like the idea of an "emissions" category or a "geospatial read"...
    # The units will specify the operation though. 
    
    # Not really sure how to handle things that scale off of outputs. 
    # For instance, how do I address this issue with the total ethanol
    # fuel out being the sum of the produced ethanol and the gasoline 
    # denaturant...?  New category of "scaled by output?" I just don't know...
    
    # Local Variable Definition
    
    main_substance_amount = 0
    output_name_list = []
    output_value_list = []
    output_units_list = []
    stover_collection_percentage = 0
    i = 0       # This counter indexes the return array
    skip_ind = 0
    overwrite_scale = 0
    
    # Grab Independent Variables logic
    
    quad_list = UF.collectIndepVars(tab_string)
    return_array = UF.createEmptyFrame()

    # Downstream Logic - Add Main Substance Amount
    
    if downstream_indicator == 1:
    
        if isinstance(input_substance_string, str) == True:
            
            match_list = [[input_or_output, D.tl_output],
                      [substance_name, input_substance_string]]
            # print(match_list)
            input_substance_amount = UF.returnPintQty(tl_array, match_list)
            
            output_name_list.append(input_substance_string)
            output_value_list.append(input_substance_amount)
            output_units_list.append('kg/yr')
        
            main_substance_amount = input_substance_amount
            # print(main_substance_amount)
        
        
        if isinstance(input_substance_string, list) == True:
            
            for j in len(range(input_substance_string)):
                
                match_list = [[input_or_output, D.tl_output],
                      [substance_name, input_substance_string[j]]]
        
                input_substance_amount = UF.returnPintQty(tl_array, match_list)
                
                output_name_list.append(input_substance_string[j])
                output_value_list.append(input_substance_amount[j])
                output_units_list.append('kg/yr')
       
            main_substance_amount = input_substance_amount[0]
            
        if len(output_name_list) > 1:
            
            for i in range(len(output_name_list)):
                scale_value = D.TEA_LCA_Qty(D.substance_dict[output_name_list[i]],
                              output_value_list[i], output_units_list[i])
                return_array.loc[i] = UF.getWriteRow(output_name_list[i], which_step,
                                            D.tl_input, scale_value.qty) 
                
        if len(output_name_list) == 1:
            scale_value = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],
                              output_value_list[0], output_units_list[0])
            return_array.loc[0] = UF.getWriteRow(output_name_list[0], which_step,
                                            D.tl_input, scale_value.qty)
        else:
            print('Error - downstream indicator triggered but no ')
            print('input substance string recognized. Ensure that')
            print('input substance string matches subst dict str.')
            return
    
    # Geospatial Data Logic
    
    if geospatial_indicator == 1 and downstream_indicator != 1:
        
        # print(output_name_list)
        
        size = D.TEA_LCA_Qty('Land Area', 100, 'ha')
        
        k = 0
        while k < len(quad_list):
            
            rows    = quad_list[k]
            name    = rows[0]
            amount  = rows[1]
            inout   = rows[2]
            unit    = rows[3]
        
            if name == 'Stover Collected':
                stover_collection_percentage = amount
            if inout == 'Out':
                output_name_list.append(name)
                output_value_list.append(amount)
                output_units_list.append(unit)
            if unit == 'ha':
                size = D.TEA_LCA_Qty(D.substance_dict['Land Area'],
                                     amount, 'hectare')
            k += 1
        
        if len(output_name_list) == 0:
            print('Error - No Out Substances Found From Excel Sheet')
            return
        # if size == 0:
        #     print('Error - No land Area Argument Detected, expects ha')
        #     return 
        if tab_string == 'CornCult' and stover_collection_percentage == 0:
            print('Error - expected non-zero argument for stover collection %')
        
        # scale = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]], 
        #                       yield_value, output_units_list[0])
        # return_array.loc[0] = UF.getWriteRow(name, which_step,
        #                                     D.tl_output, scale.qty)
        # i += 1
        
        if tab_string == 'CornCult':
            # print(i)
            scale = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'],
                                    yield_value, 'kg/ha/yr')
            return_array.loc[0] = UF.getWriteRow('Corn Grain', which_step,
                                    D.tl_output, scale.qty*size.qty)
            i += 1
            # print(i)
        
        
        if tab_string == 'SoyCult':
            # print(i)
            scale = D.TEA_LCA_Qty(D.substance_dict['Soybeans'],
                                    yield_value, 'kg/ha/yr')
            return_array.loc[0] = UF.getWriteRow('Soybeans', which_step,
                                    D.tl_output, scale.qty*size.qty)
            i += 1
        
        main_substance_amount = scale.qty * size.qty
        
        if len(output_name_list) >= 2:
            
            
            for j in range(len(output_name_list)):
                if output_name_list[j] == 'Corn Stover':
                    
                    scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[j]],
                                           output_value_list[j],
                                           output_units_list[j])        
                    return_array.loc[i] = UF.getWriteRow(output_name_list[j], 
                                                         which_step,
                                                         D.tl_output, 
                                                         scale1.qty*size.qty
                                                         *stover_collection_percentage/100)
                    
                    corn_stover_yield = scale1.qty*size.qty*(stover_collection_percentage/100)
                    
                    i += 1
                    
                if output_name_list[j] == 'Corn Grain' or output_name_list[j] == 'Soybeans':
                    # print('Youre not going to slow it, heaven knows you tried')
                    pass
                
                else:
                    # print(output_units_list)
                    scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[j]],output_value_list[j],
                                                    output_units_list[j])        
                    return_array.loc[i] = UF.getWriteRow(output_name_list[j], which_step,
                                                        D.tl_output, scale1.qty*size.qty)
                    i = i + 1
        
        


    if fips != 0:
        
        # Think that this only works for non-main substances...
        # Wait wait we want different costs and different LCI's, not 
        # different substance amounts? Well have capability...

        
        data_list = UF.External_Data('Practice Set (Python)')
        
        # print(data_list)
        
        fip_list = []
        amt_list = []
        
        k = 0 # Indexing Element
        
        for i in range(len(data_list)):
            
            # Omit the empty first row
            
            fip = data_list[i][0]
            amt = data_list[i][1]
            
            fip_list.append(fip)
            amt_list.append(amt)

        # print(fip_list)
        # print(amt_list)
        
        if fips in fip_list:
            
            k = fip_list.index(fips)
            amt = amt_list[k]
            # print(k)
            # print(amt)
            
        
    # Cultivation Portion
    
    if downstream_indicator == 0 and geospatial_indicator == 0:
        # Then you are in the cultivation portion
        
        k = 0 
        while k < len(quad_list):
            rows = quad_list[k]
            
            name    = rows[0]
            amount  = rows[1]
            inout   = rows[2]
            unit    = rows[3]
            
            if name == 'Stover Collected':
                    stover_collection_percentage = amount
            if inout == 'Out':
                output_name_list.append(name)
                output_value_list.append(amount)
                output_units_list.append(unit)
            if unit == 'ha':
                size = D.TEA_LCA_Qty(D.substance_dict['Land Area'],
                                     amount, 'hectare')
            k += 1
            
        if len(output_name_list) == 0:
            print('Error - No Out Substances Found From Excel Sheet')
            return
        if size == 0:
            print('Error - No land Area Argument Detected, expects ha')
            return 
        if tab_string == 'CornCult' and stover_collection_percentage == 0:
            print('Error - expected non-zero argument for stover collection %')
            return
    
        if len(output_name_list) >= 2:
            
            for j in range(len(output_name_list)):
                    
                name    = output_name_list[j]
                amount  = output_value_list[j]
                unit    = output_units_list[j]
                
                if name == 'Corn Stover':
                    
                    scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
                    return_array.loc[i] = UF.getWriteRow(name, 
                                                       which_step, 
                                                       D.tl_output, 
                                                       scale.qty*size.qty*stover_collection_percentage/100)
                    corn_stover_yield = scale.qty*size.qty*(stover_collection_percentage/100)
                    # print('Corn Stover', i)
                    i += 1
                    # print('Corn Stover', i)
                    # main_substance_amount = scale.qty * size.qty
                    
                if name == 'Corn Grain' or name == 'Soybeans':
                    
                    scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                          amount, unit)
                    return_array.loc[i] = UF.getWriteRow(name, which_step, D.tl_output, 
                                                         scale.qty*size.qty)
                    
                    # print('Corn Grain', i)
                    i += 1
                    # print('Corn Grain', i)
                    main_substance_amount = scale.qty * size.qty
                    
                    
                if (name != 'Corn Grain' and
                    name != 'Corn Stover' and
                    name != 'Soybeans'):
                    
                    scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
                    return_array.loc[i] = UF.getWriteRow(name, which_step, D.tl_output, 
                                                         scale.qty*size.qty)
                    
                    # print(name, i)
                    i += 1
                    # print(name, i)
                    # main_substance_amount = scale.qty * size.qty

            
        else:
            # print('In else statement')
            scale = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
                                        output_units_list[0])        
            return_array.loc[0] = UF.getWriteRow(output_name_list[0], which_step,
                                            D.tl_output, scale.qty*size.qty)
            i += 1
    

    ############### Units Read Portion (the big part) ################
    
    j = 0       # This variable reads through everything, 
                # i writes to returnarray
                
    i = len(output_name_list)
    # print(i)
    # print(main_substance_amount)
    
    for j in range(len(quad_list)):

        row = quad_list[j]

        name    = row[0]
        amount  = row[1]
        inout   = row[2]
        unit    = row[3]    

        if type(unit) == float:
            # print('No Unit Read for index ', j)
            # I think this solves our little indexing issue
            pass
            
        if inout == 'In' and unit == 'dollars/yr':
            
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
            return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                  D.tl_input, scale.qty)
            i += 1
        
        if inout == 'In' and unit == 'dollars/ha/yr':
            
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
            return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                  D.tl_input, scale.qty*size.qty)
            i += 1    
        
        if inout == 'In' and unit == 'dollars/ha':
            
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
            return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                  D.tl_input, scale.qty*size.qty)
            i += 1    
        
        if inout == 'In' and unit == 'dollars/kg Feedstock':
            
            if name == 'Labor':
                # print('If you never see this, delete this chunk')
                
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, 'dollars/kg')
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty * main_substance_amount)
                i += 1    
            else:
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, 'dollars*yr/kg')
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty * main_substance_amount)
                i += 1

        if inout == 'In' and unit == '#/ha/yr':
            if name == 'Soybean Seed':
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount*0.00194595,
                                            'kg/ha/yr')
                return_array.loc[i] = UF.getWriteRow(name, which_step,
                                            D.tl_input, scale.qty*size.qty) 
            
            if name == 'Corn Seed':
                scale = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'],
                                        amount/1695.433,'kg/ha/yr')
                return_array.loc[i] = UF.getWriteRow(rows[0], which_step,
                                            D.tl_input, scale.qty*size.qty)
                
            if rows[0] == 'Rhizome Plugs':
                scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                        amount,'ha**-1/yr')  # Need a guess on the mass of 1 plug
            return_array.loc[i] = UF.getWriteRow(name, which_step,
                                        D.tl_input, scale.qty*size.qty)
            i += 1        
        
        
        if inout == 'In' and unit == 'kg/ha/yr':
            
            if name == 'Corn Stover':
                print('Youre in the weird corn stover exception statement')
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty*size.qty)
            else:
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty*size.qty)
            i += 1
        
        if inout == 'In' and unit == 'kg/kg Feedstock':
            
            if name == 'LNG':
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, '')
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty * main_substance_amount
                                      /D.HHV_dict['LNG'].qty)
                i += 1  
            
            else:
                scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, 'kg/kg')
                return_array.loc[i] = UF.getWriteRow(name, which_step, 
                                      D.tl_input, scale.qty * main_substance_amount)
                # print('triggered')
                i += 1
          
        if inout == 'In' and unit == 'm3/ha/yr':
            # print(size.qty)
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, 'm**3/ha/yr')
            return_array.loc[i] = UF.getWriteRow(name, which_step, D.tl_input, 
                                  scale.qty * size.qty)
            i += 1    
          
        if inout == 'In' and unit == 'm3/kg Feedstock':
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, 'm**3/kg')
            return_array.loc[i] = UF.getWriteRow(name, which_step, D.tl_input, 
                                  scale.qty * main_substance_amount)
            i += 1    
        
        if inout == 'In' and unit == 'MJ/ha/yr':
            
            scale = D.TEA_LCA_Qty(D.substance_dict[name], amount, unit)
            return_array.loc[i] = UF.getWriteRow(name, which_step,
                                                 D.tl_input, scale.qty*size.qty)
            
            i += 1
        
        if inout == 'In' and unit == 'MJ/kg Feedstock':
                
                if name == 'LNG':
                    scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                        amount,'MJ/kg')
                    return_array.loc[i] = UF.getWriteRow(name, which_step,
                                            D.tl_input, scale.qty*main_substance_amount
                                            /D.HHV_dict['LNG'].qty)
                    skip_ind = 1

                    
                if name == 'Natural Gas':
                    scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                        amount,'MJ/kg')
                    return_array.loc[i] = UF.getWriteRow(name, which_step,
                                            D.tl_input, scale.qty
                                            *main_substance_amount/D.HHV_dict['Natural Gas'].qty)
                    skip_ind = 1
                    
                    
                if skip_ind != 1 or name == 'Electricity, Grid':
                    scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                        amount,'MJ/kg')
                    return_array.loc[i] = UF.getWriteRow(name, which_step,
                                            D.tl_input, scale.qty
                                            *main_substance_amount) 
                i += 1
        
        if unit == '%':
            if tab_string == 'CornCult' and name == 'Carbon Content':
                
                carbon_content = amount
                value = ((carbon_content/100)*(44/12)*(main_substance_amount
                                                       + corn_stover_yield))
                
                # Think that this above is not actually used...?
                return_array.loc[i] = UF.getWriteRow('CO2, Atmospheric', which_step,
                                        D.tl_input, ((carbon_content/100)*(44/12)
                                                      *(main_substance_amount + corn_stover_yield)))
               
            if tab_string != 'CornCult':
                scale = D.TEA_LCA_Qty(D.substance_dict['CO2, Atmospheric'],
                                            amount,'')
                return_array.loc[i] = UF.getWriteRow('CO2, Atmospheric', which_step,
                                            D.tl_input, (44/12)*scale.qty
                                            *main_substance_amount/100) 

            i += 1

            
        if inout == 'Out' and unit == 'kg/kg Feedstock':
            
            # This is the weird thing that we have to deal with somehow...
            
            if name == 'Ethanol' and tab_string == 'StarchFerm':
                
                scale = D.TEA_LCA_Qty(D.substance_dict[name], 
                                      amount + 0.014532693, '')
                # print(main_substance_amount)
                # print(scale.qty)
                return_array.loc[i] = UF.getWriteRow(name,
                                                     which_step,
                                                     D.tl_output,
                                                     scale.qty * main_substance_amount)
                # print(return_array.loc[i])
                # print(i)
                i += 1
                # print(i)
                
            else: 
                scale = D.TEA_LCA_Qty(D.substance_dict[name],
                                      amount, '')
                # print('DDGS loop next')
                # print(i)
                # print(scale.qty * main_substance_amount)
                return_array.loc[i] = UF.getWriteRow(name, 
                                                     which_step, 
                                                     D.tl_output, 
                                                     scale.qty * main_substance_amount)
                i += 1
                # print(i)
        # else:
        #     print('Warning - unrecognized Unit in index')
        #     print('i -' , i)
        #     print('j -' , j)
            
        j += 1
            
    return return_array












