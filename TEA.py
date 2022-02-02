import scipy.optimize as s_opt
import TEA_LCA_Data as D
import UnivFunc as UF
import math
import LifeCycleAssessment as LCA 

# This module conducts the economic analysis for a given biofuel production pathway 
# using the pathway module. This module calls the pathway module and has the user choose the pathway
# on which to conduct the economic analysis

yrs = 30 # userinputs.yrs

# function used for goal finding

def calc_NPV(tl_array, prod, coprods, path_string, fip, override_list):
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]          
    
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Cost']])
    capex =   capex_qty.magnitude + land_cost_qty.magnitude  #inputs ['capex']
    labor =  UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude
    
    opex = calcOPEX(tl_array, fip, override_list)
    
    economic_variable_list = UF.collectEconIndepVars(path_string)
    
    ecovar = {'op days': economic_variable_list[0],
              'disc rate': economic_variable_list[1],
              'fed tax': economic_variable_list[2],
              'state tax': economic_variable_list[3],
              'equity': economic_variable_list[4], 
              'interest': economic_variable_list[5], 
              'loan term': economic_variable_list[6],
              'maint rate': economic_variable_list[7], 
              'ins rate': economic_variable_list[8], 
              'land lease': 0, 
              'dep capex': economic_variable_list[9],
              'tax credit': economic_variable_list[10]}
    
    
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
    
    # print(depreciation)
    
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
                      loanpay, tl_array, prod, coprods, land_cost_qty, override_list, fip)        
    
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    
    # print(loanannpay)
    # print(loanint)
    # print(loanprin)
    # print(ecovar)
    
    
    # print(opex)
    # print(depinv)
    # print(invloanshare)
    # print(loanannpay)
    # print(invequityshare)
    # print(annins)
    # print(annmaint)
    # print(fopex)
    
    return result


