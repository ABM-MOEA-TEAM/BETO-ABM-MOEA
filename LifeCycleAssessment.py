# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 11:15:20 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd

def readtl_array(tl_array):
    
    output_subst = []
    input_subst = []
    output_val = []
    input_val = []
    
    for i in range(len(tl_array)):
        row = tl_array.loc[i]
        subst_name = row[UF.substance_name]
        subst_amnt = row[UF.magnitude]
        in_or_out  = row[UF.input_or_output]
    
        if in_or_out == 'Output':
            output_subst.append(subst_name)
            output_val.append(subst_amnt)
        
        if in_or_out == 'Input':
            input_subst.append(subst_name)
            input_val.append(subst_amnt)
            
    quad_list = [[],[],[],[]]
    
    quad_list = [input_subst, input_val, output_subst, output_val]
    
    return quad_list

# Same loop logic everywhere, I obviously need to centralize this.
# If possible it would be cool to write a general UF loop that takes
# a few arguments and does one or the other...

def LCAMetrics(tl_array):
    
    # Need to add logic to produce baseline revenue for $allocation
    
    return_list = []
    
    # output_frame = pd.DataFrame({'Energy Allocation, Pre-Combustion' : [],
    #                              'Energy Allocation, Post-Combustion' : [],
    #                              'Mass Allocation, Pre-Combustion' : [],
    #                              'Mass Allocation, Post-Combustion' : [],
    #                              'Economic Allocation, Pre-Combustion' : [],
    #                              'Economic Allocation, Post-Combustion' : [],
    #                              'System Boundary Expansion, Pre-Combustion' : [],
    #                              'System Boundary Expansion, Post-Combustion' : [],})
    
    input_emissions = calcInputEmissions(tl_array)
    end_use_emissions = calcEndUseEmissions(tl_array)
    coprod_emissions = calcCoProdEndUse(tl_array)
    total_MJ = calcMJProduced(tl_array)
    total_fuel_MJ = calcFuelMJProduced(tl_array)
    total_kg = calcMassOut(tl_array)
    total_dollars = calcRevenue(tl_array)
    total_credits = calcCredits(tl_array)
    
    ea_precomb_ghg = input_emissions / total_MJ
    ea_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_MJ
    ma_precomb_ghg = input_emissions / total_kg
    ma_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_kg
    dollara_precomb_ghg = input_emissions / total_dollars
    dollara_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_dollars
    se_precomb_ghg = (input_emissions + total_credits) / total_fuel_MJ
    se_postcomb_ghg = (input_emissions + total_credits + end_use_emissions + coprod_emissions) / total_fuel_MJ
    
    return_list.append(ea_precomb_ghg.magnitude)
    return_list.append(ea_postcomb_ghg.magnitude)
    return_list.append(ma_precomb_ghg)
    return_list.append(ma_postcomb_ghg)
    return_list.append(dollara_precomb_ghg)
    return_list.append(dollara_postcomb_ghg)
    return_list.append(se_precomb_ghg.magnitude)
    return_list.append(se_postcomb_ghg.magnitude)
    
    output_frame = pd.DataFrame({'Energy Allocation, Pre-Combustion' : [ea_precomb_ghg.magnitude],
                                 'Energy Allocation, Post-Combustion' : [ea_postcomb_ghg.magnitude],
                                 'Mass Allocation, Pre-Combustion' : [ma_precomb_ghg],
                                 'Mass Allocation, Post-Combustion' : [ma_postcomb_ghg],
                                 'Economic Allocation, Pre-Combustion' : [dollara_precomb_ghg],
                                 'Economic Allocation, Post-Combustion' : [dollara_postcomb_ghg],
                                 'System Boundary Expansion, Pre-Combustion' : [se_precomb_ghg.magnitude],
                                 'System Boundary Expansion, Post-Combustion' : [se_postcomb_ghg.magnitude],})
    
    
    return return_list

def calcMassOut(tl_array):
    
    return_value = 0
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        amount = output_value_list[i]
        return_value += amount
        # if name in D.emissions_list:
        #     # print('skipped')
        #     pass
        # else:
        #     return_value += amount    
            
        # Instrumentation
        # print('----', name, '----')
        # print(amount)
        # print(return_value)
        # print('---------------')
    
    return return_value

def calcCredits(tl_array):
    
    return_value = 0
    
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]   
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    LCA_val = 0
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        amount = output_value_list[i]
        
        # if (name == 'Soybean Meal' or
        #     name == 'Corn Stover, Left' or
        #     name == 'DDGS' or
        #     name == 'Glycerin'):
           
        if name in D.coprod_list:
            match_list = [[D.LCA_key_str, name],
                          [D.LCA_IO, D.tl_output]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df,
                                         match_list, D.LCA_GHG_impact)            
            # print(LCA_val)
            return_value += amount * LCA_val
        
        # Instrumentation
        # print('----', name, '----')
        # print(LCA_val)
        # print(amount)
        # print(LCA_val * amount)
        # print(return_value)
        # print('---------------')
    
    return return_value

