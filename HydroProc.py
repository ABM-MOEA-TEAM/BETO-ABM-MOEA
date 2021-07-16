# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 07:31:26 2021

@author: Jack Smith
"""

import TEA_LCA_Data as D
import UnivFunc as UF
import Soy_Cultivation as SC
import Hexane_Extraction as HE

def Hydro_Processing(conversion_IO_array):
    
    return UF.Collect_IndepVars_Loop('HydroProc', 0, 0, 1, conversion_IO_array,
                                     'Soybean Oil', 2, 0)

def main():
    
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 100, 'hectare')
    yield_value = 3698
    biomass_IO_array = SC.grow_soybean(land_area_val, yield_value)
    conversion_IO_array = HE.Hexane_Extraction(biomass_IO_array)
    return Hydro_Processing(conversion_IO_array)

if __name__ == "__main__":
    output = main()