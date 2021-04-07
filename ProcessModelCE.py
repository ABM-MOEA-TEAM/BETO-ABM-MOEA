# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 01:32:19 2020

@author: Jack Smith
"""

# Data and Universal Functions
import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import Ag_TEA
import LCA
import Ag_LCA

# Process steps
import Corn_Stover_Cultivation as CSC
import Corn_Stover_Ethanol as CSE
import Stover_Ethanol_Upgrade as SEU

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')

yield_value = 5563.08 # will be replaced by the DayCent values

stover_collected = 0.5 # Not currently being used (4/5)

# Biomass Production
biomass_IO = CSC.grow_stover(land_area_val, yield_value)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = CSE.ethanol_stover(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = SEU.upgrade_stover_ethanol(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)

downstream_IO = UF.createEmptyFrame()   # Downstream here corresponds to 
                                        # the conversion and upgrading blocks
                                        # (perhaps another name is better?)

downstream_IO = downstream_IO.append(conversion_IO, ignore_index=True)
downstream_IO = downstream_IO.append(upgrading_IO, ignore_index=True)

# And we now have a compliment to the Biomass IO array

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
IO_ds_array = UF.consolidateIO(downstream_IO)
# If we end up doing a mass allocation in the TEA steps, it might make sense
# to replace the "IO_array" as I don't know if we're using it any longer

# After executing the three process model blocks, we now determine the total
# MJ's of output fuel produced by the pathway. We may then pass that energy out
# value to the Ag_LCA block as an additional argument to allow us to find 
# gCO2eq/MJ at the farm gate (and facilitate allocation)

jet_a_out = 0
diesel_out = 0
gasoline_out = 0
ethanol_out = 0
biodiesel_out = 0
electricity_out = 0

# Need to instantiate each of the fuels as zero, as any given PW will not 
# produce all types of fuel

for i in range(len(IO_array)):
        row_vals = IO_array.loc[i]
        in_or_out = row_vals[UF.input_or_output]
        subst_name = row_vals[UF.substance_name]
        
        if 'Jet-A' in subst_name and in_or_out == D.tl_output:                              # 43.2 MJ/kg from https://ecn.sandia.gov/diesel-spray-combustion/sandia-cv/fuels/
            jet_a_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Jet-A'],
                                            [UF.input_or_output, D.tl_output]]).magnitude

        if 'Diesel' in subst_name and in_or_out == D.tl_output:
            diesel_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Diesel'],         # 42.975 MJ/kg from ""
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Gasoline' in subst_name and in_or_out == D.tl_output:
            gasoline_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Gasoline'],
                                            [UF.input_or_output, D.tl_output]]).magnitude     # 43.44 MJ/kg from https://h2tools.org/hyarc/calculator-tools/lower-and-higher-heating-values-fuels
            
        if 'Ethanol' in subst_name and in_or_out == D.tl_output:
            ethanol_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Ethanol'],
                                            [UF.input_or_output, D.tl_output]]).magnitude   # 26.95 MJ/kg from ""
                
        if 'Biodiesel' in subst_name and in_or_out == D.tl_output:
            biodiesel_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Biodiesel'],   # 37.75 MJ/kg from Tesfa - "LHV Predication Models and LHV Effect on the 
                                            [UF.input_or_output, D.tl_output]]).magnitude   # Performance of CI Engine Running with Biodiesel Blends" (Implies Compression Ignition Engine)
            
        if 'Electricity' in subst_name and in_or_out == D.tl_output:                              # 43.2 MJ/kg from https://ecn.sandia.gov/diesel-spray-combustion/sandia-cv/fuels/
            elec_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Electricity'],
                                            [UF.input_or_output, D.tl_output]]).magnitude
        
        if 'Electricity' in subst_name and in_or_out == D.tl_input:                              # 43.2 MJ/kg from https://ecn.sandia.gov/diesel-spray-combustion/sandia-cv/fuels/
            elec_in = UF.returnPintQty(IO_array, [[UF.substance_name, 'Electricity'],
                                            [UF.input_or_output, D.tl_input]]).magnitude

transport_fuel_energy = ((43.2*jet_a_out) + (42.975*diesel_out) + 
        (43.44*gasoline_out) + (26.95*ethanol_out) + (37.75*biodiesel_out))
# This is just the logic from the TEA block

LCA_val_elec = UF.returnLCANumber(D.LCA_inventory_df,
                                  [[D.LCA_key_str, 'Electricity'],
                                   [D.LCA_IO, D.tl_output]],
                                  D.LCA_GHG_impact)

elec_credit = (LCA_val_elec*elec_out)/transport_fuel_energy
#Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Calculate GHG Impact at Farm Gate
ghg_farm = Ag_LCA.calcGHGImpactAg(biomass_IO,transport_fuel_energy)

# Calculate total GHG Impact
# The Process Model is already keeping track of the emissions from the farm.
# Allocation can be applied to that portion of the GWP burden

ghg_downstream = LCA.calcGHGImpact(IO_ds_array)
# Compiles the Greenhouse Gas Impact of the conv/upgr blocks

#ghg_impact = ghg_farm + ghg_downstream
ghg_impact = ghg_farm + ghg_downstream - elec_credit

# Calculate MFSP
mfsp = TEA.calc_MFSP(IO_array)

# Calculate Minimum Crop Selling Price at farm gate
mcsp = Ag_TEA.calc_MCSP(biomass_IO)

# CheckSum for spreadsheet/Python agreement
bp_in = UF.sumProcessIO(results_array, D.biomass_production, D.tl_input)

conv_in = UF.sumProcessIO(results_array, D.conv, D.tl_input)

upgr_in = UF.sumProcessIO(results_array, D.upgrading, D.tl_input)

bp_out = UF.sumProcessIO(results_array, D.biomass_production, D.tl_output)

conv_out = UF.sumProcessIO(results_array, D.conv, D.tl_output)

upgr_out = UF.sumProcessIO(results_array, D.upgrading, D.tl_output)


# eroi_chksm = 2.51
mfsp_chksm = 2.43

print('Executed Corn Stover Fermentation to Ethanol PM')
