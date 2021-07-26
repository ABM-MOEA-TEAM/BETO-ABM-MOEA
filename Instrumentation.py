# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:02:53 2021

@author: Jack Smith
"""
import UnivFunc as UF
import TEA_LCA_Data as D
import Soy_Cultivation as SC
import TEA 

# land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
# yield_value = 3017  # Not actually used (need to remove - 6/24)

# biomass_IO = SC.grow_soybean(land_area_val, yield_value)

# output = TEA.calc_NPV(biomass_IO)

output = UF.collectIndepVars('SoyCult')

# corn_stover_25 = UF.DayCentYields('stover_yield_Mg_ha', 1)
# corn_stover_50 = UF.DayCentYields('stover_yield_Mg_ha', 2)
# corn_stover_75 = UF.DayCentYields('stover_yield_Mg_ha', 3)

# corn_grain = UF.DayCentYields('corn_yield_Mg_ha', 0)

# soy_yield = UF.DayCentYields('soy_yield_Mg_ha', 0)