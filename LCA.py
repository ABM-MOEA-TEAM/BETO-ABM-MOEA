import TEA_LCA_Data as D
import UnivFunc as UF

# Calculate EROI
def calcEROI(tl_array):
    energy_investment = 0
    energy_return = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        val_units = row_vals[UF.units]
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_energy_impact)
            LCA_units = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_units)
            if LCA_units != val_units:
                print(subst_name)
                print(LCA_units)
                print(val_units)
                pqty = D.returnPintQtyObj(mag, val_units)
                mag = UF.returnConvertedMagnitude(pqty, LCA_units)
                
            
            if in_or_out == D.tl_input:
                energy_investment += (LCA_val * mag)
            else:
                energy_return += (LCA_val * mag)
    
    eroi = 0
    try:
        eroi += energy_return/energy_investment
    except:
        print('Divide by zero error')
    return eroi

# Calculate GHG Impact by energy allocation (reminder--need to add calculations 
# for allocation by mass, economic allocation, as well as system expansion displacement credits)
def calcGHGImpact(tl_array):
    
    # Note that the fact that this is transportation fuel could be a substance attribute
    
    jet_a_out = 0
    diesel_out = 0
    gasoline_out = 0
    ethanol_out = 0
    biodiesel_out = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        in_or_out = row_vals[UF.input_or_output]
        subst_name = row_vals[UF.substance_name]
        
        if 'Jet-A' in subst_name and in_or_out == D.tl_output:
            jet_a_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Jet-A'],
                                            [UF.input_or_output, D.tl_output]]).magnitude

        if 'Diesel' in subst_name and in_or_out == D.tl_output:
            diesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Diesel'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Gasoline' in subst_name and in_or_out == D.tl_output:
            
            gasoline_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Gasoline'],
                                                      [UF.input_or_output, D.tl_output]]).magnitude
            
        if 'Ethanol' in subst_name and in_or_out == D.tl_output:
            ethanol_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Ethanol'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
                
        if 'Biodiesel' in subst_name and in_or_out == D.tl_output:
            biodiesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Biodiesel'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        

    transport_fuel_energy = (43.2*jet_a_out) + (42.975*diesel_out) + (43.44*gasoline_out) + (26.95*ethanol_out) + (37.75*biodiesel_out)
    # See the TEA file for comments on this update and for the sources of the LHV's     
    
    # note that excel formula has a few others. zero for grass so omitting.
    total_MJ = transport_fuel_energy + UF.returnPintQty(tl_array, [[UF.substance_name, 'Electricity'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
    GHG_impact = 0
    
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
                                      D.LCA_GHG_impact)
            GHG_impact += (LCA_val * mag)
    
    # print('Jet A      -', jet_a_out)        # Helpful output for debugging
    # print('Diesel     -', diesel_out)
    # print('Gasoline   -', gasoline_out)
    # print('Ethanol    -', ethanol_out)
    # print('Biodiesel  -', biodiesel_out)
    
    return GHG_impact/total_MJ # the 75 number has to do with pre/post combustion accounting

    # I removed the 75 - going to neglect the input credit of carbon pulled from atmosphere and then not track 
    # the carbon released upon combustion, as this is consistent with the methodology for the other PM's