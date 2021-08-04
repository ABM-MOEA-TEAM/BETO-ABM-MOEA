import TEA_LCA_Data as D
import pandas as pd
import numpy as np

import csv

import os
from pathlib import Path
cwd = os.getcwd()

# Column Headings for Results Dataframe
substance_name = 'Substance_Name'
process_name = 'Process_Name'
input_or_output = 'In_or_out'
magnitude = 'Magnitude'
units = 'Units'
I_O = 'I/O'
name = 'Name'
base_value = 'Base Value'

def collectDayCentData():
    path_list = [Path(cwd + '/DayCent/tabular_results/corn-stover_county_results.csv')]    
    excel_read = pd.read_csv(path_list[0])
    return excel_read

def collectIndepVars(tab_string):
    
    path_list = [Path(cwd + '/CSU_All_Pathway_TEALCA_ACTIVE.xlsx')] # Presumably will all be in this file
    
    excel_read = pd.read_excel(path_list[0],tab_string)
    
    name_list = []
    indep_vars_list = []
    I_O_list = []
    units_list = []

    return_array = [[],[],[],[]]
    
    for i in range(len(excel_read)):
        row = excel_read.loc[i]
        name_list.append(row[name])
        indep_vars_list.append(row[base_value])
        units_list.append(row[units])
        I_O_list.append(row[I_O])
        
    return_array = [name_list,indep_vars_list,I_O_list,units_list]
    
    for i in range(len(return_array)):
            name_list = []
            val_list = []
            
            unit_list = return_array[i]
            I_O_list = return_array[i-1]
            val_list = return_array[i-2]
            name_list = return_array[i-3]
            
            quad_list = list(zip(name_list, val_list, I_O_list, unit_list))
            
            # have encountered a scenario where the shortest list is the 
            # length of the quad_list, which I worry will cut out some values
            # (haven't demonstrated this happens here)
    
    
    return quad_list

def DayCentFips():
    excel_read = collectDayCentData()
    
    DayCent_Fips = []
    
    fips = 'fips'
    
    for i in range(len(excel_read)):
        row = excel_read.loc[i]
        DayCent_Fips.append(row[fips])
        
    return_fips = []
    
    
    i = 0
    while i < len(DayCent_Fips):
        value = DayCent_Fips[i]
        return_fips.append(value)
        i += 4
    
    return return_fips


def DayCentYields(crop_selection, percent_collected_ID):
    
    excel_read = collectDayCentData()
    
    Daycent_Yields = []
    
    for i in range(len(excel_read)):
        row = excel_read.loc[i]
        Daycent_Yields.append(row[crop_selection])
        
    # if crop_selection != 'stover_yield_Mg_ha':
    #     return Daycent_Yields
    
    stover_results_raw = Daycent_Yields
    
    stover_collected = []
    
    i = 0
    if percent_collected_ID == 1:
        i = 1
    if percent_collected_ID == 2:
        i = 2
    if percent_collected_ID == 3:
        i = 3
    if percent_collected_ID >= 4:
        print('Error - 1 = 25%, 2 = 50%, 3 = 75% - Pathway ID unrecognized')
        
    while i < len(stover_results_raw):
        value = stover_results_raw[i]
        stover_collected.append(value)
        i = i + 4
    
    return stover_collected

