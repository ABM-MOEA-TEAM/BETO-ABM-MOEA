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

import TEA_LCA_Data as D
import UnivFunc as UF

#   Writing each of the substances to a dictionary as above is only really justified if you can leverage a 
#   For-loop in the calculation part of the model. As the relationships get more complex, this gets infeasible.

#   What is the non-dictionary procedure for altering the units?

##############################################
################# GROWTH #####################
##############################################


#   Definition of relevant variables (faux inputs):
    
land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')

yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')    

stover_collected = 0.5 

#   Not a substance, so updating the .csv does not seem like the proper path forward.
#   Is this an acceptable way to define this?

# stover_scaling_dict = {}    # For units - I am currently scaling everything based off of rainfall 
#                                 # the percentage of stover collected...
    
# stover_scaling_dict['Rain Water (Blue Water'] = D.TEA_LCA_Qty(
#      D.substance_dict['Rain Water (Blue Water)'], 253236, 'kg/yr/in')
       
def grow_stover(size,yearly_precip):
    
#    scales = stover_scaling_dict
 
    return_array = UF.createEmptyFrame()    
    # A local instantiation of the return array datafram is preferable, here

    # These following lines perform the same write operation that the for-loop
    # does, but individually.  The for-loop should only be applied when the 
    # relationship for each substance is exactly the same (which will not be 
    # the case as the Xcel process model relationships are brought in to the
    # program)   
    
    ############    INPUTS    ###############    
    
    scale1 = D.TEA_LCA_Qty(D.substance_dict['Corn Seed'], 17.69, 'kg/ha/yr')
       
    return_array.loc[0] = UF.getWriteRow('Corn Seed', D.biomass_production, 
                                      D.tl_input, scale1.qty*size.qty)
    
    # The operation above, then, writes in to the return array the amount of 
    # corn seed needed, scaled up by 17.69 kg/ha/yr
    
    scale2 = D.TEA_LCA_Qty(D.substance_dict['Nitrogen in Fertilizer'], 161.37, 'kg/ha/yr')
    
    return_array.loc[1] = UF.getWriteRow('Nitrogen in Fertilizer', D.biomass_production,
                                      D.tl_input, scale2.qty*size.qty)
    
    scale3 = D.TEA_LCA_Qty(D.substance_dict['Phosphorus in Fertilizer'], 15.65, 'kg/ha/yr')
    
    return_array.loc[2] = UF.getWriteRow('Phosphorus in Fertilizer', D.biomass_production,
                                      D.tl_input, scale3.qty*size.qty)
    
    scale4 = D.TEA_LCA_Qty(D.substance_dict['Potassium in Fertilizer'], 76.09, 'kg/ha/yr')
    
    return_array.loc[3] = UF.getWriteRow('Potassium in Fertilizer', D.biomass_production,
                                      D.tl_input, scale4.qty*size.qty)
    
    scale5 = D.TEA_LCA_Qty(D.substance_dict['Ag Lime (CaCO3)'], 452, 'kg/ha/yr')
    
    return_array.loc[4] = UF.getWriteRow('Ag Lime (CaCO3)', D.biomass_production,
                                      D.tl_input, scale5.qty*size.qty)
    
    scale6 = D.TEA_LCA_Qty(D.substance_dict['Herbicide'], 1.21, 'kg/ha/yr')
    
    return_array.loc[5] = UF.getWriteRow('Herbicide', D.biomass_production,
                                      D.tl_input, scale6.qty*size.qty)
    
    # Stover_Collected_FV = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'kg/in')
    
    # Running into an issue with the units; if I am scaling off of the inches of rainfall
    # for the substance production of other flows. I need a faux variable to get them to read properly;
    
    scale7 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 253236, 'kg/in/ha/yr')
    
    return_array.loc[6] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_input, scale7.qty*yearly_precip.qty*size.qty)
   
    # I also need to go in and add things like the economic value associated with the process,
    # as well as other inputs which haven't been updated in Substances.csv (especially the 
    # km*tons that the trucks are required to move; within pathway optimization parameters.)
    
    ############    OUTPUTS   ###############
    
    # QUESTION - What is proper to name the Corn Stover left on the field vs
    # the stover collected? i.e. must they always have a corresponding entry 
    # in the 'substances' .csv?
    
    scale8 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Collected'], 327.24, 'kg/in/ha/yr')
    
    return_array.loc[7] = UF.getWriteRow('Corn Stover Collected', D.biomass_production, 
                                      D.tl_output, scale8.qty*yearly_precip.qty*stover_collected*size.qty)
    
    # Again, hard-coded value relates the inches of precipation to total kg
    # stover produced. The more complex relationship may be brought in from 
    # Excel, but my assumption is that a lookup operation will take its place
    # in the near future anyway.
    
    scale9 = D.TEA_LCA_Qty(D.substance_dict['Corn Stover Left'], 327.24, 'kg/in/ha/yr')
    
    return_array.loc[8] = UF.getWriteRow('Corn Stover Left', D.biomass_production, 
                                      D.tl_output, scale9.qty*yearly_precip.qty*size.qty*(1-stover_collected))
    
    scale10 = D.TEA_LCA_Qty(D.substance_dict['Corn Grain'], 369.02, 'kg/in/ha/yr')
    
    return_array.loc[9] = UF.getWriteRow('Corn Grain', D.biomass_production, 
                                      D.tl_output, scale10.qty*yearly_precip.qty*size.qty)
    
    scale11 = D.TEA_LCA_Qty(D.substance_dict['Capital Cost'], 2300, 'dollars/ha/yr')
    
    return_array.loc[10] = UF.getWriteRow('Capital Cost', D.biomass_production,
                                      D.tl_input, scale11.qty*size.qty)
    
    scale12 = D.TEA_LCA_Qty(D.substance_dict['Land Capital Cost'], 16549, 'dollars/ha/yr')
    
    return_array.loc[11] = UF.getWriteRow('Land Capital Cost', D.biomass_production,
                                      D.tl_input, scale12.qty*size.qty)
    
    scale13 = D.TEA_LCA_Qty(D.substance_dict['Labor'], 33.33333, 'dollars/ha/yr')
    
    return_array.loc[12] = UF.getWriteRow('Labor', D.biomass_production,
                                      D.tl_input, scale13.qty*size.qty)
    
    scale14 = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'], 252875, 'kg/in/ha/yr') # Total water eventually returned
    
    return_array.loc[13] = UF.getWriteRow('Rain Water (Blue Water)', D.biomass_production,
                                      D.tl_output, scale14.qty*yearly_precip.qty*size.qty)
    
    return return_array

def main():
    land_area_val = D.TEA_LCA_Qty(D.substance_dict['Land Area'], 1, 'hectare')
    yearly_precip = D.TEA_LCA_Qty(D.substance_dict['Rain Water (Blue Water)'],34,'inches')
    return grow_stover(land_area_val, yearly_precip)

if __name__ == "__main__":
    output = main()