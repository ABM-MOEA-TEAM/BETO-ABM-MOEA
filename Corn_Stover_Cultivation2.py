# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:11:55 2020

@author: Jack Smith
"""
#   This File represents the conversion of the "Bounded Rain Cellulosic Ethanol" PM 
#   Agricultural Growth and Conversion steps.  

##############################################
#################  SETUP #####################
##############################################

import pandas as pd
import TEA_LCA_Data as D
import UnivFunc as UF

#   Conversions (Consider making this a separate module or script or whatever the proper term is)

km_per_mi       = 1.60934
acre_per_ha     = 2.47105
kg_per_BuC      = 25.4      # Note that BuC here denotes a Bushel of Corn
kg_per_lbs      = 0.453515
ton_per_kg      = 0.001102
BuC_per_kg      = 0.03937
L_per_Gal       = 3.78541
acrft_per_Gal   = 0.00000306889
m3_per_Gal      = 0.003785 

#   Instantiate Pandas dataframe type to handle material flows 

# Material_Flows = pd.Series([17.69,161.37,15.65,76.09,125.52,9.06,91.35,25.78,452,1.213,34,50],
#                            ["Seeds","NitrogenFert","PhosphFert","PotassiumFert","NitrogenInt","PhosphInt","PotassiumInt","SulfurInt","Aglime","Herbicide","Precip (in)","StoverCollected (%)"])

stover_inputs_dict = {}
stover_inputs_dict['Corn Seed'] = D.TEA_LCA_Qty(
    D.substance_dict['Corn Seed'],17.69,'kg/yr/ha')
stover_inputs_dict['Nitrogen in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Nitrogen in Fertilizer'],161.37,'kg/yr/ha')
stover_inputs_dict['Phosphorus in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Phosphorus in Fertilizer'],15.65,'kg/yr/ha')
stover_inputs_dict['Potassium in Fertilizer'] = D.TEA_LCA_Qty(
    D.substance_dict['Potassium in Fertilizer'],76.09,'kg/yr/ha')
stover_inputs_dict['Ag Lime (CaCO3)'] = D.TEA_LCA_Qty(
    D.substance_dict['Ag Lime (CaCO3)'],452,'kg/yr/ha')
stover_inputs_dict['Herbicide'] = D.TEA_LCA_Qty(
    D.substance_dict['Herbicide'],1.213,'kg/yr/ha')
stover_inputs_dict['Rain Water (Blue Water)'] = D.TEA_LCA_Qty(
    D.substance_dict['Rain Water (Blue Water)'],34,'kg/yr/ha')
# stover_inputs_dict['Stover Collected (%)'] = D.TEA_LCA_Qty(       # While this is a helpful parameter, it is not an input mass flow
#     D.substance_dict['Stover Collected (%)'],50,'kg/yr/ha')

stover_outputs_dict = {}

##############################################
################# GROWTH #####################
##############################################


#   Definition of relevant variables:
    
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

biomass_output = D.TEA_LCA_Qty(D.substance_dict['Corn Stover'], 5563, 'kg/yr/ha')    

grain_output = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 12456, 'kg/yr/ha')

return_array = UF.createEmptyFrame()
    
def grow_Stover(size,biomass_production):
    # seeds = stover_inputs_dict[0,1]
    # NFert = stover_inputs_dict[1]
    # PFert = stover_inputs_dict[2]
    # KFert = stover_inputs_dict[3]
    # Aglime = stover_inputs_dict[4]
    # Herb = stover_inputs_dict[5]
    # Precip = stover_inputs_dict[6]
    
    crop_inputs = stover_inputs_dict
    crop_outputs = stover_outputs_dict   
    
    # Calculate Atmospheric CO2 based on biomass output
    return_array.loc[0] = UF.getWriteRow('Atmospheric CO2', D.biomass_production, 
                                      D.tl_input, 
                biomass_output.qty*size.qty*D.CO2_fixing_proportion_grass.qty)
    
    # special write of woody biomass
    return_array.loc[1] = UF.getWriteRow('Corn Stover', D.biomass_production, 
                                      D.tl_output, biomass_output.qty*size.qty)
    
    return_array.loc[2] = UF.getWriteRow('Corn Grain', D.biomass_production,
                                      D.tl_output, grain_output.qty*size.qty)
    
    row_count = 3
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
#   Calculation and Modeling:    
    
    # Block 110 - Land Dedication and Seeding
    
        # What do with the mass of seeds? Do I update Material_Flows?
    
    # Block 120 - Water Throughput
    
        # Probably do not need to list the amount of water we expect Not to collect
    
    # Block 130 - Fertilizers (N, P, K)
        
    # NTot = NFert + NInt
    # PTot = PFert + PInt       Not yet needed. How complex is altering the dataframe if 
    # KTot = KFert + KInt       we decided we needed such values?
    
    # Block 140 - Soil pH Management
    
        # Expended on the Field
    
    # Block 160 - Herbicide Application
        
        # Atrazine for Corn Stover Production, could consider adding drop-down list
        
    # Block 170 - Crop Operations 
    
    Labor_170 = 2.965
    Diesel_170 = 56.124     # Liters of Diesel
    
    # Block 180 - Growth and Harvest Yield
    
    # Precip_kg = Precip/12 * acre_per_ha / acrft_per_Gal * m3_per_Gal *997
    
    Water_Cons = 0.541693991        # Water which actually goes through some corn plant throughout the year
                                    # everything else does not interact with the corn, not really worth 
                                    # quantifying, but the 'growth' model is set up to take this route.
                                    # Would be good to clean this up before discussion even starts about 
                                    # integrating a specific growth model or collecting growth data.
                                    
    Water_Thru = 0.997700642        # And the other value which I am not happy about. I am concerned that
                                    # Python is going to interpret this as a particular variable type and
                                    # that we will run into a truncation error at some point. Again, worth 
                                    # changing this to something more intuitive/simple (i.e. soy growth)
                                    
    # Water_avail = Precip_kg * Water_Cons
    # Water_Cycled_thru = Water_avail * Water_Thru
    
    # Water_Struct = Water_avail - Water_Cycled_thru  # The amount of water which remains with the plant for 
                                                    # the construction of the cell walls, etc. The matter
    
    # Growth_SF = Water_Struct/10724.24131            # Scaling factor for the growth logic/behavior
    
    # a = (Growth_SF - 1)**(1.75)
    # b = - abs(a)
    # c = Water_Struct**b
    # d = Water_Struct - 10724.24131
    
    # H20_Ratio_BM = 1*Water_Struct     # 
    # H20_Ratio_BM = Water_Struct + (Water_Struct - 10724.24131)*(Water_Struct**(-abs((Growth_SF - 1)**1.75)))
    
                                    # And this is the gross calculation. The hardcoded 10724 value is the avg
                                    # amount of water which stays in the corn plants.  The Growth Scaling Factor
                                    # is responsible for the attenuation of the impact that more or less rain has
                                    # 1.75 was selected by personal preference/expectation of plany behavior based
                                    # on the rain present each year; changing this will change how sensitive the 
                                    # corn plant is to the changing rainfall. 
    
    Biomass_Produced = 4864.4   # Assumes plant is 46% carbon by mass
    
    Corn_Grain = 0.53 * Biomass_Produced            # This ratio needs a citation
    Corn_Stover_Tot = 0.47 * Biomass_Produced
    
    StoverCollected = .5
    Corn_Stover = Corn_Stover_Tot * StoverCollected / 100
    Corn_Stover_Unused = Corn_Stover_Tot - Corn_Stover
    
    # CO2_Sequestered = H20_Ratio_BM / 0.436 * (12.017/44.01)  
    
    # Block 190 - Transportation to Biorefinery
    
    Tonne_Cap_Truck = 20    # Citation Needed
    
    Avg_Dist = 35.36 * km_per_mi    # I believe that I had a reference which claimed the average corn-stover
                                    # plant traveled fifty miles to bioprocessing, but I cannot locate that source.
                                    # Another possibility is that the assumptions for the TEA portion of the CS model
                                    # assume material is collected within a radius of 50 miles... 
                                    # 35.36 represents 50/sqrt(2), as I believe (though my geometry is very rusty) that
                                    # this represents the average distance to the centroid that any point in the circle
                                    # might have. 
                                    
    Trucks_reqd = Corn_Stover / (Tonne_Cap_Truck * 1000)
    
        # I think it might be worth converting from trucks required to tonne*km, 
        # I believe that Dr. Kern did so for the MOEA and that this is the standard
        # practice for this calculation
    
    # Post-processing and Aggregation:
    
    # Materials_Reqd_CS_Cult = pd.Series.replace(0, Corn_Stover)
    # Materials_Reqd_CS_Cult = pd.Series.replace(1, Corn_Stover_Unused)
    # Materials_Reqd_CS_Cult = pd.Series.replace(2, Corn_Grain)
    # Materials_Reqd_CS_Cult = pd.Series.replace(3, Labor_170)
    # Materials_Reqd_CS_Cult = pd.Series.replace(4, Diesel_170)
    # Materials_Reqd_CS_Cult = pd.Series.replace(5, Trucks_reqd)
    #Materials_Reqd_CS_Cult = pd.Series(1,2,3,4,5,6)
    # print(Materials_Reqd_CS_Cult)
    # print(Corn_Grain)
    # return Corn_Stover
    
    return Corn_Stover
    # print("\n")
    # print("Required Materials for CS Cultivation (kg / ha)")
    # print("\n")
    # print(Material_Flows)
    # print("\n")
    # print("\n")
    # print("Material Outputs from CS Cultivation (kg / ha)")
    # print("\n")
    # print(Matl_Reqd_CS_Cult)