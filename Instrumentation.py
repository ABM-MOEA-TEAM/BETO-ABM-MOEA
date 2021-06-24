# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:02:53 2021

@author: Jack Smith
"""
import UnivFunc as UF

corn_stover_25 = UF.DayCentYields('stover_yield_Mg_ha', 1)
corn_stover_50 = UF.DayCentYields('stover_yield_Mg_ha', 2)
corn_stover_75 = UF.DayCentYields('stover_yield_Mg_ha', 3)

corn_grain = UF.DayCentYields('corn_yield_Mg_ha', 0)

soy_yield = UF.DayCentYields('soy_yield_Mg_ha', 0)