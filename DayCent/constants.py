#!/bin/python

"""A centralized place to store conversion factors and other constants.
"""

ha_per_ACRE = 0.404686
kg_per_bu_CORN = 25.4012
kg_per_bu_SOY = 27.2
g_m2_to_Mg_ha = 0.01
g_m2_to_kg_ha = 10.0
kg_ha_to_Mg_ha = 0.001

C_concentration = 0.45
N_to_N2O = 44.013/28.014
C_to_CO2 = 44.009/12.011
N2O_GWP100_AR5 = 265.0   # from WG1AR5_Chapter08_FINAL.pdf, Appendix 8.A
CH4_GWP100_AR5 = 28.0   # from WG1AR5_Chapter08_FINAL.pdf, Appendix 8.A
VOLITN_iN2ON_EF = 0.01   # kg N2O-N/kg N volatilized, from 2006 IPCC Guidelines for National Greenhouse Gas Inventories; Volume 4: Agriculture, Forestry and Other Land Use; Ch. 11, Table 11.3
LEACHN_iN2ON_EF = 0.0075   # kg N2O-N/kg N leached, from 2006 IPCC Guidelines for National Greenhouse Gas Inventories; Volume 4: Agriculture, Forestry and Other Land Use; Ch. 11, Table 11.3
