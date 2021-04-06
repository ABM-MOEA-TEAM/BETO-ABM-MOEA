import pandas as pd
import pint
import os
from pathlib import Path
cwd = os.getcwd()
ureg = pint.UnitRegistry()
ureg.define('dollars = [money]')
ureg.define('cuttings = [seed]')

def returnPintQtyObj(magnitude, units):
    return magnitude * ureg.parse_expression(units)

class TEA_LCA_Qty:
    def __init__(self, substance, magnitude, units):
        # self.ureg = ureg
        if 'Quantity' in str(type(magnitude)):
            self.qty = magnitude
        else:
            self.qty = magnitude * ureg.parse_expression(units)
                
        self.substance = substance
               
class TEA_LCA_Qty_Cited:
    def __init__(self, substance, magnitude, units, citation):
        self.substance = substance
        self.citation = citation
        self.qty = magnitude * ureg.parse_expression(units)
        
class Qty_Cited:
    def __init__(self, name_str, magnitude, units, citation):
        self.name_str = name_str
        self.citation = citation
        self.qty = magnitude * ureg.parse_expression(units)
        
class Substance:
    def __init__(self, name_str, id_str):
        self.name_str = name_str
        self.id_str = id_str

# Paths and hard-coded strings
path_list = [Path(cwd + '/LCA_Inventory.csv'), 
             Path(cwd + '/Substances.csv')]

# LCA Inventory Variables
LCA_key_str = 'Key_String'
LCA_IO = 'In_or_out'
LCA_units = 'Default_Unit'
LCA_energy_impact = 'Energy_Impact (MJ/X)'
LCA_cost = 'Cost'
LCA_GHG_impact = 'GHG_Impact'
LCA_inventory_df = pd.read_csv(path_list[0])

# Get [short] list of substances that are NOT fungible, depends on LCA Inventory
sub_list = []
nonfunglist = []
for i in range(len(LCA_inventory_df)):
    row = LCA_inventory_df.loc[i]
    if row[LCA_key_str] in sub_list:
        nonfunglist.append(row[LCA_key_str])
    else:
        sub_list.append(row[LCA_key_str])

# Keyword Strings
tl_input = 'Input'
tl_output = 'Output'
zeroed = 'Zeroed Out'
biomass_production = 'Biomass Production'
conv = 'Conversion/Extraction'
upgrading = 'Upgrading'
comb = 'Combustion'
cons = 'Consolidated'

# Substance Variables
substance_id = 'substance_id'
substance_full_string = 'substance_full_string'
substances_df = pd.read_csv(path_list[1])

substance_dict = {}
substance_id_dict = {}
for i in range(len(substances_df)):
    row = substances_df.loc[i]
    substance_dict[row[substance_full_string]] = Substance(row[substance_full_string],
                                                  row[substance_id])
    substance_id_dict[row[substance_id]] = Substance(row[substance_full_string],
                                                  row[substance_id])

# Assorted cited values used in calculations
N20_emit_proportion = Qty_Cited(
    'N2O emissions due to N fertilizer application', 0.01325, 'dimensionless',
    'Zhang et al., 2013')
CO2_fixing_proportion_grass = Qty_Cited(
    'kg of atmospheric CO2 per kg grass biomass', (11.0/6.0), 'dimensionless',
    'unknown')
forestry_woody_biomass_val = TEA_LCA_Qty_Cited(
    substance_dict['Woody Biomass'], 11525, 'kg/yr/ha',
    'Average of Kreutz et al., 2008--FT fuels from coal and switchgrass and Beal 2018 ABECCS')