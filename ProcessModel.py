# Data and Universal Functions
import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import Ag_TEA
import LCA
import Ag_LCA

# Process steps
import Grow_Grass as GG
import GasFT as GFT
import Hydroprocessing as H


# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 8960, 'kg/yr/ha')
# biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 17933, 'kg/yr/ha')
# Second variable exists so that I could verify that the lookup table output is the same as 
# the PM execution (note the difference in magnitude of yield)

biomass_IO = GG.growGrassForOneYear(land_area_val, biomass_output)

results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = GFT.convertGrassBiomass(land_area_val, results_array)
results_array = results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = H.upgradeGrassProducts(land_area_val,results_array)
results_array = results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)

# Calculate EROI
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
            
        if 'Electricity' in subst_name and in_or_out == D.tl_output:
            electricity_out = UF.returnPintQty(IO_array, [[UF.substance_name, 'Electricity'],    
                                            [UF.input_or_output, D.tl_output]]).magnitude 
            
transport_fuel_energy = ((43.2*jet_a_out) + (42.975*diesel_out) + 
        (43.44*gasoline_out) + (26.95*ethanol_out) + (37.75*biodiesel_out))



# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array)

# Calculate GHG Impact at Farm Gate
ghg_impact_farm = Ag_LCA.calcGHGImpactAg(biomass_IO, transport_fuel_energy)

# Calculate MFSP
mfsp = TEA.calc_MFSP(IO_array)

# Calculate MCSP at Farm Gate
mcsp = Ag_TEA.calc_MCSP(biomass_IO)

# CheckSum for spreadsheet/Python agreement
bp_in = UF.sumProcessIO(results_array, D.biomass_production, D.tl_input)
bp_in_chksm = 4182843.33
conv_in = UF.sumProcessIO(results_array, D.conv, D.tl_input)
conv_in_chksm = 4321198.198
upgr_in = UF.sumProcessIO(results_array, D.upgrading, D.tl_input)
upgr_in_chksm = 614186.0335
bp_out = UF.sumProcessIO(results_array, D.biomass_production, D.tl_output)
bp_out_chksm = 896156.35
conv_out = UF.sumProcessIO(results_array, D.conv, D.tl_output)
conv_out_chksm = 4456826.453
upgr_out = UF.sumProcessIO(results_array, D.upgrading, D.tl_output)
upgr_out_chksm = 448586.7008

eroi_chksm = 2.51
ghg_impact_chksm = 41.87    # with updated inventory - closer to 42.32 (3/8/21)
mfsp_chksm = 8.24           # with updated inventory - closer to  8.78 (3/8/21)

# print('Executed Switchgrass Gasification to Jet PM')