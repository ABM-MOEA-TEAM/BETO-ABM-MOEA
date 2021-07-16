import TEA_LCA_Data as D
import UnivFunc as UF

# Calculate EROI. Note that MJ/X is hard-coded units for LCI
def calcEROI(tl_array):
    energy_investment = 0
    energy_return = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        val_units = row_vals[UF.units]
        val_qty = D.returnPintQtyObj(mag, val_units)
        if in_or_out != D.zeroed:
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_energy_impact)
            LCA_units = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_units)
            LCA_qty = D.returnPintQtyObj(LCA_val, str('MJ / (' + LCA_units + ')'))           

            if LCA_units != val_units: # Performs check (verify 'X' and col. D match)
                print(subst_name)
                print(LCA_units)
                print(val_units)
                pqty = D.returnPintQtyObj(mag, val_units)
                mag = UF.returnConvertedMagnitude(pqty, LCA_units)
                
            if in_or_out == D.tl_input:
                energy_investment += (LCA_qty * val_qty).to('MJ')
                # This will throw an error if violated (MJ/X * X should = MJ)
            else:
                energy_return += (LCA_qty * val_qty).to('MJ')
    
    eroi = 0
    try:
        eroi += energy_return/energy_investment
    except:
        print('Divide by zero error')
    return eroi

# Calculate GHG Impact by energy allocation (reminder--need to add calculations 
# for allocation by mass, economic allocation, as well as system expansion displacement credits)

def calcGHGImpact(tl_array, prod, coprods): # Needs additional argument (calcGHGImpact(tl_array,products_list,co-products_list))
    
    # Note that the fact that this is transportation fuel could be a substance attribute
    
    output_frame = [] 

    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]          
        
        
    match_list = [[UF.substance_name, prod[0]],[UF.input_or_output, D.tl_output]] 
    # Can be done outside of for because the PW only has one "primary" product
    fuel_out = UF.returnPintQty(tl_array, match_list)
    fuel_out_type = prod[0]

    transport_fuel_kg = fuel_out
        
    HHV = D.HHV_dict[fuel_out_type].qty
    transport_fuel_energy = transport_fuel_kg * HHV
    
    coprods_vals = []
    coprods_HHV = []
    coprods_MJ = []
    

    for j in range(len(coprods)):
        match_list = [[UF.substance_name, coprods[j]],[UF.input_or_output, D.tl_output]]
        coprods_vals.append(UF.returnPintQty(tl_array,match_list))
        coprods_HHV.append(D.HHV_dict[coprods[j]])
        coprods_MJ.append(coprods_vals[j]*coprods_HHV[j].qty)
        
    GHG_impact_val = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out == D.tl_input:             
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_GHG_impact)
            GHG_impact_val += (LCA_val * mag)
        # print('-----------')
        # print(subst_name)
        # print(LCA_val)
        # print(mag)
        # print(GHG_impact_val)
        # print('-----------')
        
    GHG_impact = D.TEA_LCA_Qty(D.substance_dict['Greenhouse Gas Impact'], GHG_impact_val, 'g/yr')
    # print(GHG_impact.qty)
  
    for i in range(len(coprods)):
        if coprods[i] == 'Electricity':
            Elec = True
            
    ############## Energy Allocation Block ############## 
    coproduct_energy_content = 0
    
    for i in range(len(coprods)):
        coproduct_energy_content += coprods_MJ[i]
    #print(coprods_MJ)
    total_MJ = transport_fuel_energy + coproduct_energy_content
    
    # Define ratios to apply to each of the (co)products
    
    primary_ratio = transport_fuel_energy/total_MJ
    
    coprod_ratio_list = []
    
    for i in range(len(coprods)):
        coprod_ratio_list.append(coprods_MJ[i]/total_MJ)
    #print(coprod_ratio_list)
    
    primary_burden = (primary_ratio*GHG_impact.qty)/transport_fuel_energy
    coprod_burden_list = []
    
    for i in range(len(coprods)):
        coprod_burden_list.append((coprod_ratio_list[i]*GHG_impact.qty)/transport_fuel_energy)
    
    output_frame.append(primary_burden)
    for i in range(len(coprods)):
        output_frame.append(coprod_burden_list[i])

    # Update on Intent (4/20) - Energy Allocation and System Expansion only
    
    ############## System Boundary Expansion Block ##############
    
    out_GHG_impact_val = 0
    
    for i in range(len(tl_array)):
        row_vals = tl_array.loc[i]
        subst_name = row_vals[UF.substance_name]
        in_or_out = row_vals[UF.input_or_output]
        mag = row_vals[UF.magnitude]
        if in_or_out == D.tl_output:             
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_GHG_impact)
            out_GHG_impact_val += (LCA_val * mag)
    # LCA inventory values are negative for "displaceable" coproducts (i.e. soymeal)
    # Thus, we will add the "out_GHG" value to the GHG_impact from the input substances.
    # (adds positive GWP burden for non-useful outputs, and negative LCA values takes 
    # away GWP burden for useful outputs)
    
    out_GHG_impact = D.TEA_LCA_Qty(D.substance_dict['Greenhouse Gas Impact'], out_GHG_impact_val, 'g/yr')
    
    Disp_GHG_impact = GHG_impact.qty + out_GHG_impact.qty
    
    Disp_Burden = Disp_GHG_impact/transport_fuel_energy
    
    output_frame.append(Disp_Burden)
    
    return output_frame