def collectEconIndepVars(column_id):
    
    path_list = [Path(cwd + '/CSU_All_Pathway_TEALCA_ACTIVE.xlsx')]
    
    excel_read = pd.read_excel(path_list[0], 'TEA')
    
    return_list = []
    
    column_number = 0
    
    if column_id == 'Soy Biodiesel' or column_id == 0:
        column_number = 1
    
    if column_id == 'Soy Jet':
        column_number = 2
        
    if column_id == 'Corn Grain EtOH':
        column_number = 3
    
    if column_number == 0:
        print('Error - unrecognized column ID string')
        
    Operating_Capacity_Row = excel_read.loc[13]
    Discount_Rate_Row = excel_read.loc[14]
    Tax_Rate_Row = excel_read.loc[15]
    Equity_Share_Row = excel_read.loc[16]
    Interest_Rate_Row = excel_read.loc[17]
    Loan_Term_Row = excel_read.loc[18]
    Maintenance_Rate_Row = excel_read.loc[19]
    Insurance_Rate_Row = excel_read.loc[20]
    Depreciable_Amount_Row = excel_read.loc[21]
    Tax_Credit_Row = excel_read.loc[22]
    Salvage_Row = excel_read.loc[23]
    
    
    return_list.append(Operating_Capacity_Row[column_number])
    return_list.append(Discount_Rate_Row[column_number])
    return_list.append(Tax_Rate_Row[column_number])
    return_list.append(Equity_Share_Row[column_number])
    return_list.append(Interest_Rate_Row[column_number])
    return_list.append(Loan_Term_Row[column_number])
    return_list.append(Maintenance_Rate_Row[column_number])
    return_list.append(Insurance_Rate_Row[column_number])
    return_list.append(Depreciable_Amount_Row[column_number])
    return_list.append(Tax_Credit_Row[column_number])
    return_list.append(Salvage_Row[column_number])
    
    return return_list

# Instantiate an empty datafram
def createEmptyFrame():
    # Data structure to store all results
    return pd.DataFrame({substance_name : [], process_name : [], 
                        input_or_output : [], magnitude : [],
                        units : []})
# Indice variables
empty_frame = createEmptyFrame()
substance_idx = list(empty_frame.columns).index(substance_name)
process_idx = list(empty_frame.columns).index(process_name)
IO_idx = list(empty_frame.columns).index(input_or_output)
mag_idx = list(empty_frame.columns).index(magnitude)
units_idx = list(empty_frame.columns).index(units)
col_count = len(list(empty_frame.columns))

# Column Headings for Summary Results Dataframe
state_name_col = 'State_Name'
avg_yield_col = 'Average_Yield'
eroi_col = 'EROI'


def Collect_IndepVars_Loop(tab_string, yield_value, geospatial_indicator,
                           downstream_indicator, tl_array, input_substance_string,
                           step_ID, DayCent_read_string, fips):
# This needs to be decentralized and cleaned up. Ideally, I would find a work around
# for the gross nested-if statement logic (7/1)    
    
    yield_input_list = []

# Identify the step - cultivation, conversion or upgrading from the given argument
# This gets passed on to the nested if logic loop (the big boolean rats nest)
    if step_ID == 0:
        which_step = D.biomass_production
    if step_ID == 1:
        which_step = D.conv
    if step_ID == 2:
        which_step = D.upgrading
    if step_ID != 0 and step_ID != 1 and step_ID != 2:
        print('Error - Expected final argument (step_ID) to be 0, 1, or 2')
        print('0 --------- Biomass Production Step')
        print('1 --------- Conversion/Extraction Step')
        print('2 --------- Upgrading Step')
        return
      
    return nested_if_logic(tab_string, yield_value, geospatial_indicator, 
                           downstream_indicator, tl_array, input_substance_string,
                           which_step, DayCent_read_string, fips)

