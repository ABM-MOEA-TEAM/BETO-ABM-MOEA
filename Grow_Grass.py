import TEA_LCA_Data as D
import UnivFunc as UF

# Grass Biomass Production IO
grass_inputs_dict = {}
grass_inputs_dict['Nitrogen in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Nitrogen in Fertilizer'], 118, 'kg/yr/ha')
grass_inputs_dict['Phosphorus in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Phosphorus in Fertilizer'], 22.25, 'kg/yr/ha')
grass_inputs_dict['Potassium in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Potassium in Fertilizer'], 10, 'kg/yr/ha')
grass_inputs_dict['Herbicide'] = D.TEA_LCA_Qty(
    D.substance_dict['Herbicide'], 2.398987661, 'kg/yr/ha')
grass_inputs_dict['Insecticide'] = D.TEA_LCA_Qty(
    D.substance_dict['Insecticide'], 0.005118259, 'kg/yr/ha')
grass_inputs_dict['Grass Seed'] = D.TEA_LCA_Qty(
    D.substance_dict['Grass Seed'], 1.122727273, 'kg/yr/ha')
grass_inputs_dict['Diesel'] = D.TEA_LCA_Qty(
    D.substance_dict['Diesel'], 15.65646375, 'kg/yr/ha')
grass_inputs_dict['Labor'] = D.TEA_LCA_Qty(
    D.substance_dict['Labor'], 33.33333333, 'dollars/yr/ha')
grass_inputs_dict['Land Capital Cost'] = D.TEA_LCA_Qty(
    D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha')
grass_inputs_dict['Capital Cost'] = D.TEA_LCA_Qty(
    D.substance_dict['Capital Cost'], 2300, 'dollars/ha')
grass_inputs_dict['Rain Water (Blue Water)'] = D.TEA_LCA_Qty(
    D.substance_dict['Rain Water (Blue Water)'], 6350, 'meter ** 3/yr/ha')

grass_outputs_dict = {}

fert_mag = (D.N20_emit_proportion.qty 
            * grass_inputs_dict['Nitrogen in Fertilizer'].qty)
grass_outputs_dict['Fertilizer N2O'] = D.TEA_LCA_Qty(
    D.substance_dict['Fertilizer N2O'], fert_mag, fert_mag)

# Grass Biomass Production       
def growGrassForOneYear(size, biomass_output):
    return_array = UF.createEmptyFrame()
    
    
    crop_inputs = grass_inputs_dict
    crop_outputs = grass_outputs_dict   
    
    # Calculate Atmospheric CO2 based on biomass output
   
   
    return_array.loc[0] = UF.getWriteRow('Atmospheric CO2', D.biomass_production, 
                                      D.tl_input, 
                biomass_output.qty*size.qty*D.CO2_fixing_proportion_grass.qty)
    
    # special write of woody biomass
    return_array.loc[1] = UF.getWriteRow('Woody Biomass', D.biomass_production, 
                                      D.tl_output, biomass_output.qty*size.qty)
    
    row_count = 2
    # Scale crop inputs
    for key in crop_inputs:
        pint_qty = size.qty*crop_inputs[key].qty
        return_array.loc[row_count] = UF.getWriteRow(key, D.biomass_production, 
                                                  D.tl_input, pint_qty)
        row_count += 1
        
    # Scale crop outputs
    for key in crop_outputs:
        pint_qty = size.qty*crop_outputs[key].qty
        return_array.loc[row_count] = UF.getWriteRow(key, D.biomass_production, 
                                                  D.tl_output, pint_qty)
        row_count += 1
        
    return return_array
        
    # else: 
    #     BMProduced = D.TEA_LCA_Qty(D.substance_dict, biomass_output, 'kg/ha')
        
        
    #     return_array.loc[0] = UF.getWriteRow('Atmospheric CO2', D.biomass_production, 
    #                                       D.tl_input, 
    #                 BMProduced.qty*size.qty*D.CO2_fixing_proportion_grass.qty)
        
    #     # special write of woody biomass
    #     return_array.loc[1] = UF.getWriteRow('Woody Biomass', D.biomass_production, 
    #                                       D.tl_output, BMProduced.qty*size.qty)
        
    #     row_count = 2
    #     # Scale crop inputs
    #     for key in crop_inputs:
    #         pint_qty = size.qty*crop_inputs[key].qty
    #         return_array.loc[row_count] = UF.getWriteRow(key, D.biomass_production, 
    #                                                   D.tl_input, pint_qty)
    #         row_count += 1
            
    #     # Scale crop outputs
    #     for key in crop_outputs:
    #         pint_qty = size.qty*crop_outputs[key].qty
    #         return_array.loc[row_count] = UF.getWriteRow(key, D.biomass_production, 
    #                                                   D.tl_output, pint_qty)
    #         row_count += 1
    #     print('Engaged')
    #     print('Yield for specific county - ', BMProduced.qty)
    #     return return_array
        
    
    
def main():
    land_area_val = D.TEA_LCA_Qty('Land Area', 100, 'hectare')
    biomass_output = D.TEA_LCA_Qty('Woody Biomass', 8960, 'kg/yr/ha')
    return growGrassForOneYear(land_area_val, biomass_output)


if __name__ == "__main__":
    output = main()