def NPV_calc(fopex, depreciation, loanint, ecovar, invequityshare, loanpay,
             tl_array, prod, coprods, land_cost_qty, override_list, fip):
    
    # If no output fuel exists, I want to either call this loop or have it be run
    # automatically.
    
    ann_coproduct_revenue = 0   # Not really needed
    transport_fuel_energy = 0   # But now I don't have to change any logic
    pint_price_per_MJ = 0
    
    # print('In the correct loop')
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df,    # This looks like the output list of 
                                      match_list,               # transport fuels. I do not know if we want
                                      D.LCA_cost,0)             # to geospatially vary these cost values... ignore?
            
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(subst_name)
                print('Replacing with 0')
                LCA_val = 0
                
            if in_or_out == D.tl_output and (subst_name == 'Jet-A' or
                                             subst_name == 'Diesel, Produced' or
                                             subst_name == 'Gasoline, Produced' or 
                                             subst_name == 'LPG, Produced' or 
                                             subst_name == 'Propane, Produced' or 
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

    nonfuel_value = calcNonFuelValue(tl_array, 1, override_list, fip)
    #ann_fuel_revenue =  (pint_price_per_MJ * fuel_out)
    
    annrevenue = nonfuel_value
    
    
    # print(annrevenue)
    # print('----- Non-Fuel Value -----')
    # print(nonfuel_value)
    # print('--------------------------')
    
    #calculating net income
    netincome = []
    years = int(yrs)
    i = 0
    # print(annrevenue)
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
    
    # print(lossforward)
    #calculating income tax
    
    i = 0
    incometax = []
    while i < years:
        if taxincome [i] < 0:
            incometax.append (0)
        else:
            incometax.append ((taxincome [i] * (ecovar['fed tax'] + 
                                                ecovar['state tax'])) 
                                                - ecovar['tax credit'])
        i += 1
    # calculating cash flow
    cashflow = [-invequityshare]
    i = 1
    
    # print(taxincome)
    
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
             loanpay, tl_array, prod, coprods, land_cost_qty, cult_only, override_list, fip):
    
    if cult_only == 1:
        crop_price_per_MJ = price_per_MJ
        
        crop_price_per_MJ = D.returnPintQtyObj(price_per_MJ, 'yr/MJ')
        
        match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
        crop_out = UF.returnPintQty(tl_array, match_list)
        primary_crop_out_type = prod[0]
        crop_kg = crop_out
        
        other_crop_out_type = []
        other_HHVs = []
        other_crop_kg = []
        additional_revenue = 0
        
        
        for i in range(len(coprods)):
        
            if (coprods[i] == 'Corn Stover' or  
                                             coprods[i] == 'Gasoline, Produced' or 
                                             coprods[i] == 'LPG, Produced' or 
                                             # coprods[i] == 'Propane, Produced' or 
                                             coprods[i] == 'Ethanol' or 
                                             coprods[i] == 'Biodiesel, Produced'):
            
                other_crop_out_type.append(coprods[i])
                
            for i in range(len(other_crop_out_type)):
                other_HHVs.append(D.HHV_dict[other_crop_out_type[i]].qty)
                match_list = [[UF.substance_name, coprods[i]],[UF.input_or_output, D.tl_output]]
                other_crop_kg.append(UF.returnPintQty(tl_array, match_list))
            
            HHV = D.HHV_dict[primary_crop_out_type].qty
            
            primary_crop_energy = crop_kg * HHV
        
        
            ann_coproduct_revenue = 0   # Placeholder value for the eventual coproducts (might not be needed here anymore? 3/22)
              
            nonfuel_value = calcNonFuelValue_cult(tl_array, prod, override_list, fip)
            ann_fuel_revenue =  (crop_price_per_MJ * primary_crop_energy) 
            add_num = 0
            
            # print(ann_fuel_revenue)
            
            for i in range(len(other_crop_out_type)):
                other_crop_energy = other_crop_kg[i] * (other_HHVs[i]).magnitude
                # print(other_transport_fuel_energy)
                add_num = crop_price_per_MJ * other_crop_energy
                additional_revenue += add_num.magnitude
                
                
            # ann_fuel_revenue = pint_price_per_kg * transport_fuel_kg
            
            # ann_fuel_revenue += additional_revenue
        
            # print(add_num)
            # print(ann_fuel_revenue)
            
            # print(nonfuel_value)
            annrevenue = ann_fuel_revenue + nonfuel_value
            
        
    else:
        # print(price_per_MJ)
        pint_price_per_MJ = D.returnPintQtyObj(price_per_MJ, 'yr/MJ')
        #pint_price_per_kg = D.returnPintQtyObj(price_per_MJ, 'yr/kg')
        
        # I haven't been able to work out how to get the HHV dictionary to give us just the 
        # values, not the pint quantities.  Because of this, I have this gross 'yr/MJ' unit
        # on the pint_price_per_MJ value as the logic below demands a unitless value. I 
        # am happy to change it to include pint units downstream, but it is nice being able
        # to see the MFSP results as floats in the variable explorer (and not as a 'Quanti-
        # ty object of pint.quantity module') (6/7)
        match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
        fuel_out = UF.returnPintQty(tl_array, match_list)
        primary_fuel_out_type = prod[0]
        transport_fuel_kg = fuel_out
        
        other_fuel_out_type = []
        other_HHVs = []
        other_fuel_kg = []
        additional_revenue = 0
        #print(transport_fuel_kg)
        
        
        
        # Need to add logic to handle multiple different fuels with the HHV's
        # Going to throw some things off?  (7/22)
        
        for i in range(len(coprods)):
            if (coprods[i] == 'Diesel, Produced' or  
                                                 coprods[i] == 'Gasoline, Produced' or 
                                                 coprods[i] == 'LPG, Produced' or 
                                                 # coprods[i] == 'Propane, Produced' or 
                                                 coprods[i] == 'Ethanol' or 
                                                 coprods[i] == 'Biodiesel, Produced'):
                
                other_fuel_out_type.append(coprods[i])
                
        for i in range(len(other_fuel_out_type)):
            other_HHVs.append(D.HHV_dict[other_fuel_out_type[i]].qty)
            match_list = [[UF.substance_name, coprods[i]],[UF.input_or_output, D.tl_output]]
            other_fuel_kg.append(UF.returnPintQty(tl_array, match_list))
        
        HHV = D.HHV_dict[primary_fuel_out_type].qty
        
        primary_transport_fuel_energy = transport_fuel_kg * HHV
    
    
        ann_coproduct_revenue = 0   # Placeholder value for the eventual coproducts (might not be needed here anymore? 3/22)
          
        nonfuel_value = calcNonFuelValue(tl_array, 0, override_list, fip)
        ann_fuel_revenue =  (pint_price_per_MJ * primary_transport_fuel_energy) 
        add_num = 0
        
        # print(ann_fuel_revenue)
        
        for i in range(len(other_fuel_out_type)):
            other_transport_fuel_energy = other_fuel_kg[i] * (other_HHVs[i]).magnitude
            # print(other_transport_fuel_energy)
            add_num = pint_price_per_MJ * other_transport_fuel_energy
            additional_revenue += add_num.magnitude
            
            
        # ann_fuel_revenue = pint_price_per_kg * transport_fuel_kg
        
        ann_fuel_revenue += additional_revenue
    
        # print(add_num)
        # print(ann_fuel_revenue)
        
        annrevenue = ann_fuel_revenue + ann_coproduct_revenue + nonfuel_value
        
    # print('===== Annual Revenue ====')
    # print(annrevenue)
    # print('Annual Fuel Revenue Variable')
    # print(ann_fuel_revenue)
    # print('Annual Coproduct Revenue Variable')
    # print(ann_coproduct_revenue)
    # print('Nonfuel Value Variable')
    # print(nonfuel_value)
    
    
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
    # print(annrevenue)
    # print(loanpay)
    # print(netincome)
    
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
    
    # print(lossforward)
    # print(taxincome)
    #calculating income tax
    
    i = 0
    incometax = []
    while i < years:
        if taxincome [i] < 0:
            incometax.append (0)
        else:
            incometax.append (taxincome [i] * (ecovar['fed tax']
                                               + ecovar['state tax'])
                                               - ecovar['tax credit'])
        i += 1
    # calculating cash flow
    cashflow = [-invequityshare]
    i = 1
    
    # print(incometax)
    
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
    
    # print(disccashflow)
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
    # print(npv)
    return abs(npv[-1])