def nested_if_logic(tab_string, yield_value, geospatial_indicator, 
                           downstream_indicator, tl_array, input_substance_string,
                           which_step, DayCent_read_string, fips):
   
    ################## DOWNSTREAM NESTED IF LOGIC ######################
    
    # If indicator is engaged, you will need to read the given tl_array to find
    # some particular substance (the feedstock) and its amount. I think this is
    # the only real difference in the two branches.  A good place to begin with 
    # edits could be to merge the two branches somehow (might not be easy to do
    # with the numerous different unit types that appear in cult or conversion)
    # (7/1)
    
    # Disagree with this more and more that I think about it. The cultivation 
    # and downstream steps are just a bit different in terms of the independent
    # parameters which we feed them (most cultivation is a fixed amount, most
    # downstream indepvars are scales against the feedstock amount)
    
    if downstream_indicator == 1:

        # Create Match_List ID with given substance input string 
        match_list = [[input_or_output, D.tl_output],
                     [substance_name, input_substance_string]] 
        
        # Grab the amount of that input substance (used for scaling later)
        input_substance_amount = returnPintQty(tl_array, match_list) 
        
        # Executes loop above to grab all relevant rows from All_PW's
        # vars_list = collectIndepVars(tab_string)
        
        quad_list = collectIndepVars(tab_string) 
        return_array = createEmptyFrame()
        output_name_list = []
        output_value_list = []
        output_units_list = []
        
        output_name_list.append(input_substance_string)
        output_value_list.append(input_substance_amount)
        output_units_list.append('kg/yr')


        i = 0
    
        scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
                                            output_units_list[0])
        return_array.loc[0] = getWriteRow(output_name_list[0], which_step,
                                            D.tl_input, scale0.qty)
        
        Main_Substance_Amount = input_substance_amount
        
        i = 1
        j = 0

        while j < len(quad_list):
            
            skip_ind = 0
            rows = quad_list[j]
            
            if rows[2] == 'In' and rows[3] == 'dollars/yr':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty)
                i += 1
            
                
            if rows[2] == 'In' and rows[3] == 'dollars/kg Feedstock':
              
                if rows[0] == 'Labor': # As the other two $'s are not /yr
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'dollars/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount)
                    i += 1
                    
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'dollars*yr/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty
                                                *Main_Substance_Amount)
                    i += 1
            
            if rows[2] == 'In' and rows[3] == 'MJ/yr':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty) 
                i += 1    
            
            if rows[2] == 'In' and rows[3] == 'kg/kg Feedstock':
                if rows[0] == 'LNG':
                    
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*
                                                Main_Substance_Amount/D.HHV_dict['LNG'].qty) 
                    i += 1
                
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'kg/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*
                                                Main_Substance_Amount)    
                    i += 1
            
            if rows[2] == 'In' and rows[3] == 'm3/kg Feedstock':
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'m**3/kg')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*
                                            Main_Substance_Amount) 
                i += 1
                
            if rows[2] == 'In' and rows[3] == 'MJ/kg Feedstock':
                
                if rows[0] == 'LNG':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'MJ/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*Main_Substance_Amount/D.HHV_dict['LNG'].qty)
                    skip_ind = 1

                    
                if rows[0] == 'Natural Gas':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'MJ/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount/D.HHV_dict['Natural Gas'].qty)
                    skip_ind = 1
                    
                    
                elif skip_ind != 1:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'MJ/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount) 
                    # print('triggered')

                i += 1
                
            if rows[2] == 'Out' and rows[3] == 'kg/kg Feedstock':
                if rows[0] == 'Ethanol' and tab_string == 'StarchFerm':
                    
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1]+0.014532693,'')   
                    # Need to include the Gasoline Denaturant. Not sure how to 
                    # address this at all..
                    
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                    D.tl_output, scale_value.qty*
                                                    Main_Substance_Amount) 
                    i += 1
                
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                    D.tl_output, scale_value.qty*
                                                    Main_Substance_Amount) 
                    i += 1
            j += 1
    
        return return_array
  
 ###################### GEOSPATIAL DATA LOGIC ########################
    
 # This block will mimic the behavior of the Cultivation Nested If Logic (below)
 # with the exception of where it pulls the yield value from; this block will
 # take in an expected productivity value, whereas the block below will pull
 # the productivity from the CSU_All_PW's_File
    
    if geospatial_indicator == 1:
        
        quad_list = collectIndepVars(tab_string) 
        #print(quad_list)
        size = 0  # ! Need to change this to pull from excel sheet
        return_array = createEmptyFrame()
        output_name_list = []
        output_value_list = []
        output_units_list = []
        stover_collection_percentage = 0
        
        # While loop runs through the list of quads to grab the ha's & outputs 
        
        i = 0
        while i < len(quad_list):
            rows = quad_list[i]
            if rows[0] == 'Stover Collected':
                stover_collection_percentage = rows[1]
            if rows[2] == 'Out':
                  output_name_list.append(rows[0])
                  output_value_list.append(rows[1])
                  output_units_list.append(rows[3])
            if rows[3] == 'ha':
                size = D.TEA_LCA_Qty(D.substance_dict['Land Area'], rows[1], 'hectare')
            i += 1
            
        
        if len(output_name_list) == 0:
            print('Error - No Out Substances Found From Excel Sheet')
            return
        if size == 0:
            print('Error - No land Area Argument Detected, expects ha')
            return 
        if tab_string == 'CornCult' and stover_collection_percentage == 0:
            print('Error - expected non-zero argument for stover collection %')
        
        i = 0
        
        scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]], yield_value,
                                            output_units_list[0])        
        return_array.loc[0] = getWriteRow(output_name_list[0], which_step,
                                            D.tl_output, scale0.qty*size.qty)
        i = i + 1
        
        if len(output_name_list) >= 2:
            
            if output_name_list[1] == 'Corn Stover':
                
                scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[1]],output_value_list[1],
                                            output_units_list[1])        
                return_array.loc[1] = getWriteRow(output_name_list[1], which_step,
                                                    D.tl_output, scale1.qty*size.qty
                                                    *stover_collection_percentage/100)
                corn_stover_yield = scale1.qty*size.qty*(stover_collection_percentage/100)
            
            else:
                
                scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[1]],output_value_list[1],
                                                output_units_list[1])        
                return_array.loc[1] = getWriteRow(output_name_list[1], which_step,
                                                    D.tl_output, scale1.qty*size.qty)
            i = i + 1
        
        Main_Substance_Amount = scale0.qty*size.qty
        
        j = 0
    
        while j < len(quad_list):
            rows = quad_list[j]
            if rows[2] == 'In' and rows[3] == 'kg/ha/yr':
                
                if rows[0] == 'Corn Stover':
                    print('Youre in the weird corn stover exception statement')
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*size.qty)
                    
                else:
                    
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*size.qty)
                i += 1
            
            if rows[2] == 'In' and rows[3] == 'dollars/ha/yr':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
                i += 1
            
            if rows[2] == 'In' and rows[3] == 'dollars/ha':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
                i += 1
                
            if rows[2] == 'In' and rows[3] == 'dollars/kg Feedstock':
              
                if rows[0] == 'Labor': # As the other two $'s are not /yr
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'dollars/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount)
                    i += 1
                    
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'dollars*yr/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty
                                                *Main_Substance_Amount)
                    i += 1
            
            if rows[2] == 'In' and rows[3] == '#/ha/yr':
                if rows[0] == 'Soybean Seed':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1]*0.00194595,'kg/ha/yr')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*size.qty) 
                
                if rows[0] == 'Corn Seed':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'],
                                            rows[1]/1695.433,'kg/ha/yr')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*size.qty)
                    
                if rows[0] == 'Rhizome Plugs':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'ha**-1/yr')  # Need a guess on the mass of 1 plug
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
                i += 1
            
            if rows[2] == 'In' and rows[3] == 'MJ/ha/yr':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty) 
                i += 1    
            
            if rows[2] == 'In' and rows[3] == 'kg/kg Feedstock':
                if rows[0] == 'LNG':
                    print(i)
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*
                                                Main_Substance_Amount*D.HHV_dict['LNG'].qty) 
                    i += 1
                    
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                                rows[1],'kg/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                                D.tl_input, scale_value.qty*
                                                Main_Substance_Amount)    
                    i += 1
            
            if rows[2] == 'In' and rows[3] == 'm3/ha/yr':
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'m**3/ha/yr')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty) 
                i += 1
                
            if rows[2] == 'In' and rows[3] == 'MJ/kg Feedstock':
                
                if rows[0] == 'LNG':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount/D.HHV_dict['LNG'].qty) 
                else:
                    scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'MJ/kg')
                    return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount) 
                i += 1
            
            if rows[3] == '%':
                if tab_string == 'CornCult' and rows[0] == 'Carbon Content':
                    
                    carbon_content = rows[1]
                    value = ((carbon_content/100)*(44/12)*(Main_Substance_Amount + corn_stover_yield))
                    return_array.loc[i] = getWriteRow('CO2, Atmospheric', which_step,
                                            D.tl_input, ((carbon_content/100)*(44/12)
                                                          *(Main_Substance_Amount + corn_stover_yield)))
                   
                if tab_string != 'CornCult':
                    scale_value = D.TEA_LCA_Qty(D.substance_dict['CO2, Atmospheric'],
                                                rows[1],'kg/kg')
                    return_array.loc[i] = getWriteRow('CO2, Atmospheric', which_step,
                                                D.tl_input, (44/12)*scale_value.qty
                                                *Main_Substance_Amount/100) 
    
                i += 1    
            
            j += 1
        return return_array

      
 ################## CULTIVATION NESTED IF LOGIC ######################   
 
 # Point is that this portion of the loop cannot be reached if the downstream
 # indicator is engaged.  This constitutes the second branch of the loop
 
 
    quad_list = collectIndepVars(tab_string)
    # print(quad_list)
    
    size = 0  # ! Need to change this to pull from excel sheet
    return_array = createEmptyFrame()
    output_name_list = []
    output_value_list = []
    output_units_list = []
    stover_collection_percentage = 0
    
    # While loop runs through the list of quads to grab the ha's & outputs 
    
    i = 0
    while i < len(quad_list):
        rows = quad_list[i]
        if rows[0] == 'Stover Collected':
            stover_collection_percentage = rows[1]
        if rows[2] == 'Out':
              output_name_list.append(rows[0])
              output_value_list.append(rows[1])
              output_units_list.append(rows[3])
        if rows[3] == 'ha':
            size = D.TEA_LCA_Qty(D.substance_dict['Land Area'], rows[1], 'hectare')
        i += 1
        
    
    if len(output_name_list) == 0:
        print('Error - No Out Substances Found From Excel Sheet')
        return
    if size == 0:
        print('Error - No land Area Argument Detected, expects ha')
        return 
    if tab_string == 'CornCult' and stover_collection_percentage == 0:
        print('Error - expected non-zero argument for stover collection %')
    
    i = 0
    
    # scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
    #                                     output_units_list[0])        
    # return_array.loc[0] = getWriteRow(output_name_list[0], which_step,
    #                                     D.tl_output, scale0.qty*size.qty)
    # i += 1
    
    if len(output_name_list) >= 2:
        
        for j in range(len(output_name_list)):
            
            if output_name_list[j] == 'Corn Stover':            
                
                scale1 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[j]],output_value_list[j],
                                            output_units_list[j])        
                return_array.loc[i] = getWriteRow(output_name_list[j], which_step,
                                                    D.tl_output, scale1.qty*size.qty
                                                    *stover_collection_percentage/100)
                corn_stover_yield = scale1.qty*size.qty*(stover_collection_percentage/100)
                i += 1
                # print('1')
            
            if output_name_list[j] == 'Corn Grain' or output_name_list[j] == 'Soybeans':
              
                scale0 = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], output_value_list[j],
                                            output_units_list[j])
                return_array.loc[0] = getWriteRow(output_name_list[0], which_step,
                                        D.tl_output, scale0.qty*size.qty)
                i += 1
                # print('2')
                
            if (output_name_list[j] != 'Corn Grain' and
                output_name_list[j] != 'Corn Stover' and
                output_name_list[j] != 'Soybeans'):

                scale = D.TEA_LCA_Qty(D.substance_dict[output_name_list[j]],output_value_list[j],
                                                output_units_list[j])        
                return_array.loc[i] = getWriteRow(output_name_list[j], which_step,
                                                D.tl_output, scale.qty*size.qty)
                i += 1
                # print('3')
    
    # if len(output_name_list) >= 2:
        
    #     for j in range(len(output_name_list)):
            
    #         if output_name_list[j] == 'Corn Grain':
                
            
    
    else:
        scale0 = D.TEA_LCA_Qty(D.substance_dict[output_name_list[0]],output_value_list[0],
                                        output_units_list[0])        
        return_array.loc[0] = getWriteRow(output_name_list[0], which_step,
                                        D.tl_output, scale0.qty*size.qty)
        i += 1
    
    Main_Substance_Amount = scale0.qty*size.qty
    
    j = 0

    while j < len(quad_list):
        rows = quad_list[j]

        if rows[2] == 'External In' and rows[0] == 'Hexane Loss':
            
            col_title = 'Practice Set (Python)'  # Will then change this to be electricity
                                                 # when we have that column populated, and so on
            
            # Best would be to reference the list title with the row name, but don't know if we
            # will be clean enough on the excel end to be able to rely on that being correct...
            
            data_set = External_Data(col_title)
            value = 0
            
            for i in range(len(data_set)):
                data_row = data_set[i]
                if data_row[0] == fips:
                    value = data_row[1]
            if value == 0:
                print('Error - could not find matching FIP')
            
            #print(value)
            scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],value,rows[3])
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty)
            i += 1
        
        if rows[2] == 'In' and rows[3] == 'kg/ha/yr':
            
            if rows[0] == 'Corn Stover':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
                
            else:
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
            i += 1
            
        # And now a million exceptions for different unit types
        
        if rows[2] == 'In' and rows[3] == 'dollars/ha/yr':
            
            scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],rows[1],rows[3])
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty*size.qty)
            i += 1
        
        if rows[2] == 'In' and rows[3] == 'dollars/ha':
            
            scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],rows[3])
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty*size.qty)
            i += 1
            
        if rows[2] == 'In' and rows[3] == 'dollars/kg Feedstock':
          
            if rows[0] == 'Labor': # As the other two $'s are not /yr
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'dollars/kg')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty
                                        *Main_Substance_Amount)
                i += 1
                
            else:
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'dollars*yr/kg')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty
                                            *Main_Substance_Amount)
                i += 1
        
        if rows[2] == 'In' and rows[3] == '#/ha/yr':
            if rows[0] == 'Soybean Seed':
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1]*0.00194595,'kg/ha/yr')
                return_array.loc[i] = getWriteRow(rows[3], which_step,
                                            D.tl_input, scale_value.qty*size.qty) 
            
            if rows[0] == 'Corn Seed':
                scale_value = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'],
                                        rows[1]/1695.433,'kg/ha/yr')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*size.qty)
                
            if rows[0] == 'Rhizome Plugs':
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'ha**-1/yr')  # Need a guess on the mass of 1 plug
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty*size.qty)
            i += 1
        
        if rows[2] == 'In' and rows[3] == 'MJ/ha/yr':
            
            scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                    rows[1],rows[3])
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty*size.qty) 
            i += 1    
        
        if rows[2] == 'In' and rows[3] == 'kg/kg Feedstock':
            if rows[0] == 'LNG':
                
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*
                                            Main_Substance_Amount*D.HHV_dict['LNG'].qty) 
                i += 1
                
            else:
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                            rows[1],'kg/kg')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                            D.tl_input, scale_value.qty*
                                            Main_Substance_Amount)    
                i += 1
        
        if rows[2] == 'In' and rows[3] == 'm3/ha/yr':
            scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                        rows[1],'m**3/ha/yr')
            return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty*size.qty) 
            i += 1
            
        if rows[2] == 'In' and rows[3] == 'MJ/kg Feedstock':
            
            if rows[0] == 'LNG':
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                    rows[1],'')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty
                                        *Main_Substance_Amount/D.HHV_dict['LNG'].qty) 
            else:
                scale_value = D.TEA_LCA_Qty(D.substance_dict[rows[0]],
                                    rows[1],'MJ/kg')
                return_array.loc[i] = getWriteRow(rows[0], which_step,
                                        D.tl_input, scale_value.qty
                                        *Main_Substance_Amount) 
            i += 1
        
        if rows[3] == '%':
            if tab_string == 'CornCult' and rows[0] == 'Carbon Content':
                
                carbon_content = rows[1]
                value = ((carbon_content/100)*(44/12)*(Main_Substance_Amount + corn_stover_yield))
                return_array.loc[i] = getWriteRow('CO2, Atmospheric', which_step,
                                        D.tl_input, ((carbon_content/100)*(44/12)
                                                      *(Main_Substance_Amount + corn_stover_yield)))
               
            if tab_string != 'CornCult':
                scale_value = D.TEA_LCA_Qty(D.substance_dict['CO2, Atmospheric'],
                                            rows[1],'kg/kg')
                return_array.loc[i] = getWriteRow('CO2, Atmospheric', which_step,
                                            D.tl_input, (44/12)*scale_value.qty
                                            *Main_Substance_Amount/100) 

            i += 1    
        
        j += 1
            
    return return_array

