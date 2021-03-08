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
import LCA

# Process steps
import Corn_Grain_Cultivation as CGC
import Corn_Grain_Ethanol as CGE
import Grain_Ethanol_Upgrade as GEU

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'],10974,'kg/ha/yr')
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
#eroi = LCA.calcEROI(IO_array)

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
mfsp_chksm = 1.39

print('Executed Corn Grain Fermentation to Ethanol PM')