def calc_MBSP(biomass_IO, prod, coprods, path_string, fip, override_list):
    
    tl_array = biomass_IO
    
    # for i in range(len(biomass_IO)):

    for i in biomass_IO.index: 
        # print(i)
        row_vals = biomass_IO.loc[i]
        subst_name = row_vals[UF.substance_name]          
        
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    
    crop_out = UF.returnPintQty(tl_array, match_list)
    crop_out_type = prod[0]
    
    # print(crop_out_type)
    
    HHV = D.HHV_dict[crop_out_type].qty      
 
    #print(fuel_out_type)
 
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Cost']])

    match_list = [[D.LCA_key_str, 'Land Cost']]#, [D.LCA_IO, in_or_out]]
    land_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, override_list, fip)
    
    match_list = [[D.LCA_key_str, 'Capital Cost']]#, [D.LCA_IO, in_or_out]]
    capex_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, override_list, fip)
    
    match_list = [[D.LCA_key_str, 'Labor']]#, [D.LCA_IO, in_or_out]]
    labor_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, override_list, fip)
    
    capex =   ((capex_qty.magnitude * capex_scalar) + 
               (land_cost_qty.magnitude * land_scalar)) #inputs ['capex']
    
    labor =  (UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude) * labor_scalar
    
    #calculating total costs for inputs to the pathway (opex)
    
    opex = calcOPEX(tl_array, fip, override_list)
    #print(capex)
    # print('Operational Cost ------')
    # print(opex)
    # print('-----------------------')
    
    #Economic analysis variables
    
    economic_variable_list = UF.collectEconIndepVars(path_string)
    
    ecovar = {'op days': economic_variable_list[0],
              'disc rate': economic_variable_list[1],
              'fed tax': economic_variable_list[2],
              'state tax': economic_variable_list[3],
              'equity': economic_variable_list[4], 
              'interest': economic_variable_list[5], 
              'loan term': economic_variable_list[6],
              'maint rate': economic_variable_list[7], 
              'ins rate': economic_variable_list[8], 
              'land lease': 0, 
              'dep capex': economic_variable_list[9],
              'tax credit': economic_variable_list[10]}
    
    macrs = [0.143, 0.245, 0.175, 0.125, 0.089, 0.089, 0.089, 0.045]
    ###yrs = input('What is the project lifespan? ')
    landcapex =  land_cost_qty.magnitude 
    
    #Total depreciable investment
    depinv =  capex_qty.magnitude * ecovar['dep capex']
    # print(depinv)
    #Investment-loan share
    invloanshare = capex * (1-ecovar['equity'])
    # print(invloanshare)
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
        
    # print(loanpay)
    # print(loanint)
    # print(loanprin)
    
    
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
                                                                 coprods,
                                                                 land_cost_qty,
                                                                 1,
                                                                 override_list,
                                                                 fip))
    
    # print('Result Value ?')
    # print(result)
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    return result.x     # $/MJ (above optimization) * MJ/gge
    
    
    return

