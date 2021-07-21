import scipy.optimize as s_opt
import TEA_LCA_Data as D
import UnivFunc as UF

# This module conducts the economic analysis for a given biofuel production pathway 
# using the pathway module. This module calls the pathway module and has the user choose the pathway
# on which to conduct the economic analysis

yrs = 30 # userinputs.yrs

# function used for goal finding

def calc_NPV(tl_array, prod, coprods, path_string):
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]          
    
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
    #print(ecovar)
    macrs = [0.143, 0.245, 0.175, 0.125, 0.089, 0.089, 0.089, 0.045]
    ###yrs = input('What is the project lifespan? ')
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
    #Salvage value end of life
    salvage = landcapex
    #Annual insurance
    annins = depinv * ecovar ['ins rate']
    #Annual maintenance
    annmaint = depinv * ecovar['maint rate']
    #Annual material and energy costs = opex, Annual labor costs = labor
    #Fixed operating costs in $/yr
    fopex =  annins + annmaint + opex + labor
    # print(opex)
    # print(fopex)
    # print('annual insurance:')
    # print(annins)
    # print('annual maintenance')
    # print(annmaint)
    # print('annual labor')
    # print(labor)
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

    result = NPV_calc(fopex, depreciation, loanint, ecovar, invequityshare, 
                      loanpay, tl_array, prod, land_cost_qty)        
    
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    
    return result


def NPV_calc(fopex, depreciation, loanint, ecovar, invequityshare, loanpay,
             tl_array, prod, land_cost_qty):
    
    # If no output fuel exists, I want to either call this loop or have it be run
    # automatically.
    
    ann_coproduct_revenue = 0   # Not really needed
    transport_fuel_energy = 0   # But now I don't have to change any logic
    pint_price_per_MJ = 0
    
    # print('In the correct loop')
    
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

    return npv[-1]
    

def NPV_goal(price_per_MJ, fopex, depreciation, loanint, ecovar, invequityshare,
             loanpay, tl_array, prod, land_cost_qty):
    
    pint_price_per_MJ = D.returnPintQtyObj(price_per_MJ, 'yr/MJ')
    #pint_price_per_kg = D.returnPintQtyObj(price_per_MJ, 'yr/kg')
    
    # I haven't been able to work out how to get the HHV dictionary to give us just the 
    # values, not the pint quantities.  Because of this, I have this gross 'yr/MJ' unit
    # on the pint_price_per_MJ value as the logic below demands a unitless value. I 
    # am happy to change it to include pint units downstream, but it is nice being able
    # to see the MFSP results as floats in the variable explorer (and not as a 'Quanti-
    # ty object of pint.quantity module') (6/7)
    
    #Primary Fuel Products
    # jet_a_out = 0
    # diesel_out = 0
    # gasoline_out = 0
    # ethanol_out = 0
    # biodiesel_out = 0

    # for i in range(len(tl_array)):
    #     row_vals = tl_array.loc[i]
    #     subst_name = row_vals[UF.substance_name]          
    #     in_or_out = row_vals[UF.input_or_output]
        
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    fuel_out = UF.returnPintQty(tl_array, match_list)
    fuel_out_type = prod[0]
    transport_fuel_kg = fuel_out
    
    #print(transport_fuel_kg)
    
    HHV = D.HHV_dict[fuel_out_type].qty
    
    transport_fuel_energy = transport_fuel_kg * HHV

    ann_coproduct_revenue = 0   # Placeholder value for the eventual coproducts (might not be needed here anymore? 3/22)
      
    nonfuel_value = calcNonFuelValue(tl_array)
    ann_fuel_revenue =  pint_price_per_MJ * transport_fuel_energy
    
    #ann_fuel_revenue = pint_price_per_kg * transport_fuel_kg
    
    annrevenue = ann_fuel_revenue + ann_coproduct_revenue + nonfuel_value
    
    # print('Price Per MJ')
    # print(price_per_MJ)
    # print('--------------')
    # calculating total annual revenue from annual fuel revenue and co product revenue
    # for key in prodcost:
    #     if key in prodcost and key in outputs:
    #         annrevenue += prodcost [key] * outputs[key]
    
    
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
    #print(annrevenue)
    #print(loanpay)
    #print(netincome)
    
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
    # print(netincome)    
    #print(abs(npv[-1]))
    #print(price_per_MJ)
    print(npv)
    return abs(npv[-1])

def calc_MFSP(tl_array, prod, coprods, path_string):
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]          
        
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    # Can be done outside of for because the PW only has one "primary" product
    fuel_out = UF.returnPintQty(tl_array, match_list)
    fuel_out_type = prod[0]
    
    HHV = D.HHV_dict[fuel_out_type].qty      
 
    # coprods_vals = []
    # coprods_HHV = []
    # coprods_MJ = []
    

    # for j in range(len(coprods)):
    #     match_list = [[UF.substance_name, coprods[j]],[UF.input_or_output, D.tl_output]]
    #     coprods_vals.append(UF.returnPintQty(tl_array,match_list))
    #     coprods_HHV.append(D.HHV_dict[coprods[j]])
    #     coprods_MJ.append(coprods_vals[j]*coprods_HHV[j].qty)
        
    #print(fuel_out_type)
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Cost']])
    capex =   capex_qty.magnitude + land_cost_qty.magnitude  #inputs ['capex']
    labor =  UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude
    
    
    #calculating total costs for inputs to the pathway (opex)
    
    opex = calcOPEX(tl_array)
    #print(capex)
    # print('Operational Cost ------')
    # print(opex)
    # print('-----------------------')
    #Economic analysis variables
    
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
    ###yrs = input('What is the project lifespan? ')
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
        
    result = s_opt.minimize_scalar(lambda price_per_MJ: NPV_goal(price_per_MJ, 
                                                                 fopex, 
                                                                 depreciation, 
                                                                 loanint, 
                                                                 ecovar, 
                                                                 invequityshare,
                                                                 loanpay,
                                                                 tl_array,
                                                                 prod,
                                                                 land_cost_qty))
    
    # print('Result Value ?')
    # print(result)
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    return result.x     # $/MJ (above optimization) * MJ/gge

# Calculate cost of inputs (opex)
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

# Calculate value of non-fuel outputs
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