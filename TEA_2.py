# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:15:21 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import scipy.optimize as s_opt

def calcOPEX(tl_array):
    inputs_cost = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed and (subst_name != 'Land Cost' and
                                      subst_name != 'Capital Cost' and
                                      subst_name != 'Labor'):
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost)
            if in_or_out == D.tl_input:
                total = LCA_val*mag
                # print('------',subst_name,'-------')
                # print(LCA_val)
                # print(mag)
                # print(total)
                # print('---------------------')
                inputs_cost += (LCA_val * mag)
    #print(inputs_cost)
    return inputs_cost

def calcNonFuelValue(tl_array):
    outputs_value = 0
    
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
            if in_or_out == D.tl_output and (subst_name != 'Jet-A' and
                                             subst_name != 'Diesel' and
                                             subst_name != 'Gasoline' and 
                                             subst_name != 'Ethanol' and 
                                             subst_name != 'Biodiesel, Produced'):
                total = LCA_val * mag
                outputs_value += (LCA_val * mag)  # In dollars 
                # print('--------')
                # print(subst_name)
                # print(LCA_val)
                # print(mag)
                # print(total)
                # print('--------')
                
    # print(outputs_value)
    return outputs_value

def par_tea(tl_array, prod, coprods, path_string):
    print('its a party its a party its a party')
    output = 0
    yrs = 30
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]          
        
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    # Can be done outside of for because the PW only has one "primary" product
    fuel_out = UF.returnPintQty(tl_array, match_list)
    fuel_out_type = prod[0]
    
    HHV = D.HHV_dict[fuel_out_type].qty      
    
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Cost']])
    capex =   capex_qty.magnitude + land_cost_qty.magnitude  #inputs ['capex']
    labor =  UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude
    
    opex = calcOPEX(tl_array)
    
    economic_variable_list = UF.collectEconIndepVars(path_string)
    
    ecovar = {'disc rate': economic_variable_list[1],
              't': economic_variable_list[2],
              'equity': economic_variable_list[3], 
              'interest': economic_variable_list[4], 
              'loan term': economic_variable_list[5],
              'maint rate': economic_variable_list[6], 
              'ins rate': economic_variable_list[7], 
              'land lease': 0, 
              'dep capex': economic_variable_list[8]}
    
    macrs = [0.143, 0.245, 0.175, 0.125, 0.089, 0.089, 0.089, 0.045]
    
    landcapex =  land_cost_qty.magnitude 
    
    #Total depreciable investment
    depinv =  capex_qty.magnitude * ecovar['dep capex']

    #Investment-loan share
    invloanshare = capex * (1-ecovar['equity'])

    #Loan annual payment
    loanannpay = capex*(1-ecovar['equity'])*ecovar['interest']*(1+ecovar['interest'])**ecovar['loan term']/((1+ecovar['interest'])**ecovar['loan term']-1)
    # print('---------')
    # print('Loan Annual Payment')
    # print(loanannpay)
    # print('---------')
    #Investment-equity share
    invequityshare = capex * (ecovar['equity'])
    # print(invequityshare)
    
    #Salvage value end of life
    salvage = landcapex
    #Annual insurance
    annins = depinv * ecovar ['ins rate']
    # print(annins)
    #Annual maintenance
    annmaint = depinv * ecovar['maint rate']
    # print(annmaint)
    #Annual material and energy costs = opex, Annual labor costs = labor
    #Fixed operating costs in $/yr
    fopex =  annins + annmaint + opex + labor
    # print(fopex)
    
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
    
    # print(depreciation)
    # print(depinv)
    # print(invloanshare)
    # print(loanannpay)
    # print(invequityshare)
    # print(annins)
    # print(annmaint)
    # print(fopex)
    # print(fuel_out)
    # print(fuel_out_type)
    
    loanpay = [ ]
    loanint = [ ]
    loanprin = [ ]
    
    while i < int(ecovar['loan term']):
        loanpay.append (loanannpay)
        if i == 0:
            loanint.append (invloanshare*ecovar ['interest'])
            loanprin.append (invloanshare-loanpay[i]+loanint [i])
            # print(loanint)
            #print(loanprin)
        else:
            loanint.append (loanprin [i-1]*ecovar ['interest'])
            loanprin.append (loanprin[i-1]-loanpay[i] + loanint[i])
            #print(loanprin[i])
            # print(loanint)
        i += 1
    
    #adding zeros to the end of loan payment, interest, and principle for duration of project
    dif = int(yrs) - len(loanprin)
    
    if dif > 0:
        addzero = [0] * dif
        loanpay.extend (addzero)
        loanint.extend (addzero)
        loanprin.extend (addzero)

    result = NPV_calc(fopex, depreciation, loanint, ecovar, invequityshare, 
                      loanpay, tl_array, prod, land_cost_qty)        
    
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    
    return result