def quick_MFSP(tl_array, prod, coprods, path_string, fip, override_list):
    
    # Goal is to replicate the approximation that takes place in the TEA tab of the 
    # all pathways model 
    
    return_var = 0
    
    capex_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Capital Cost']])
    land_cost_qty = UF.returnPintQty(tl_array, [[UF.substance_name, 'Land Cost']])
    amortized_capex = (capex_qty + land_cost_qty) / 30
    
    labor =  (UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude) 
    opex = calcOPEX(tl_array, fip, override_list)
    
    dep_amt_rate = 0.9 # Note we will have to add functionality if we want to dynamically update this
    maint_rate = 0.03
    ins_rate = 0.01
    
    dep_inv     = capex_qty * dep_amt_rate 
    insurance   = dep_inv * ins_rate
    maintenance = dep_inv * maint_rate
    
    coprod_rev = calcNonFuelValue(tl_array, 0, override_list, fip) * 0.35 # average discount over 30 yrs
    fuel_prod_mj = LCA.calcFuelMJProduced(tl_array)
    fuel_prod_gge = fuel_prod_mj/132.61 # MJ per gas gallon equivalent
    
    total_costs = amortized_capex.magnitude + labor + opex + insurance.magnitude + maintenance.magnitude
    # Notice that you are not discounting the costs. Need to do that...
    rev_minus_costs = coprod_rev - total_costs
    
    mfsp_non_discounted = rev_minus_costs/-(fuel_prod_gge)
    
    return_var = mfsp_non_discounted / 0.35 # and again, as revenue must be discounted as well
    
    return return_var
    
