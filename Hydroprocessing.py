import TEA_LCA_Data as D
import UnivFunc as UF

forestry_upgr_in = {}
forestry_upgr_in['Syncrude'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Syncrude'], 6154.35, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_in['Hydrogen'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Hydrogen'], 23.05, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_in['Electricity'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Electricity'], 1095.336, 'MJ/yr/ha',
    'Swanson, 2010')
forestry_upgr_in['Labor'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Labor'], 13.94, 'dollars/yr/ha',
    'Swanson, 2010')
forestry_upgr_in['Capital Cost'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Capital Cost'], 613.43, 'dollars/ha',
    'Swanson, 2010')

forestry_upgr_out = {}
forestry_upgr_out['Jet-A'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Jet-A'], 435.645, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_out['Water'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Water'], 3693.7625, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_out['Propane'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Propane'], 283.16925, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_out['Diesel'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Diesel'], 893.07225, 'kg/yr/ha',
    'Swanson, 2010')
forestry_upgr_out['Gasoline'] = D.TEA_LCA_Qty_Cited(
    D.substance_dict['Gasoline'], 464.39757, 'kg/yr/ha',
    'Swanson, 2010')

# Grass Upgrading IO
upgr_in_list = ['Syncrude', 'Hydrogen', 'Electricity', 
                'Labor', 'Capital Cost']
upgr_out_list = ['Jet-A', 'Water', 'Propane', 
                 'Diesel', 'Gasoline']


# Grass Upgrading     
def upgradeGrassProducts(size, conv_IO_array):
    return_array = UF.createEmptyFrame()
    forestry_vals = forestry_upgr_in
    forestry_out = forestry_upgr_out
    in_list = upgr_in_list
    out_list = upgr_out_list
    match_list = [[UF.input_or_output, D.tl_output],
                  [UF.substance_name, 'Woody Biomass']]
    grass_biomass_out_qty = UF.returnPintQty(conv_IO_array, match_list)
    scaling_param = size.qty * (grass_biomass_out_qty/
                        (size.qty * D.forestry_woody_biomass_val.qty))
    
    row_count = 0

    for substance in in_list:
        pint_qty = scaling_param*forestry_vals[substance].qty
        return_array.loc[row_count] = UF.getWriteRow(substance, D.upgrading, 
                                                  D.tl_input, pint_qty)
        row_count += 1
        
    for substance in out_list:
        pint_qty = scaling_param*forestry_out[substance].qty
        return_array.loc[row_count] = UF.getWriteRow(substance, D.upgrading, 
                                                  D.tl_output, pint_qty)
        row_count += 1
        
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty('Land Area', 100, 'hectare')
    biomass_output = D.TEA_LCA_Qty('Woody Biomass', 8960, 'kg/yr/ha')
    conv_IO_array = UF.createEmptyFrame()
    conv_IO_array.loc[0] = UF.getWriteRow('Woody Biomass', D.biomass_production, 
                                      D.tl_output, biomass_output.qty*land_area_val.qty)
    return upgradeGrassProducts(land_area_val, conv_IO_array)


if __name__ == "__main__":
    output = main()