def External_Data(col_title):
    
    path_list = [Path(cwd + '/CSU_All_Pathway_TEALCA_ACTIVE.xlsx')]
    
    excel_read = pd.read_excel(path_list[0],'GeoInputs')
    
    value_list = []
    fips_list = []
    
    for i in range(len(excel_read)):
        row = excel_read.loc[i]
        value_list.append(row[col_title])
        fips_list.append(row['FIPS'])
        
    return_list = list(zip(fips_list, value_list))

    return return_list

# Instantiate an empty dataframe
def createEmptySummaryFrame():
    # Data structure to store all results
    return pd.DataFrame({state_name_col : [], avg_yield_col : [],
                         eroi_col : []})

# Helper functions
def returnConvertedMagnitude(qty, output_units):
    converted_qty = qty.to(output_units)
    return converted_qty.magnitude

def returnPintQty(tl_array, match_list):
    return_obj = 'Found zero or multiple rows'
    num_pairs = len(match_list)
    query_str = ''
    for i in range(num_pairs):
        if i == (num_pairs-1):
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '"'
        else:
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '" and '
        #print(query_str)
    rows = tl_array.query(query_str)
    if len(rows) == 1:
        row_vals = list(rows.loc[list(rows.index)[0]])
        return_obj = row_vals[mag_idx] * D.ureg.parse_expression(row_vals[units_idx])
            
    return return_obj