def calc_MFSP(tl_array, prod, coprods, path_string, fip, override_list):
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
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
    # print(land_cost_qty)
    
    if type(override_list) == list:
            
        if 'Arable Land Value ($/ha)' in override_list:
            # print('Stepping in and grabbing given land cost')
            amount = UF.returnGeoLCANumber('Arable Land Value ($/ha)',fip, 'Electricity, Grid')
            # print('done')
            # print(amount)
            land_cost_qty = D.returnPintQtyObj(amount, 'dollars')
            
    # print(land_cost_qty)
    # Need to go through grab LCA value for potential scalars
    match_list = [[D.LCA_key_str, 'Land Cost']]#, [D.LCA_IO, in_or_out]]
    land_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, 0, 0)  
    # print(land_scalar)
    
    match_list = [[D.LCA_key_str, 'Capital Cost']]#, [D.LCA_IO, in_or_out]]
    capex_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, override_list, fip)
    
    match_list = [[D.LCA_key_str, 'Labor']]#, [D.LCA_IO, in_or_out]]
    labor_scalar = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, 0, 0) # Clobbering the OL here, always refences actual value?
    
    capex =   ((capex_qty.magnitude * capex_scalar) + 
               (land_cost_qty.magnitude * land_scalar)) #inputs ['capex']
    
    labor =  (UF.returnPintQty(tl_array, [[UF.substance_name, 'Labor']]).magnitude) * labor_scalar
    
    
    #calculating total costs for inputs to the pathway (opex)
    
    opex = calcOPEX(tl_array, fip, override_list)
    #print(capex)
    # print('Operational Cost ------')
    # print(opex)
    # print('-----------------------')
    #Economic analysis variables
    
    economic_variable_list = UF.collectEconIndepVars(path_string)
    
    # ecovar = {'disc rate': economic_variable_list[1],
    #           'fed tax': economic_variable_list[2],
    #           'equity': economic_variable_list[3], 
    #           'interest': economic_variable_list[4], 
    #           'loan term': economic_variable_list[5],
    #           'maint rate': economic_variable_list[6], 
    #           'ins rate': economic_variable_list[7], 
    #           'land lease': 0, 
    #           'dep capex': economic_variable_list[8]}
    
    ecovar = {'op days': economic_variable_list[0],
              'disc rate': economic_variable_list[1],
              'fed tax': economic_variable_list[2],
              'state tax': economic_variable_list[3],
              'equity': economic_variable_list[4], 
              'interest': economic_variable_list[5], 
              'loan term': economic_variable_list[6],
              'maint rate': economic_variable_list[7], 
              'ins rate': economic_variable_list[8], 
              'land lease': 0, 
              'dep capex': economic_variable_list[9],
              'tax credit': economic_variable_list[10]}
    
    macrs = [0.143, 0.245, 0.175, 0.125, 0.089, 0.089, 0.089, 0.045]
    ###yrs = input('What is the project lifespan? ')
    landcapex =  land_cost_qty.magnitude 
    
    #Total depreciable investment
    depinv =  capex_qty.magnitude * ecovar['dep capex']
    # print(depinv)
    #Investment-loan share
    invloanshare = capex * (1-ecovar['equity'])
    # print(invloanshare)
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
        
    # print(loanpay)
    # print(loanint)
    # print(loanprin)
    
    
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
                                                                 coprods,
                                                                 land_cost_qty,
                                                                 0,
                                                                 override_list,
                                                                 fip))
                                                                 
    
    # print('Result Value ?')
    # print(result)
    # print('---------')
    # print('CAPEX')
    # print(capex)  
    # print('-------')
    return result.x     # $/MJ (above optimization) * MJ/gge

# Calculate cost of inputs (opex)
def calcOPEX(tl_array, fip, override_list):
    inputs_cost = 0
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
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
                                      D.LCA_cost, override_list, fip)
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(subst_name)
                print('Replacing with 0')
                LCA_val = 0
            if in_or_out == D.tl_input:
                total = LCA_val * mag
                # print('------',subst_name,'-------')
                # print(LCA_val)
                # print(mag)
                # print(total)
                # print(inputs_cost)
                # print('---------------------')
                inputs_cost += (LCA_val * mag)
    #print(inputs_cost)
    return inputs_cost

# Calculate value of non-fuel outputs

def calcNonFuelValue_cult(tl_array, prod, override_list, fip):
    
    outputs_value = 0
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost, 0, 0)
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(subst_name)
                print('Replacing with 0')
                LCA_val = 0
            if in_or_out == D.tl_output and subst_name not in prod:
                total = LCA_val * mag
                outputs_value += (LCA_val * mag)  # In dollars 
                # print('--------')
                # print(subst_name)
                # print(LCA_val)
                # print(mag)
                # print(total)
                # print(outputs_value)
                # print('--------')

        
    return outputs_value

def calcNonFuelValue(tl_array, baseline_indicator,override_list, fip):
    outputs_value = 0
    
    # for i in range(len(tl_array)):
    for i in tl_array.index:
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_cost,0,0)
            if math.isnan(LCA_val) == True:
                print('Warning - NaN value associated with ')
                print(subst_name)
                print('Replacing with 0')
                LCA_val = 0
            if in_or_out == D.tl_output and baseline_indicator == 1:
                total = LCA_val * mag
                outputs_value += (LCA_val * mag)  # In dollars 
                # print('--------')
                # print(subst_name)
                # print(LCA_val)
                # print(mag)
                # print(total)
                # print(outputs_value)
                # print('--------')

            
            if in_or_out == D.tl_output and baseline_indicator != 1 and (
                                             subst_name != 'Jet-A' and
                                             subst_name != 'LPG, Produced' and
                                             # subst_name != 'Propane, Produced' and
                                             subst_name != 'Diesel, Produced' and
                                             subst_name != 'Gasoline, Produced' and 
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