def calcInputEmissions(tl_array):
    
    return_value = 0

    input_subst_list = []
    input_value_list = []
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    input_subst_list = quad_list[0]
    input_value_list = quad_list[1]
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    
    if len(input_subst_list) != len(input_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(input_subst_list)):
        name = input_subst_list[i]
        amount = input_value_list[i]
    
        match_list = [[D.LCA_key_str, name],
                      [D.LCA_IO, D.tl_input]]
        LCA_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_GHG_impact)            
        return_value += amount * LCA_val
        
        # Instrumentation
        # print('----', name, '----')
        # print(LCA_val)
        # print(amount)
        # print(LCA_val * amount)
        # print(return_value)
        # print('---------------')
        
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        amount = output_value_list[i]
            
        if name in D.emissions_list:
            match_list = [[D.LCA_key_str, name],
                           [D.LCA_IO, D.tl_output]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df,
                                         match_list, D.LCA_GHG_impact)
            return_value += amount * LCA_val
            
            # Instrumentation
            # print('In the thingy')
            # print('----', name, '----')
            # print(LCA_val)
            # print(amount)
            # print(LCA_val * amount)
            # print(return_value)
            # print('---------------')
    
    return return_value

def calcMJProduced(tl_array):

    return_value = 0

    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    # print(output_subst_list)
    # print(output_value_list)
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        HHV = D.HHV_dict[name].qty
        amount = output_value_list[i]
        
        return_value += amount * HHV 
    
        # print(return_value)
        
        # Instrumentation 
        # print('----', name, '----')
        # print(HHV)
        # print(amount)
        # print(amount * HHV)
        # print(return_value)
        # print('------------------')
        
    return return_value

def calcFuelMJProduced(tl_array):
    
    return_value = 0
    
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        
        name = output_subst_list[i]
        amount = output_value_list[i]
            
        if name in D.output_fuels_list:
            
            HHV = D.HHV_dict[name].qty
            return_value += amount * HHV     

    # Instrumentation 
        # print('----', name, '----')
        # print(HHV)
        # print(amount)
        # print(amount * HHV)
        # print(return_value)
        # print('------------------')
    
    return return_value
    
def calcEndUseEmissions(tl_array):
    
    return_value = 0
    
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        
        # Carbon Percentage defined in LCA tab and then also as indep var?
        
        # if (name != 'CO2 Emissions' and
        #     name != 'Soybean Meal' and
        #     name != 'DDGS' and
        #     name != 'N2O Emissions' and
        #     name != 'CO2, Commercial'):
        
        if name in D.output_fuels_list:
            
            Carbon_Percentage = D.Carbon_Dict[name]
            amount = output_value_list[i]
            
            return_value += ((amount)*Carbon_Percentage*44/12*1000)
    
    # Instrumentation
    # print('----', name, '----')
    # print(Carbon_Percentage)
    # print(amount)
    # print(return_value)
    
    return return_value

def calcCoProdEndUse(tl_array):
    
    return_value = 0
    
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        
        # Carbon Percentage defined in LCA tab and then also as indep var?
        
        # if (name != 'CO2 Emissions' and
        #     name != 'Soybean Meal' and
        #     name != 'DDGS' and
        #     name != 'N2O Emissions' and
        #     name != 'CO2, Commercial'):
        
        if name in D.coprod_list:
            
            Carbon_Percentage = D.Carbon_Dict[name]
            amount = output_value_list[i]
            
            return_value += ((amount)*Carbon_Percentage*44/12*1000)
    
            # Instrumentation
            # print('----', name, '----')
            # print(Carbon_Percentage)
            # print(amount)
            # print(return_value)
    
    return return_value
    
def calcRevenue(tl_array):
    
    return_value = 0
    
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]
    
    if len(output_subst_list) != len(output_value_list):
        print('Error - substance name list and value list of unequal length')
        return
    
    for i in range(len(output_subst_list)):
        name = output_subst_list[i]
        amount = output_value_list[i]
    
        match_list = [[D.LCA_key_str, name],
                      [D.LCA_IO, D.tl_output]]
        LCA_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_cost)            
        return_value += amount * LCA_val
        
        # Instrumentation
        # print('----', name, '----')
        # print(amount)
        # print(LCA_val)
        # print(return_value)
    
        
    return return_value