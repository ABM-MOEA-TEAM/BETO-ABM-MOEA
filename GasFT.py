import TEA_LCA_Data as D
import UnivFunc as UF

# Forestry Values
forestry_cited_values_dict = {}
forestry_cited_values_dict['Water'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Water'], 6350.275, 'kg/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Steam'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Steam'], 3169.375, 'kg/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['FT Catalysts'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['FT Catalysts'], 1.483835301, 'kg/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Air'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Air'], 16728.5375, 'kg/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Propane'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Propane'], 283.16925, 'kg/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Electricity'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Electricity'], 9907.812, 'MJ/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Labor'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Labor'], 69.71, 'dollars/yr/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Capital Cost'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Capital Cost'], 7547.02, 'dollars/ha',
    'Swanson, 2010')
forestry_cited_values_dict['Land Capital Cost'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Land Capital Cost'], 0.000001, 'dollars/ha',
    'Swanson, 2010')        # Need an empty but present value for non-vert. int.

forestry_out_vals = {}
forestry_out_vals['Syncrude'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Syncrude'], 6154.35, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['Slag'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Slag'], 656.925, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['CO2 Gas'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['CO2 Gas'], 11349.32058, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['Nitrogen Gas'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Nitrogen Gas'], 12614.1125, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['Hydrogen'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Hydrogen'], 23.05, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['Wastewater'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Wastewater'], 8655.275, 'kg/yr/ha',
    'Swanson, 2010')
forestry_out_vals['Electricity'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Electricity'], 17873.892, 'MJ/yr/ha',
    'Swanson, 2010')

# Grass Conversion IO
conv_in_list = ['Water', 'Steam', 'FT Catalysts', 'Air',
                'Propane', 'Electricity', 'Labor', 'Capital Cost','Land Capital Cost']
conv_out_list = ['Syncrude', 'Slag', 'CO2 Gas', 'Nitrogen Gas', 'Hydrogen',
                 'Wastewater', 'Electricity']

# Grass Extraction/Conversion        
def convertGrassBiomass(size, biomass_IO_array):
    return_array = UF.createEmptyFrame()
    forestry_vals = forestry_cited_values_dict
    forestry_out = forestry_out_vals
    
    in_list = conv_in_list
    out_list = conv_out_list
    match_list = [[UF.input_or_output, D.tl_output],
                  [UF.substance_name, 'Woody Biomass']]
    grass_biomass_out_qty = UF.returnPintQty(biomass_IO_array, match_list)
    scaling_param = size.qty * (grass_biomass_out_qty/
                    (size.qty * D.forestry_woody_biomass_val.qty))
    
    # special write of woody biomass
    return_array.loc[0] = UF.getWriteRow('Woody Biomass', D.conv, 
                                      D.tl_input, grass_biomass_out_qty)
    
    row_count = 1

    for substance in in_list:
        pint_qty = scaling_param*forestry_vals[substance].qty
        return_array.loc[row_count] = UF.getWriteRow(substance, D.conv, 
                                                  D.tl_input, pint_qty)
        row_count += 1
        
    for substance in out_list:
        pint_qty = scaling_param*forestry_out[substance].qty
        return_array.loc[row_count] = UF.getWriteRow(substance, D.conv, 
                                                  D.tl_output, pint_qty)
        row_count += 1
        
    
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty('Land Area', 100, 'hectare')
    biomass_output = D.TEA_LCA_Qty('Woody Biomass', 8960, 'kg/yr/ha')
    biomass_IO_array = UF.createEmptyFrame()
    biomass_IO_array.loc[0] = UF.getWriteRow('Woody Biomass', D.biomass_production, 
                                      D.tl_output, biomass_output.qty*land_area_val.qty)
    return convertGrassBiomass(land_area_val, biomass_IO_array)


if __name__ == "__main__":
    output = main()