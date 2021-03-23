# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 22:07:39 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import LCA

# Process steps
import Corn_Grain_Cultivation as CGC


# Initialize our results dataframe
results_array = UF.createEmptyFrame()

# Initialize the input values for PM execution (yield will be replaced by DayCent values)
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'],10974,'kg/ha/yr')

biomass_IO = CGC.grow_corn(land_area_val, biomass_yield)                                    # In order to mimic new farm-land purchase, I think we will
                                                                                            # need to add an additional argument to the grow-grass step
                                                                                            # to switch on/off additional capital cost (currently omitting)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Which executes just fine - Now we need to modify the existing TLAs to accept only biomass as the product
Ag_only = bool(True)

MCSP = TEA.calc_MFSP(results_array,Ag_only)*1000 # Need a new loop for Ag only Process Set

MCSP = round(MCSP)

print(MCSP)