def returnLCANumber(df, match_list, desired_col_name):
    return_obj = 0
    num_pairs = len(match_list)
    query_str = ''
    for i in range(num_pairs):
        if i == (num_pairs-1):
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '"'
        else:
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '" and '
    
    rows = df.query(query_str)
    if len(rows) == 1:
        return_obj = rows.iloc[0][desired_col_name]
    else:
        # print('LCA query returned no value')
        pass
            
    return return_obj

def returnProdlist(pathname):
    prodlist = []
    return_list = []        
    
    prods = 'Product'
    products_listed = pd.read_csv(pathname)
    
    for i in range(len(products_listed)):
        row = products_listed.loc[i]
        prodlist.append(row[prods])
 
    for i in range(len(products_listed)):
        row = prodlist[i]
        isnull_query = pd.isnull(row)
        if isnull_query == False:
            return_list.append(row)
    return return_list

def returnCoProdlist(pathname):
    coprodlist = []
    
    coprods = 'Co-products'
    coprods_list = pd.read_csv(pathname)
    
    for i in range(len(coprods_list)):
        row = coprods_list.loc[i]
        coprodlist.append(row[coprods])
        
    return coprodlist

def returnListOfPintQtys(tl_array):
    return_list = []
    for i in range(len(tl_array)):
        row_vals = list(tl_array.loc[list(tl_array.index)[i]])
        return_list.append(D.returnPintQtyObj(row_vals[mag_idx], row_vals[units_idx]))
    return return_list

