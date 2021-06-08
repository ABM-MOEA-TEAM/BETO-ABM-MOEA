# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 09:58:54 2021

@author: jacks074
"""

# Data and Universal Functions
import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import LCA

# Process steps
import algae_cult_placeholder as ACP
import HTL_algae as HTLa

import os
from pathlib import Path
cwd = os.getcwd()

# Initialize empty Process Model output table
results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

# Scaling Value
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
pathway_ID = 1


biomass_IO = ACP.grow_algae(land_area_val)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Extraction/Conversion
conversion_IO = HTLa.HTL_algae(biomass_IO, pathway_ID)
results_array = results_array.append(conversion_IO, ignore_index=True)
ds_results_array = ds_results_array.append(conversion_IO, ignore_index=True)

# Process Control Vol IO
IO_array = UF.consolidateIO(results_array)
ds_IO_array = UF.consolidateIO(ds_results_array)

cwd = os.getcwd()    
path_list = [Path(cwd + '/algae_htl_diesel_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

#Calculate EROI
eroi = LCA.calcEROI(IO_array)

# Calc GHG Impact
ghg_impact = LCA.calcGHGImpact(IO_array, prod, coprods)
                            
# Calculate MFSP
mfsp = (TEA.calc_MFSP(IO_array, prod, coprods) * 42.975) # MJ/Gal Diesel
new_mfsp = (TEA.calc_MFSP(ds_IO_array, prod, coprods) * 42.975) # MJ/Gal Diesel
print(new_mfsp)