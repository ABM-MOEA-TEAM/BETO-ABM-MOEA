# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:45:55 2021

@author: Jack Smith
"""
# Attempt to construct a Process Model file which only executes Agricultural block step
# and then returns minimum crop selling price
import TEA_LCA_Data as D
import UnivFunc as UF

# Bolt on TEA and LCA
import TEA
import LCA

# Process steps
import Grow_Grass as GG


# Initialize our results dataframe
results_array = UF.createEmptyFrame()

# Initialize the input values for PM execution (yield will be replaced by DayCent values)
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
biomass_output = D.TEA_LCA_Qty(D.substance_dict['Woody Biomass'], 17933, 'kg/yr/ha')

biomass_IO = GG.growGrassForOneYear(land_area_val, biomass_output)                          # In order to mimic new farm-land purchase, I think we will
                                                                                            # need to add an additional argument to the grow-grass step
                                                                                            # to switch on/off additional capital cost (currently omitting)
results_array = results_array.append(biomass_IO, ignore_index=True)

# Which executes just fine - Now we need to modify the existing TLAs to accept only biomass as the product
Ag_only = bool(True)

MCSP = TEA.calc_MFSP(results_array,Ag_only)*1000

MCSP = round(MCSP)

print(MCSP)
