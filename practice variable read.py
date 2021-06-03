# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 12:52:45 2021

@author: Jack Smith
"""
import pandas as pd
import pint
import os
from pathlib import Path
cwd = os.getcwd()
ureg = pint.UnitRegistry()
ureg.define('dollars = [money]')

import TEA_LCA_Data as D
import UnivFunc as UF

import TEA
import LCA

# Initializes empty output table
results_array = UF.createEmptyFrame()

path_list = [Path(cwd + '/soy_biodiesel_variables_practice.xlsx')]

worksheet_read = pd.read_excel(path_list[0])


values = []
substance = []
rows = UF.createEmptyFrame()

for i in range(len(worksheet_read)):
    
    row = worksheet_read.loc[i]
    print(row)
    # rows = D.TEA_LCA_Qty(D.substance_dict[worksheet_read.loc[i,'key_str']],
    #                                    worksheet_read.loc[i,'value'], 
    #                                    worksheet_read.loc[i,'default_units'])

def grow_soy_practice(worksheet_read):
    
    return_array = UF.createEmptyFrame()
    values = []
    substances = []
        
    # for i in range(len(worksheet_read)):
        
    #     rows = D.TEA_LCA_Qty(D.substance_dict[worksheet_read.loc[i,'key_str']],
    #                                  worksheet_read.loc[i,'value'], 
    #                                  worksheet_read.loc[i,'default_units'])
       
    #     values.append(rows.qty)
    #     substances.append(rows.substance)
    #     # return_array.loc[i] = UF.getWriteRow(worksheet_read.loc[i,'key_str'],
    #     #                        worksheet_read.loc[i,'process_step'], 
    #     #                        worksheet_read.loc[i,'i_o'],
    #     #                        value.loc[i])
    
    return values
# Get [short] list of substances that are NOT fungible, depends on LCA Inventory
# sub_list = []
# nonfunglist = []
# for i in range(len(LCA_inventory_df)):
#     row = LCA_inventory_df.loc[i]
#     if row[LCA_key_str] in sub_list:
#         nonfunglist.append(row[LCA_key_str])
#     else:
#         sub_list.append(row[LCA_key_str])
