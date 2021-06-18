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

import os
from pathlib import Path
cwd = os.getcwd()

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

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
ds_results_array = ds_results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = GEU.upgrade_grain_ethanol(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)
ds_results_array = ds_results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
ds_IO_array = UF.consolidateIO(ds_results_array)

#Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Read prodlist .csv
cwd = os.getcwd()    
path_list = [Path(cwd + '/grain_ethanol_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)
# print(ghg_impact)

# Calculate MFSP
# mfsp = (TEA.calc_MFSP(IO_array, prod, coprods) * 80.49) # MJ/Gal EtOH
new_mfsp = (TEA.calc_MFSP(ds_IO_array, prod, coprods) * 80.49) # MJ/Gal EtOH
print(new_mfsp)

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
mfsp_chksm = 1.29

print('Executed Corn Grain Fermentation to Ethanol PM')
