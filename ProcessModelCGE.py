# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 04:45:25 2021

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
import Corn_Grain_Cultivation as CGC
import Corn_Grain_Ethanol as CGE
import Grain_Ethanol_Upgrade as GEU

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')

biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 10974, 'kg/ha/yr')

# Ag_only = bool(False)
AllocationID = 1  # This is a solid idea

#stover_collected = 0.5

# Biomass Production
biomass_IO = CGC.grow_corn(land_area_val, biomass_yield)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = CGE.ethanol_grain(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = GEU.upgrade_grain_ethanol(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)

#Calculate EROI
eroi = LCA.calcEROI(IO_array)


jet_a_out = 0
diesel_out = 0
gasoline_out = 0
ethanol_out = 0
biodiesel_out = 0
electricity_out = 0


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
            

transport_fuel_energy = ((43.2*jet_a_out) + (42.975*diesel_out) + 
        (43.44*gasoline_out) + (26.95*ethanol_out) + (37.75*biodiesel_out))


# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array)

# Calculate GHG Impact at Farm Gate
ghg_impact_farm = Ag_LCA.calcGHGImpactAg(biomass_IO, transport_fuel_energy)

# Calculate MFSP
mfsp = TEA.calc_MFSP(IO_array)

# Calculate Minimum Crop Selling Price at Farm Gate
mcsp = Ag_TEA.calc_MCSP(biomass_IO)

# CheckSum for spreadsheet/Python agreement
bp_in = UF.sumProcessIO(results_array, D.biomass_production, D.tl_input)

conv_in = UF.sumProcessIO(results_array, D.conv, D.tl_input)

upgr_in = UF.sumProcessIO(results_array, D.upgrading, D.tl_input)

bp_out = UF.sumProcessIO(results_array, D.biomass_production, D.tl_output)

conv_out = UF.sumProcessIO(results_array, D.conv, D.tl_output)

upgr_out = UF.sumProcessIO(results_array, D.upgrading, D.tl_output)


# eroi_chksm = 2.51
# ghg_impact_chksm = 41.87
mfsp_chksm = 1.39

print('Executed Corn Grain Fermentation to Ethanol PM')
