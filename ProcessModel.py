# Data and Universal Functions
import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import LCA

# Process steps
import Grow_Grass as GG
import Grow_Grass2 as GG2
import GasFT as GFT
import Hydroprocessing as H


# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')

biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 8960, 'kg/yr/ha')

ScalingValue = 1000
# Biomass Production

biomass_IO = GG.growGrassForOneYear(land_area_val, biomass_output)
#biomass_IO = GG2.growGrassPerKg(land_area_val, biomass_output, ScalingValue)
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

# Calculate GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array)

# Calculate MFSP
mfsp = TEA.calc_MFSP(IO_array)

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
ghg_impact_chksm = 41.87
mfsp_chksm = 8.24
