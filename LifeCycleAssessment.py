# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 11:15:20 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import pandas as pd
import math

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

def LCAMetrics(tl_array, ol, fip):
    
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
    
    input_emissions = calcInputEmissions(tl_array, ol, fip)
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
    
    # print('Input Emissions Total')
    # print(input_emissions)
    
    output_frame = pd.DataFrame({'Energy Allocation, Pre-Combustion' : [ea_precomb_ghg.magnitude],
                                 'Energy Allocation, Post-Combustion' : [ea_postcomb_ghg.magnitude],
                                 'Mass Allocation, Pre-Combustion' : [ma_precomb_ghg],
                                 'Mass Allocation, Post-Combustion' : [ma_postcomb_ghg],
                                 'Economic Allocation, Pre-Combustion' : [dollara_precomb_ghg],
                                 'Economic Allocation, Post-Combustion' : [dollara_postcomb_ghg],
                                 'System Boundary Expansion, Pre-Combustion' : [se_precomb_ghg.magnitude],
                                 'System Boundary Expansion, Post-Combustion' : [se_postcomb_ghg.magnitude],})
    
    
    return return_list

def LCAMetrics_cult(tl_array, ol, fip):
    
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
    
    input_emissions = calcInputEmissions(tl_array, ol, fip)
    end_use_emissions = calcEndUseEmissions(tl_array)
    coprod_emissions = calcCoProdEndUse(tl_array)
    total_MJ = calcMJProduced(tl_array)
    # total_fuel_MJ = calcFuelMJProduced(tl_array)
    total_kg = calcMassOut(tl_array)
    total_dollars = calcRevenue(tl_array)
    total_credits = calcCredits(tl_array)
    
    ea_precomb_ghg = input_emissions / total_MJ
    ea_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_MJ
    ma_precomb_ghg = input_emissions / total_kg
    ma_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_kg
    dollara_precomb_ghg = input_emissions / total_dollars
    dollara_postcomb_ghg = (input_emissions + end_use_emissions + coprod_emissions) / total_dollars
    # se_precomb_ghg = (input_emissions + total_credits) / total_fuel_MJ
    # se_postcomb_ghg = (input_emissions + total_credits + end_use_emissions + coprod_emissions) / total_fuel_MJ
    
    return_list.append(ea_precomb_ghg.magnitude)
    return_list.append(ea_postcomb_ghg.magnitude)
    return_list.append(ma_precomb_ghg)
    return_list.append(ma_postcomb_ghg)
    return_list.append(dollara_precomb_ghg)
    return_list.append(dollara_postcomb_ghg)
    # return_list.append(se_precomb_ghg.magnitude)
    # return_list.append(se_postcomb_ghg.magnitude)
    
    
    output_frame = pd.DataFrame({'Energy Allocation, Pre-Combustion' : [ea_precomb_ghg.magnitude],
                                 'Energy Allocation, Post-Combustion' : [ea_postcomb_ghg.magnitude],
                                 'Mass Allocation, Pre-Combustion' : [ma_precomb_ghg],
                                 'Mass Allocation, Post-Combustion' : [ma_postcomb_ghg],
                                 'Economic Allocation, Pre-Combustion' : [dollara_precomb_ghg],
                                 'Economic Allocation, Post-Combustion' : [dollara_postcomb_ghg]})
                                 # 'System Boundary Expansion, Pre-Combustion' : [se_precomb_ghg.magnitude],
                                 # 'System Boundary Expansion, Post-Combustion' : [se_postcomb_ghg.magnitude],})
    
    
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
                                         match_list, D.LCA_GHG_impact,0,0)   # Skipped this one?         
            # print(LCA_val)                                                 # Can we think of a case where this is needed?
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(name)
                print('Replacing with 0')
                LCA_val = 0
            return_value += amount * LCA_val
        
        # Instrumentation
        # print('----', name, '----')
        # print(LCA_val)
        # print(amount)
        # print(LCA_val * amount)
        # print(return_value)
        # print('---------------')
    
    return return_value

