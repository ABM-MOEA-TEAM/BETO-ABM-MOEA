# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 12:48:35 2021

@author: Jack Smith
"""

import os
from pathlib import Path
import pandas as pd

import olca

cwd = os.getcwd()
client = olca.Client(8080)

path_list = [Path(cwd + '/ImpactResults.xlsx'), 
             Path(cwd + '/CSU_All_Pathway_TEALCA_ACTIVE.xlsx'),
             Path(cwd + '/LifeCycleHold.xlsx')]

method = 'TRACI [v2.1, February 2014]'
# method = 'TRACI'
# process_string = 'butene production, mixed | butene, mixed | APOS, S'
# UUID = '758a20f5-4c5b-37ec-814f-1a0c1e0aec00'

# process_string = 'bark chips production, hardwood, at sawmill | bark | APOS, S'
process_string = 'electricity, high voltage, production mix | electricity, high voltage | APOS, S'
# process_string = 'market for maintenance, electric bicycle | maintenance, electric bicycle | Cutoff, U'
# UUID = 'a72b5b5d-0d3b-3f29-8c1d-1c3620aa469f'
UUID = '5510474f-0212-32d9-8699-7a00f9dbc6ac'
# UUID = 'a2b1d953-bafb-34a0-b01e-63af53104e11'

process_string_list = ['linseed production | linseed | Cutoff, S',
                       'dichloropropene to generic market for pesticide, unspecified | pesticide, unspecified | Cutoff, S',
                       'maize grain production | maize grain | Cutoff, S']

def storeImpacts(method, process_string_list):
    
    ACD = []
    ECO = []
    EUT = []
    GWP = []
    HHC = []
    HNC = []
    O3D = []
    O3F = []
    RDP = []
    RSP = []
    name_list = []
    
    for i in range(len(process_string_list)):
        
        process_string = process_string_list[i]
        print(process_string)
        
        impact_results = getImpacts(method, process_string)
        
        acd = impact_results[0][1]
        eco = impact_results[1][1]
        eut = impact_results[2][1]
        gwp = impact_results[3][1]
        hhc = impact_results[4][1]
        hnc = impact_results[5][1]
        o3d = impact_results[6][1]
        o3f = impact_results[7][1]
        rdp = impact_results[8][1]
        rsp = impact_results[9][1]
        
        ACD.append(acd)
        ECO.append(eco)
        EUT.append(eut)
        GWP.append(gwp)
        HHC.append(hhc)
        HNC.append(hnc)
        O3D.append(o3d)
        O3F.append(o3f)
        RDP.append(rdp)
        RSP.append(rsp)
        name_list.append(process_string)
        
    
    print('out of for loop')
    writer = pd.DataFrame([ACD,ECO,EUT,GWP,HHC,HNC,O3D,O3F,RDP,RSP])
    print(writer)
    writer.to_excel(path_list[2])
    
    return

def getImpacts(method, process_string):
    
    # create the calculation setup
    setup = olca.CalculationSetup()
    
    # Now we define the type of calculation to be performed
    # see http://geendelta.github.io/olca-schema/html/CalculationType.html
    
    setup.calculation_type = olca.CalculationType.CONTRIBUTION_ANALYSIS
    
    # Select the impact method
    setup.impact_method = client.find(olca.ImpactMethod, method)
    
    
    # Determine if a product system exists in the OpenLCA env.
    
    print('Initializing Contribution Analysis')
    print('Searching for Product System...')
    
    null_comparison_obj = None
    setup.product_system = client.find(olca.ProductSystem, process_string)
    print('...')
    
    if type(setup.product_system) == type(null_comparison_obj):
        print('No Product System Exists - Constructing...')
        
        client.create_product_system(UUID)
        print('Constructed')
        setup.product_system = client.find(olca.ProductSystem, process_string)
        print('')
    
    print('Executing Impact Analysis...')
        
    # setup.parameter_redefs = client.find(olca.Location, 'GLO')
    
    # define the 'amount' variable in setup
    # This is the function unit of the syste, 
    # note that the unit of the flow system may also be defined. 
    
    setup.amount = 1.0
    
    results = client.calculate(setup)
    
    print('...')
    
    client.excel_export(results, 'ImpactResults.xlsx')
    
    output = pd.read_excel(path_list[0], 'Impacts')
    
    return output

def formatOutput():
    
    excel_read = getImpacts(method, process_string)
    
    output_name = []
    output_vals = []
    output_unit = []
    
    for i in range(1,11):
        output_vals.append(excel_read.loc[i][4])
        output_unit.append(excel_read.loc[i][3])
        output_name.append(excel_read.loc[i][2])
    
    return_obj = []
    
    for j in range(10):
        return_obj.append([output_name[j],output_vals[j],output_unit[j]])
      
    print(return_obj)
    return return_obj