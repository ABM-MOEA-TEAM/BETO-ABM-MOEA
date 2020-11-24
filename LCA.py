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
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_energy_impact)
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

# Calculate GHG Impact
def calcGHGImpact(tl_array):
    jet_a_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Jet-A'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    diesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Diesel'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    gasoline_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Gasoline'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
    transport_fuel_energy = 46.0*(jet_a_out+diesel_out+gasoline_out)
    
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

    return 75 + GHG_impact/total_MJ            