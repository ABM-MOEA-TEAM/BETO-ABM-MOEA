import TEA_LCA_Data as D
import pandas as pd

# Column Headings for Results Dataframe
substance_name = 'Substance_Name'
process_name = 'Process_Name'
input_or_output = 'In_or_out'
magnitude = 'Magnitude'
units = 'Units'

# Instantiate an empty dataframe
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
            
            if subst_str not in D.nonfunglist:
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