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

import os
from pathlib import Path
cwd = os.getcwd()

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 8960, 'kg/yr/ha')
# biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 17933, 'kg/yr/ha')
# Second variable exists so that I could verify that the lookup table output is the same as 
# the PM execution (note the difference in magnitude of yield)

biomass_IO = GG.growGrassForOneYear(land_area_val, biomass_output)

results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = GFT.convertGrassBiomass(land_area_val, results_array)
results_array = results_array.append(conversion_IO, ignore_index=True)
ds_results_array = ds_results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = H.upgradeGrassProducts(land_area_val,results_array)
results_array = results_array.append(upgrading_IO, ignore_index=True)
ds_results_array = ds_results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
ds_IO_array = UF.consolidateIO(ds_results_array)

# Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Read prodlist .csv
cwd = os.getcwd()    
path_list = [Path(cwd + '/grass_jet_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)
print(ghg_impact)
# Calculate GHG Impact at Farm Gate
#ghg_impact_farm = Ag_LCA.calcGHGImpactAg(biomass_IO, transport_fuel_energy)

# Calculate MFSP
mfsp = (TEA.calc_MFSP(IO_array, prod, coprods) * 152.79) # MJ/Gal Jet-A
new_mfsp = (TEA.calc_MFSP(ds_IO_array, prod, coprods) * 152.79) # MJ/Gal Jet-A
print(new_mfsp)

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