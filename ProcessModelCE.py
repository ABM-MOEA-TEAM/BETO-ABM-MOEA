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


import os
from pathlib import Path
cwd = os.getcwd()

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

yield_value = 5563.08 # will be replaced by the DayCent values

stover_collected = 0.5 # Not currently being used (4/5)

# Biomass Production
biomass_IO = CSC.grow_stover(land_area_val, yield_value)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = CSE.ethanol_stover(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)
ds_results_array = ds_results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = SEU.upgrade_stover_ethanol(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)
ds_results_array = ds_results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
ds_IO_array = UF.consolidateIO(ds_results_array)

# If we end up doing a mass allocation in the TEA steps, it might make sense
# to replace the "IO_array" as I don't know if we're using it any longer

# After executing the three process model blocks, we now determine the total
# MJ's of output fuel produced by the pathway. We may then pass that energy out
# value to the Ag_LCA block as an additional argument to allow us to find 
# gCO2eq/MJ at the farm gate (and facilitate allocation)

cwd = os.getcwd()    
path_list = [Path(cwd + '/stover_ethanol_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

#Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Calc GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)
print(ghg_impact)
                      
# Calculate MFSP
mfsp = (TEA.calc_MFSP(IO_array, prod, coprods) * 80.49) # MJ/Gal EtOH
new_mfsp = (TEA.calc_MFSP(ds_IO_array, prod, coprods) * 80.49) # MJ/Gal EtOH
print(new_mfsp)

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
mfsp_chksm = 2.40

print('Executed Corn Stover Fermentation to Ethanol PM')