def NPV_calc(fopex, depreciation, loanint, ecovar, invequityshare, loanpay,
             tl_array, prod, land_cost_qty):

    yrs = 30
    ann_coproduct_revenue = 0   # Not really needed
    transport_fuel_energy = 0   # But now I don't have to change any logic
    pint_price_per_MJ = 0

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
            if in_or_out == D.tl_output and (subst_name == 'Jet-A' or
                                             subst_name == 'Diesel' or
                                             subst_name == 'Gasoline' or 
                                             subst_name == 'Ethanol' or 
                                             subst_name == 'Biodiesel, Produced'):
                pint_price_per_MJ = LCA_val 
                # print('--------')
                # print(subst_name)
                # print(LCA_val)
                # print(mag)
                # print('--------')
    
    pint_price_per_MJ = D.returnPintQtyObj(pint_price_per_MJ, 'yr/kg')     
    # print('Price Per MJ')
    # print(pint_price_per_MJ.magnitude)       
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    fuel_out = UF.returnPintQty(tl_array, match_list)
    # fuel_out_type = prod[0]
    # transport_fuel_kg = fuel_out
    
    # HHV = D.HHV_dict[fuel_out_type].qty
    # transport_fuel_energy = transport_fuel_kg * HHV
    
    nonfuel_value = calcNonFuelValue(tl_array)
    ann_fuel_revenue =  (pint_price_per_MJ * fuel_out)
    
    ann_coproduct_revenue = nonfuel_value
    annrevenue = ann_fuel_revenue + ann_coproduct_revenue
    
    
    #print(annrevenue)
    # print('----- Non-Fuel Value -----')
    # print(nonfuel_value)
    # print('--------------------------')
    
    #calculating net income
    netincome = []
    years = int(yrs)
    i = 0
    
    while i < years:
        if i == years-1: # In the last year you get the salvage value back? (7/16)
            netincome.append (annrevenue - fopex -depreciation [i] -loanint [i]
                              + land_cost_qty.magnitude)
        else:
            netincome.append (annrevenue - fopex -depreciation [i] -loanint [i])
        i += 1
        
            
    
    # print(netincome)
    # print('Coproduct Rev. ------')
    # print(ann_coproduct_revenue)
    # print('---------------------')
    # print('Fuel Revenue --------')
    # print(ann_fuel_revenue)
    # print('---------------------')
    # print('Annual Revenue ------')
    # print(annrevenue)
    # print('---------------------')
    

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
    
    #print(lossforward)
    
    #calculating income tax
    
    i = 0
    incometax = []
    while i < years:
        if taxincome [i] < 0:
            incometax.append (0)
        else:
            incometax.append (taxincome [i] * ecovar['t'])
        i += 1
    
    #print(incometax)
    
    # calculating cash flow
    cashflow = [-invequityshare]
    i = 1
    
    while i < years + 1:
        cashflow.append (annrevenue - fopex - loanpay [i-1] - incometax [i-1])
        i += 1 
    
    # print(cashflow)
    
    # calculating discounted cash flow
    disccashflow = []
    i = 0
    
    while i < years + 1:
        disccashflow.append (cashflow [i]/(1+ecovar['disc rate'])**i)
        i += 1
    
    #print(disccashflow)
    
    # calculating cumulative discounted cash flow
    cumdisccashflow = [disccashflow [0]]
    
    i = 1
    
    while i < years + 1:
        cumdisccashflow.append (cumdisccashflow [i - 1] + disccashflow [i])
        i += 1
    
    # NPV retrieval from cumulative discounted cash flow
    npv = cumdisccashflow
    
    # print(abs(npv[-1]))
    return npv[-1]
    

