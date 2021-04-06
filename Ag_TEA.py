# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:20:36 2021

@author: Jack Smith
"""

import scipy.optimize as s_opt
import TEA_LCA_Data as D
import UnivFunc as UF

# This module contains the Agriculture-Only Techno-Economic Analysis block.
# It is almost exactly the same as the TEA.py file

yrs = 30 # Time horizon for farm breakeven?

# NPV_goal function determines 30 year net-present value output for some 
# selected MCSP - this routine is run numerous times during the "optimize" func

def NPV_goal(MCSP, fopex, depreciation, loanint, ecovar, invequityshare,
             loanpay, tl_array):

    #Coproducts List (Only Crops for Ag-Only Executions)
    switchgrass_out = 0
    corn_grain_out = 0
    soybean_out = 0
    corn_stover_out = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        in_or_out = row_vals[UF.input_or_output]
        subst_name = row_vals[UF.substance_name]

    # _________________________________AG-PRODUCTS_________________________________
    
        if 'Woody Biomass' in subst_name and in_or_out == D.tl_output:
            switchgrass_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Woody Biomass'],     # Should probably build this out elsewhere as well
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Corn Grain' in subst_name and in_or_out == D.tl_output:
            corn_grain_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Grain'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
            
        if 'Soybeans' in subst_name and in_or_out == D.tl_output:
            soybean_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Soybeans'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Corn Stover Collected' in subst_name and in_or_out == D.tl_output:
            corn_stover_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Stover Collected'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        # Leaving out stover currently as I have no idea how we are going to approach; 
        # are we considering stover just to be an additional free resource?
        # Are we going to assume that the farmers expect some value back from the stover? 
    
    # This conditional covers the case of Grain/Stover in tandem
    
    if corn_stover_out != 0 and corn_grain_out != 0:
        
        crop_yield = corn_stover_out        # and we need to perform allocation
        
    else:
        crop_yield = switchgrass_out + corn_grain_out + soybean_out + corn_stover_out
        
    annrevenue = MCSP * crop_yield

    #calculating net income
    netincome = []
    years = int(yrs)
    i = 0
    
    while i < years:
        netincome.append (annrevenue - fopex -depreciation [i] -loanint [i])
        i += 1
    
    #calculating losses forward and taxable income
    lossforward = []
    taxincome = [0]
    i = 0
    
    while i < years:
        if taxincome [i] < 0:
            lossforward.append (taxincome [i])
        else:
            lossforward.append (0)
        taxincome.append (lossforward [i] + netincome [i])
        i += 1
    taxincome.pop(0)
    
    #calculating income tax
    
    i = 0
    incometax = []
    while i < years:
        if taxincome [i] < 0:
            incometax.append (0)
        else:
            incometax.append (taxincome [i] * ecovar['t'])
        i += 1
    # calculating cash flow
    cashflow = [-invequityshare]
    i = 1
    
    while i < years + 1:
        cashflow.append (annrevenue - fopex - loanpay [i-1] - incometax [i-1])
        i += 1 
    
    # calculating discounted cash flow
    disccashflow = []
    i = 0
    
    while i < years + 1:
        disccashflow.append (cashflow [i]/(1+ecovar['disc rate'])**i)
        i += 1
    
    # calculating cumulative discounted cash flow
    cumdisccashflow = [disccashflow [0]]
    
    i = 1
    
    while i < years + 1:
        cumdisccashflow.append (cumdisccashflow [i - 1] + disccashflow [i])
        i += 1
    
    # NPV retrieval from cumulative discounted cash flow
    npv = cumdisccashflow
    
    # print(abs(npv[-1]))
    return abs(npv[-1])

def calc_MCSP(tl_array):
    
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Capital Cost']])
    capex =   capex_qty.magnitude + land_cost_qty.magnitude  #inputs ['capex']
    labor =  UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude
    
    # Added another loop for determining proper ratio between corn/stover
    
    corn_grain_out = 0
    corn_stover_out = 0
    mass_allocation_ratio = 1
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        in_or_out = row_vals[UF.input_or_output]
        subst_name = row_vals[UF.substance_name]
    
        if 'Corn Grain' in subst_name and in_or_out == D.tl_output:
                corn_grain_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Grain'],
                                                [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Corn Stover Collected' in subst_name and in_or_out == D.tl_output:
                corn_stover_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Corn Stover Collected'],
                                                [UF.input_or_output, D.tl_output]]).magnitude
            
        
        if corn_stover_out != 0 and corn_grain_out != 0:
                #print('Altered allocation ratio')
                mass_allocation_ratio = (corn_stover_out / (corn_stover_out + corn_grain_out))
                #print(mass_allocation_ratio)
                
    capex_qty = capex_qty*mass_allocation_ratio
    land_cost_qty = land_cost_qty*mass_allocation_ratio
    capex = capex*mass_allocation_ratio
   
    opex = calcOPEX(tl_array)

    #Economic analysis variables
    ecovar = {'disc rate': 0.1, 't': 0.2, 'equity': 0.4, 'interest': 0.08, 'loan term': 10, 
              'maint rate': 0.03, 'ins rate': 0.01, 'land lease': 0, 'dep capex': 0.85}
    macrs = [0.143, 0.245, 0.175, 0.125, 0.089, 0.089, 0.089, 0.045]
    # Matches the B&D AltJet Spreadsheet
    
    ###yrs = input('What is the project lifespan? ')
    landcapex =  land_cost_qty.magnitude 
    
    #Total depreciable investment
    depinv =  capex_qty.magnitude * ecovar['dep capex']
    #Investment-loan share
    invloanshare = capex * (1-ecovar['equity'])
    #Loan annual payment
    loanannpay = capex*(1-ecovar['equity'])*ecovar['interest']*(1+ecovar['interest'])**ecovar['loan term']/((1+ecovar['interest'])**ecovar['loan term']-1)
    #Investment-equity share
    invequityshare = capex * (ecovar['equity'])
    #Salvage value end of life
    salvage = landcapex
    #Annual insurance
    annins = depinv * ecovar ['ins rate']
    #Annual maintenance
    annmaint = depinv * ecovar['maint rate']
    #Annual material and energy costs = opex, Annual labor costs = labor
    #Fixed operating costs in $/yr
    fopex =  annins + annmaint + opex + labor
    
    
    #creating MACRS list with zeros at the end to match duration of project
    depyrs = len (macrs)
    dif = int(yrs) - depyrs
    if dif > 0:
        addzero = [0] * dif
        macrs.extend (addzero)
    
    depreciation = []
    i = 0
    
    #calculating depreciation of depreciable investment in each year
    while i < len(macrs) :
        depreciation.append (depinv * macrs [i])
        i += 1
    
    i = 0
    
    #calculating loan payment, interest, and principle for each time step
    loanpay = [ ]
    loanint = [ ]
    loanprin = [ ]
    
    while i < int(ecovar['loan term']):
        loanpay.append (loanannpay)
        if i == 0:
            loanint.append (invloanshare*ecovar ['interest'])
            loanprin.append (invloanshare-loanpay[i]+loanint [i])
        else:
            loanint.append (loanprin [i-1]*ecovar ['interest'])
            loanprin.append (loanprin[i-1]-loanpay[i] + loanint[i])
        
        i += 1
    
    #adding zeros to the end of loan payment, interest, and principle for duration of project
    dif = int(yrs) - len(loanprin)
    
    if dif > 0:
        addzero = [0] * dif
        loanpay.extend (addzero)
        loanint.extend (addzero)
        loanprin.extend (addzero)
        
    result = s_opt.minimize_scalar(lambda MCSP: NPV_goal(MCSP, 
                                                                 fopex, 
                                                                 depreciation, 
                                                                 loanint, 
                                                                 ecovar, 
                                                                 invequityshare,
                                                                 loanpay,
                                                                 tl_array))

      
    return result.x         # $/kg

# Calculate cost of inputs (opex)
def calcOPEX(tl_array):
    inputs_cost = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost)
            if in_or_out == D.tl_input:
                inputs_cost += (LCA_val * mag)
   
    return inputs_cost
