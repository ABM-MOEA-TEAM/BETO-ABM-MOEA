# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 11:48:27 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF

import TEA
import LCA

import Soy_Cultivation as SC
import Hexane_Extraction as HE
import Transesterification as T

import os
from pathlib import Path

results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()

land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
biomass_yield = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 10974, 'kg/ha/yr')

results_array = UF.createEmptyFrame()
ds_results_array = UF.createEmptyFrame()
biomass_IO = SC.grow_soybean(land_area_val, biomass_yield)
results_array = results_array.append(biomass_IO, ignore_index=True)
conversion_IO = HE.Hexane_Extraction(biomass_IO)
results_array = results_array.append(conversion_IO, ignore_index=True)
upgrading_IO = T.Transesterification(conversion_IO)
results_array = results_array.append(upgrading_IO, ignore_index=True)
IO_array = UF.consolidateIO(results_array)

cwd = os.getcwd()    
path_list = [Path(cwd + '/soy_biodiesel_prodlist.csv')]

pathname = path_list[0]

prod = UF.returnProdlist(pathname)
coprods = UF.returnCoProdlist(pathname)

MFSP = TEA.calc_MFSP(IO_array, prod, coprods)
print(MFSP*37.75)

NPV_Biomass = TEA.calc_NPV(biomass_IO)
NPV_Conversion = TEA.calc_NPV(conversion_IO)
NPV_Upgrading = TEA.calc_NPV(upgrading_IO)

Biomass_Conversion_array = UF.createEmptyFrame()
Conversion_Upgrading_array = UF.createEmptyFrame()

Biomass_Conversion_array = Biomass_Conversion_array.append(biomass_IO, ignore_index=True)
Biomass_Conversion_array = Biomass_Conversion_array.append(conversion_IO, ignore_index=True)

Conversion_Upgrading_array = Conversion_Upgrading_array.append(conversion_IO, ignore_index=True)
Conversion_Upgrading_array = Conversion_Upgrading_array.append(upgrading_IO, ignore_index=True)

NPV_BC_Consolidated = UF.consolidateIO(Biomass_Conversion_array)
NPV_CU_Consolidated = UF.consolidateIO(Conversion_Upgrading_array)

NPV_Biomass_Conversion = TEA.calc_NPV(NPV_BC_Consolidated)
NPV_Conversion_Upgrading = TEA.calc_NPV(NPV_CU_Consolidated)