def sumQtysWhere(match_list, tl_array):
    num_pairs = len(match_list)
    query_str = ''
    for i in range(num_pairs):
        if i == (num_pairs-1):
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '"'
        else:
            query_str += match_list[i][0] + ' == "' + match_list[i][1] + '" and '
    
    rows = tl_array.query(query_str)
            
    return_obj = D.returnPintQtyObj(0.0, 'dimensionless')
    if (len(rows) > 0):
        pint_qtys = returnListOfPintQtys(rows)
        return_obj = D.returnPintQtyObj(0.0, format(pint_qtys[0].units))
        for qty in pint_qtys:
            return_obj = return_obj + qty
    return return_obj

def sumProcessIO(df, process_name_val, in_or_out_val):
    query_str = process_name + ' == "' + process_name_val + '" and ' + input_or_output + ' == "' + in_or_out_val + '"'
    rows = df.query(query_str)
    return rows.sum(axis = 0, skipna = True)[magnitude]

def getWriteRow(subst, proc, in_out, pint_qty):
    write_row = col_count * [0]
    write_row[substance_idx] = subst
    write_row[process_idx] = proc
    write_row[IO_idx] = in_out
    write_row[mag_idx] = pint_qty.magnitude
    write_row[units_idx] = format(pint_qty.units)
    return write_row