def calcInputEmissions(tl_array, ol, fip):
    
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
                                     match_list, D.LCA_GHG_impact, ol, fip)  
        if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(name)
                print('Replacing with 0')
                LCA_val = 0
                      
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
                                         match_list, D.LCA_GHG_impact,0,0) # Don't expect to have county-to-county specific emissions data
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(name)
                print('Replacing with 0')
                LCA_val = 0
            
            return_value += amount * LCA_val
            
            # print('In the thingy')
            # print('----', name, '----')
            # print(LCA_val)
            # print(amount)
            # print(LCA_val * amount)
            # print(return_value)
            # print('---------------')
        
        # Want to have something that is much more general
        # maybe...?
        if name in D.Waste_List:
            match_list = [[D.LCA_key_str, name],
                          [D.LCA_IO, D.tl_output]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df,
                                         match_list, D.LCA_GHG_impact, 0, 0)
            
            return_value += amount * LCA_val
            # Instrumentation
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
    # print(quad_list)
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
        
        if math.isnan(amount) == True:
            amount = 0
        
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
                                     match_list, D.LCA_cost,0,0)    
        if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(name)
                print('Replacing with 0')
                LCA_val = 0
                    
        return_value += amount * LCA_val
        
        # Instrumentation
        # print('----', name, '----')
        # print(amount)
        # print(LCA_val)
        # print(return_value)
    
        
    return return_value

def calcWater(tl_array, fip, ol):
    
    return_val = 0
    
    input_subst_list = []
    input_value_list = []
    output_subst_list = []
    output_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    input_subst_list = quad_list[0]
    input_value_list = quad_list[1]
    output_subst_list = quad_list[2]
    output_value_list = quad_list[3]


def calcCriteria(tl_array, fip, ol):
    
    return_list = []
    
    Acid_total  = 0
    Eco_total   = 0
    Eutr_total  = 0
    HHC_total   = 0
    HHNC_total  = 0
    O3D_total   = 0
    O3F_total   = 0
    RD_total    = 0
    RE_total    = 0
    
    input_subst_list = []
    input_value_list = []
    
    quad_list = readtl_array(tl_array)
    
    input_subst_list = quad_list[0]
    input_value_list = quad_list[1]
    
    if len(input_subst_list) != len(input_value_list):
        print('Error - substance name list and value list of unequal length')
        return
        
    for i in range(len(input_subst_list)):
        name = input_subst_list[i]
        amount = input_value_list[i]
        
        match_list = [[D.LCA_key_str, name],
                      [D.LCA_IO, D.tl_input]]
        
        Acid_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Acidification, ol, fip)   
        if math.isnan(Acid_val) == True:
                print('Warning - No Value Present for Acidification,', name)
                pass         
        else:
            Acid_total += amount * Acid_val
            
        Eco_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Ecotoxicity, ol, fip)
        if math.isnan(Eco_val) == True:
                print('Warning - No Value Present for Ecotoxicity,', name)
                pass 
        else:
            Eco_total += amount * Eco_val
            
        Eutr_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Eutrophication, ol, fip)
        if math.isnan(Eutr_val) == True:
                print('Warning - No Value Present for Eutrophication,', name)
                pass 
        else:
            Eutr_total += amount * Eutr_val
            
        HHC_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_HHC, ol, fip)
        if math.isnan(HHC_val) == True:
                print('Warning - No Value Present for HHC,', name)
                pass
        else:
            HHC_total += amount * HHC_val
            
        HHNC_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_HHNC, ol, fip)
        if math.isnan(HHNC_val) == True:
                print('Warning - No Value Present for HHNC,', name)
                pass 
        else:
            HHNC_total += amount * HHNC_val
            
        O3D_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Ozone_Depletion, ol, fip)
        if math.isnan(O3D_val) == True:
                print('Warning - No Value Present for Ozone Depletion,', name)
                pass
        else:
            O3D_total += amount * O3D_val
            
        O3F_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Ozone_Formation, ol, fip)
        if math.isnan(O3F_val) == True:
                print('Warning - No Value Present for Ozone Formation,', name)
                pass 
        else:
            O3F_total += amount * O3F_val
            
        RD_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Resource_Depletion, ol, fip)
        if math.isnan(RD_val) == True:
                print('Warning - No Value Present for Resource Depletion,', name)
                pass 
        else:
            RD_total += amount * RD_val
            
        RE_val = UF.returnLCANumber(D.LCA_inventory_df,
                                     match_list, D.LCA_Respiratory_Effects, ol, fip)
        if math.isnan(RE_val) == True:
                print('Warning - No Value Present for Respiratory Effects,', name)
                pass 
        else:
            RE_total += amount * RE_val
        
        
        
    return [Acid_total, Eco_total, Eutr_total, HHC_total, HHNC_total, O3D_total, O3F_total, RD_total, RE_total]
