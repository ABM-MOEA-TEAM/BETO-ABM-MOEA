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

            if LCA_units != val_units:
                print(subst_name)
                print(LCA_units)
                print(val_units)
                pqty = D.returnPintQtyObj(mag, val_units)
                mag = UF.returnConvertedMagnitude(pqty, LCA_units)
                
            if in_or_out == D.tl_input:
                energy_investment += (LCA_qty * val_qty).to('MJ')
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
        if in_or_out == D.tl_input:             #(4/7) changed to "tl_input" as we are not handling the 
            #print(subst_name)                  # output substance impacts until we try to tackle displ
            match_list = [[D.LCA_key_str, subst_name],
                          [D.LCA_IO, in_or_out]]
            LCA_val = UF.returnLCANumber(D.LCA_inventory_df, 
                                      match_list, 
                                      D.LCA_GHG_impact)
            #print(LCA_val)
            GHG_impact_val += (LCA_val * mag)
    
    GHG_impact = D.TEA_LCA_Qty(D.substance_dict['Greenhouse Gas Impact'], GHG_impact_val, 'g/yr')
    print(GHG_impact.qty)
# If electricity is present, only economic and energy allocation make sense
    
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
    #print(primary_burden)
    #print(coprod_burden_list[0])
    #print(coprods)
    #print(coprod_burden_list)
    #print(output_frame)
    return output_frame

    
    # Intent as of (4/7) is to simply return all LCA results 
    # for all methods (ie from energy, mass, $ allocation and later displac.)
    
    # Need to add names for entries in output frame
    
        # Replace these statements with products list and coproducts list
        # Substance name is critical - MJ's 
        # Collapse down to single if;
        # If subst_name in products_list and in_or_out == output:
            # create a dictionary (declare) {} - 
            # dictionary_subst_name = pintQty (should populate with amounts of indicated prod quantities)
        # same loop and structure for coproducts 
        # that gives us length of coproducts list 
        
        # Create a dictionary in TEA_LCA_Data with the substance name and energy content
        
    # jet_a_out = 0
    # diesel_out = 0
    # gasoline_out = 0
    # ethanol_out = 0
    # biodiesel_out = 0
    # electricity_out_MJ = 0
    # soymeal_out = 0


    # for i in range(len(tl_array)):
    #     row_vals = tl_array.loc[i]
    #     in_or_out = row_vals[UF.input_or_output]
    #     subst_name = row_vals[UF.substance_name]
        

    #     if 'Jet-A' in subst_name and in_or_out == D.tl_output:
    #         jet_a_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Jet-A'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude

    #     if 'Diesel' in subst_name and in_or_out == D.tl_output:
    #         diesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Diesel'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude
        
    #     if 'Gasoline' in subst_name and in_or_out == D.tl_output:
            
    #         gasoline_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Gasoline'],
    #                                                   [UF.input_or_output, D.tl_output]]).magnitude
            
    #     if 'Ethanol' in subst_name and in_or_out == D.tl_output:
    #         ethanol_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Ethanol'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude
                
    #     if 'Biodiesel' in subst_name and in_or_out == D.tl_output:
    #         biodiesel_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Biodiesel'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude
    # # transport fuel energy is the primary product, the list below identifies following coproducts    

    #     if 'Electricity' in subst_name and in_or_out == D.tl_output:
    #         electricity_out_MJ = UF.returnPintQty(tl_array, [[UF.substance_name, 'Electricity'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude

    # # Feed Coproducts list
    #     if 'Soymeal' in subst_name and in_or_out == D.tl_output:
    #         soymeal_out = UF.returnPintQty(tl_array, [[UF.substance_name, 'Soymeal'],
    #                                         [UF.input_or_output, D.tl_output]]).magnitude
    
        
    # transport_fuel_kg = jet_a_out + diesel_out + gasoline_out + ethanol_out + biodiesel_out # all kg

    # transport_fuel_energy = ((43.2*jet_a_out) + (42.975*diesel_out) + 
    #     (43.44*gasoline_out) + (26.95*ethanol_out) + (37.75*biodiesel_out)) 
    
    # loop to get products energy (above) from pint qts (amnts) with HHV's .csv.
    # make the heating values pint quantities (kg/day?) TEA_LCA_Data function in declaration (MJ/kg)
    
    # Going to move these values from being hardcoded to being a substance attribute
    # Also decided to switch from LHV to HHV (4/7)
    
    # Transport fuel = primary product, Electricity out = 1st coproduct, Feed out = 2nd coproduct
    
    # This function must take the mass of all outputs (coproducts) such that we can both track how many
    # coproducts are present and the amount of each coproduct (so that we can scale based on energy,mass, $..)
    
    # total_MJ = transport_fuel_energy + electricity_out_MJ
    
    # feed_out_kg = soymeal_out #+ all the other things I need to add still (DDGS..) (4/7)
    
    # feed_out_MJ = soymeal_out # * energy of soymeal + DDGS * energy of DDGS, etc.
    
    # Evaluate the Total GHG burden of the pathway

    # GHG_impact is the total burden that the pathway possesses 

    #################### Energy Allocation Logic ####################
    
    # primary_prod_MJ = transport_fuel_energy # Should always be nonzero as a fuel is always produced
    
    # coprod1_MJ = 0
    # coprod2_MJ = 0
    
    # if electricity_out_MJ == 0 and feed_out_MJ == 0:
    # # Should not occur for any of the pathways as all produce elec or feed
    
    #     print("No coproduct! Check pathway?")
    #     return output_frame
    
    # if electricity_out_MJ != 0 and feed_out_kg != 0:
    #     coprod1_MJ = electricity_out_MJ
    #     coprod2_MJ = feed_out_MJ
    
    # # This assumes that at most only fuel, elec, and one feed are produced
    # # probably ok for the first attempt but not going to be sufficient for 
    # # pathways with numerous coproducts (i.e. algae) 
    
    # if electricity_out_MJ == 0 and feed_out_kg != 0:
    #     coprod1_MJ = feed_out_MJ
    
    # # If no electricity is made and feed is present, feed is only (1st) coproduct
    
    # if electricity_out_MJ != 0 and feed_out_kg == 0:
    #     coprod1_MJ = electricity_out_MJ
    
    # # Nothing should get through these if's but it would probably be best to clean 
    # # them up somehow. Maybe set coprod1_MJ to elec and coprod2_MJ to feed and then
    # # check for the special case of is elec == 0? Ways to improve code...(4/7)
    
    # total_MJ = primary_prod_MJ + coprod1_MJ + coprod2_MJ
    
    # primary_ratio = primary_prod_MJ/total_MJ
    # coprod1_ratio = coprod1_MJ/total_MJ
    # coprod2_ratio = coprod2_MJ/total_MJ    
    
    # normalized_burden = GHG_impact/total_MJ
    # primary_burden = (GHG_impact*primary_ratio)/primary_prod_MJ
    # coprod1_burden = (GHG_impact*coprod1_ratio)/primary_prod_MJ
    # coprod2_burden = (GHG_impact*coprod2_ratio)/primary_prod_MJ
    
    # # I am normalizing with respect to the transport fuel energy rather than each
    # # coproduct as the we feel it describes more clearly the relative burdens of 
    # # the different products. If /"coprod1", all should be the same:
    # # GHG_impact/total_MJ's gives the value that all work out to. 
    
    # output_frame.append(normalized_burden)
    # output_frame.append(primary_burden)
    # output_frame.append(coprod1_burden)
    # output_frame.append(coprod2_burden)
    # print(coprod2_burden)
    # #################### Mass Allocation Logic ####################
    
    # return output_frame