def consolidateIO(multistep_array):
    return_array = createEmptyFrame()
    row_count = 0
    for subst_str in D.substance_dict.keys():
        if subst_str in multistep_array.iloc[:,substance_idx].values:
            match_list_1 = [[input_or_output, D.tl_output],
              [substance_name, subst_str]]
            sum_outputs = sumQtysWhere(match_list_1, multistep_array)
            match_list_2 = [[input_or_output, D.tl_input],
              [substance_name, subst_str]]
            sum_inputs = sumQtysWhere(match_list_2, multistep_array)
            
            if subst_str not in D.DoNotConsolidateList:
                # if fungible, sum outputs and substract sum of inputs
                # if value is positive, write to outputs
                # if value is negative, write abs val to inputs   
                
                # This net_val logic is bad but seems to work fine.
                net_val = D.returnPintQtyObj(0, 'dimensionless')
                if format(sum_outputs.units) != format(sum_inputs.units):
                    # units are not the same
                    if sum_outputs.magnitude == 0:
                        net_val = D.returnPintQtyObj(-1, 'dimensionless') * sum_inputs
                    elif sum_inputs.magnitude == 0:
                        net_val = sum_outputs
                    else:
                        print('Units disagreement and non-zero values are potentially being lost '
                              + subst_str)
                else:
                    # this is possible because we know the units are the same
                    net_val = sum_outputs - sum_inputs
                    
                if net_val.magnitude > 0:
                    # report as output
                    return_array.loc[row_count] = getWriteRow(
                        subst_str, D.cons, 
                        D.tl_output, net_val)
                    row_count += 1
                elif net_val.magnitude == 0:
                    return_array.loc[row_count] = getWriteRow(
                        subst_str, D.cons, 
                        D.zeroed, net_val)
                    row_count += 1
                else:
                    # report as input, value is negative
                    return_array.loc[row_count] = getWriteRow(
                        subst_str, D.cons, 
                        D.tl_input, net_val*D.returnPintQtyObj(-1, 'dimensionless'))
                    row_count += 1
            else:
                # if not fungible, sum outputs, sum inputs, report two line items
                # write outputs
                if sum_outputs.magnitude != 0:
                    return_array.loc[row_count] = getWriteRow(
                                        subst_str, D.cons, 
                                        D.tl_output, sum_outputs)
                    row_count += 1
                # write inputs
                if sum_inputs.magnitude != 0:
                    return_array.loc[row_count] = getWriteRow(
                                        subst_str, D.cons, 
                                        D.tl_input, sum_inputs)
                    row_count += 1
                
    return return_array

def randomizeIO(input_IO_array, distribution_type_list):
    return_array = createEmptyFrame()
    for i in range(len(input_IO_array)):
        row_vals = input_IO_array.loc[i]
        flow_magnitude = row_vals[magnitude]
        sampled_magnitude = (flow_magnitude + (distribution_type_list[0].std_dev * 
                                               flow_magnitude) * np.random.standard_normal())
        row_units = row_vals[units]
        return_array.loc[i] = getWriteRow(row_vals[substance_name], row_vals[process_name], 
            row_vals[input_or_output], D.returnPintQtyObj(sampled_magnitude, row_units))
        
    return return_array
        