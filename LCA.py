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
    if 'Jet-A' in tl_array:
        jet_a_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Jet-A'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    else:
        jet_a_out = 0
    
    if 'Diesel' in tl_array:
        diesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Diesel'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    else:
        diesel_out = 0
    
    if 'Gasoline' in tl_array:
        gasoline_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Gasoline'],
                                            [UF.input_or_output, D.tl_output]]).magnitude   # Need to edit this so that it includes all possible final fuel types
    else:
        gasoline_out = 0
    
    if 'Ethanol' in tl_array:
        ethanol_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Ethanol'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    else:
        ethanol_out = 0
        
    if 'Biodiesel' in tl_array:
        biodiesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Biodiesel'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    else:
        biodiesel_out = 0
        
    transport_fuel_energy = 46*(jet_a_out + diesel_out + gasoline_out + ethanol_out + biodiesel_out)
    # shouldn't use 46 for all of them. do separately with correct energy content (MJ/kg)
    
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

    return 75 + GHG_impact/total_MJ # the 75 number has to do with pre/post combustion accounting