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
import LCA

# Process steps
import Corn_Stover_Cultivation as CSC
import Corn_Stover_Ethanol as CSE
import Stover_Ethanol_Upgrade as SEU

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

stover_collected = 0.5

# Biomass Production
biomass_IO = CSC.grow_stover(land_area_val, yearly_precip)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = CSE.ethanol_stover(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)

# Upgrading
upgrading_IO = SEU.upgrade_stover_ethanol(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)

#Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Calculate GHG Impact
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


# eroi_chksm = 2.51
# ghg_impact_chksm = 41.87
# mfsp_chksm = 8.24


