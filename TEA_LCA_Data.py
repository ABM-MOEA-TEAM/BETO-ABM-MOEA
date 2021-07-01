import pandas as pd
import pint
import os
from pathlib import Path
import xlsxwriter

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
        
class Probability_Distribution:
    def __init__(self, dist_name, avg, std_dev):
        self.dist_name = dist_name
        self.avg = avg
        self.std_dev = std_dev
        
# Paths and hard-coded strings
path_list = [Path(cwd + '/LCA_Inventory.csv'), 
             Path(cwd + '/Substances.csv'),
             Path(cwd + '/AltJet_Excerpt_Example.xlsx'),
             Path(cwd + '/CSU_All_Pathway_TEALCA_062421.xlsx')]

# LCA Inventory Variables
LCA_key_str = 'Key_String'
LCA_IO = 'In_or_out'
LCA_units = 'Default_Unit'
LCA_energy_impact = 'Energy_Impact (MJ/X)'
LCA_cost = 'Cost'
LCA_GHG_impact = 'GHG_Impact'
LCA_inventory_df = pd.read_csv(path_list[0])
# LCA_inventory_df = pd.read_excel(path_list[3],'LCI')

# Going to just try switching the read source over to the all_pathways sheet (6/29)

# Get [short] list of substances that are NOT fungible, depends on LCA Inventory
# sub_list = []
# nonfunglist = []
# for i in range(len(LCA_inventory_df)):
#     row = LCA_inventory_df.loc[i]
#     if row[LCA_key_str] in sub_list:
#         nonfunglist.append(row[LCA_key_str])
#     else:
#         sub_list.append(row[LCA_key_str])

DoNotConsolidateList = ['Electricity', 
                        'Diesel',
                        'Gasoline',
                        'Water']
# DoNotConsolidateList.append('Electricity')# 
# DoNotConsolidateList.append('Diesel')
# DoNotConsolidateList.append('Gasoline')
# DoNotConsolidateList.append('Water')

# Non-funglist is an explicit list of substance to not be added/aggegregated.
# This prevents the non-vertically integrated case from functioning
# (5/25) Change to more "Do not consolidate List" - prescribe each substance
# which is not to be consolidated. 

# Keyword Strings
tl_input = 'Input'
tl_output = 'Output'
zeroed = 'Zeroed Out'
biomass_production = 'Biomass Production'
conv = 'Conversion/Extraction'
upgrading = 'Upgrading'
comb = 'Combustion'
cons = 'Consolidated'

# Related to Monte Carlo
normal = 'Normal'

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

# Heating Values for each output substance (NOTE - 4/13 - 
# need to change these to HHV's as they are currently the LHV's)
# NP: Can also use TEA_LCA_Qty_Cited class to embed the citation in the object
HHV_dict = {}

HHV_dict['LNG'] = TEA_LCA_Qty(substance_dict['LNG'], 50, 'MJ/kg')       # AltJet
HHV_dict['Ethanol'] = TEA_LCA_Qty(substance_dict['Ethanol'], 26.95, 'MJ/kg')
HHV_dict['Diesel'] = TEA_LCA_Qty(substance_dict['Diesel'], 42.975, 'MJ/kg')
HHV_dict['Gasoline'] = TEA_LCA_Qty(substance_dict['Gasoline'], 43.44, 'MJ/kg')
HHV_dict['Jet-A'] = TEA_LCA_Qty(substance_dict['Jet-A'], 43.2, 'MJ/kg')
HHV_dict['Biodiesel'] = TEA_LCA_Qty(substance_dict['Biodiesel'], 37.75, 'MJ/kg')
HHV_dict['Corn Grain'] = TEA_LCA_Qty(substance_dict['Corn Grain'], 16.1, 'MJ/kg') # https://feedtables.com/charts/energy-mj
HHV_dict['Corn Stover'] = TEA_LCA_Qty(substance_dict['Corn Stover'], 17.64, 'MJ/kg') # https://www.researchgate.net/publication/277311384_Ash_Content_and_Calorific_Energy_of_Corn_Stover_Components_in_Eastern_Canada
HHV_dict['DDGS'] = TEA_LCA_Qty(substance_dict['DDGS'], 22.7,'MJ/kg') # https://agritrop.cirad.fr/582534/1/ID582534.pdf
HHV_dict['Soybean Meal'] = TEA_LCA_Qty(substance_dict['Soybean Meal'], 16.12,'MJ/kg') # https://nutrition.ansci.illinois.edu/sites/default/files/AnimFeedSciTechnol188.64-73.pdf
HHV_dict['Glycerol'] = TEA_LCA_Qty(substance_dict['Glycerol'], 25.3,'MJ/kg') # https://www.intechopen.com/books/biofuels-status-and-perspective/glycerol-as-a-raw-material-for-hydrogen-production
HHV_dict['Electricity'] = TEA_LCA_Qty(substance_dict['Electricity'], 1, 'MJ/MJ')
HHV_dict['Biochar'] = TEA_LCA_Qty(substance_dict['Biochar'], 20.55, 'MJ/kg') # https://www.sciencedirect.com/science/article/pii/S258929912030046X#:~:text=The%20calorific%20value%20of%20the,potential%20use%20as%20solid%20fuel.

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

# EXAMPLE load of xlsx spreadsheet using tab name
grass_io_df = pd.read_excel(path_list[2], sheet_name='Grass IO')
user_lci_df = pd.read_excel(path_list[2], sheet_name='User Defined LCI')
npv_parameters_df = pd.read_excel(path_list[2], sheet_name='NPV Parameters')

distribution_list = [Probability_Distribution(normal, 0, 0.5)]
