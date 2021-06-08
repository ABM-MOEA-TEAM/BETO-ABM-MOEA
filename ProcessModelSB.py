 # -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:52:42 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

import TEA
import Ag_TEA
import LCA
import Ag_LCA

# Process steps
import Soy_Cultivation as SC
import Soy_Diesel as SD
import Soy_Diesel_Upgrade as SDU

import os
from pathlib import Path
cwd = os.getcwd()

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()
# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
yield_value = 3698
#yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

Ag_only = bool(False)
AllocationID = 3

# Biomass Production
biomass_IO = SC.grow_soy(land_area_val, yield_value)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = SD.diesel_soy(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)
ds_results_array = ds_results_array.append(conversion_IO, ignore_index=True)

# # Upgrading
upgrading_IO = SDU.upgrade_soy_diesel(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)
ds_results_array =ds_results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
ds_IO_array = UF.consolidateIO(ds_results_array)
#IO_ds_array = UF.consolidateIO()
# Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Read prodlist .csv
cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)
print(ghg_impact)

# Calculate GHG Impact at Farm Gate
MJ_out = 23635
ghg_impact_farm = Ag_LCA.calcGHGImpactAg(biomass_IO, MJ_out)

# Calculate MFSP
mfsp = (TEA.calc_MFSP(IO_array, prod, coprods) * 135.13) # MJ/Gal BD (Check)
new_mfsp = (TEA.calc_MFSP(ds_IO_array, prod, coprods) * 135.13) # MJ/Gal BD
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

mfsp_chksm = 2.57

print('Executed Soybean Transesterification to Biodiesel PM')