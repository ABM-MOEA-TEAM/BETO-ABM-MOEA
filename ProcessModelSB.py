# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:52:42 2021

@author: Jack Smith
"""
import TEA_LCA_Data as D
import UnivFunc as UF

import TEA
import TEA2
import LCA

# Process steps
import Soy_Cultivation as SC
import Soy_Diesel as SD
import Soy_Diesel_Upgrade as SDU

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

Ag_only = bool(False)
AllocationID = 3

# Biomass Production
biomass_IO = SC.grow_soy(land_area_val, yearly_precip)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = SD.diesel_soy(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)

# # Upgrading
upgrading_IO = SDU.upgrade_soy_diesel(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)

# Calculate EROI
# eroi = LCA.calcEROI(IO_array)

# # Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array)

# Calculate MFSP
mfsp = TEA.calc_MFSP(IO_array)




# CheckSum for spreadsheet/Python agreement
bp_in = UF.sumProcessIO(results_array, D.biomass_production, D.tl_input)
conv_in = UF.sumProcessIO(results_array, D.conv, D.tl_input)
upgr_in = UF.sumProcessIO(results_array, D.upgrading, D.tl_input)
bp_out = UF.sumProcessIO(results_array, D.biomass_production, D.tl_output)
conv_out = UF.sumProcessIO(results_array, D.conv, D.tl_output)
upgr_out = UF.sumProcessIO(results_array, D.upgrading, D.tl_output)

mfsp_chksm = 2.87

print('Executed Soybean Transesterification to Biodiesel PM')