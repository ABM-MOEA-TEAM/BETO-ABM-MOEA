# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:53:49 2020

@author: Jacks074
"""
import pandas as pd
import Corn_Stover_Cultivation as CS_Cult

Material_Flows = pd.Series([18876,151,52,18366,140,5.244,0.903,80.676,0.744,1.042,
                            1.488,0.223,0.276,8.700,6,71,137,10],
                           ["Water_DAH","H2SO4_DAH","NH3_DAH","Water_EH","Glucose_EP",
                            "NH3_EP","SO2_EP","CSL_EP","Corn_Oil_EP","AmSulf_EP",
                            "PotSulf_EP","MgSulf_EP","CaCl2_EP","DAP_EP","CSL_F",
                            "Flue_Gas_WT","NaOH_WT","Gas"])

def Ethanol_Stover():
    
    Biomass = CS_Cult.grow_Stover()
    Biomass = round(Biomass)
    
    #   Block 200 - Size Reduction and Comminution Process
    
        #   Hammer mill is used to reduce the size of the corn stover particulates (believe it is 5mm)
    
    Matl_Pass_Thru = 0.97
    Biomass = Biomass*Matl_Pass_Thru    # Expecting to lose some mass on input (grate)
    
    kWh_Per_Tonne_200 = 39
    MJ_Per_kg_Stover = kWh_Per_Tonne_200 / 1000 * 3.6
    
    Comminution_Elec = MJ_Per_kg_Stover * Biomass
    Matl_Handling_E_200 = 66.61
    
    #   Block 300 - Dilute Acid Hydrolysis
    
        #   Sulfuric Acid is used to break down the biomass feedstock (Ammonia is used to neutralize)
    
    Ratio_Water_Stover_300 = 4
    Perc_Acid_By_Weight = 0.08
    Molar_Mass_H2SO4 = 98.079       #   Gram/Mole
    Molar_Mass_NH3 = 17.031
    Base_To_Neutralize = ((Molar_Mass_NH3 * 2/Molar_Mass_H2SO4))       #   Molar Mass NH3 * 2 / Molar Mass H2SO4
                                    #   Verify that two is the proper stoich. Coeff
    C_P_Water   = 4.84              #   kJ/kg*C
    C_P_Stover  = 1.03              
    C_P_H2SO4   = 1.34
    Final_T_300 = 175               #   C
    Init_T_300  = 20                #   C
    Total_Mass_Conv_Perc_300 = 0.9730
    
    Dilution_Water_300 = Ratio_Water_Stover_300 * Biomass
    Acid_Weight = Perc_Acid_By_Weight * Dilution_Water_300 / 10
    
    
    Q_Reqd      = (Dilution_Water_300 * C_P_Water *(Final_T_300 - Init_T_300)) + (Biomass*C_P_Stover*(Final_T_300 - Init_T_300)) + (Acid_Weight* C_P_H2SO4*(Final_T_300 - Init_T_300))
    
    Pre_Hydrolysate = Biomass + Dilution_Water_300 + Acid_Weight + Base_To_Neutralize
    Biomass = Biomass * Total_Mass_Conv_Perc_300
    Waste_Water_300 = Pre_Hydrolysate - Biomass
    Matl_Handling_E_300 = 224.30
    
    #   Block 400 - Enzymatic Hydrolysis
    
        #   Enzyme Added in final breakdown step
        
    Ratio_Water_Hydrolysate_400  = 4
    Ratio_Cellulase_Cellulose    = 0.02
    Final_T_400                  = 175
    Init_T_400                   = 48
    
    Dilution_Water_400 = Biomass * Ratio_Water_Hydrolysate_400
    Cellulase = Ratio_Cellulase_Cellulose * Biomass * 0.4105        #   Ratio Cellulase
    
    Q_Cooling_400 = (Biomass * C_P_Stover*(Final_T_400 - Init_T_300))/1000
    Matl_Handling_E_400 = 50.21
    
    Hydrolysate = Biomass + Dilution_Water_400 + Cellulase
    Biomass = Biomass
    
    #   Block 500 - Enzyme Production 
    
        #   Nutrients required to grow the cellulase enzyme
        
    Matl_Handling_E_500            = 1343.51
    # Glucose_500         = Material_Flows([4])
    # Ammonia_500         = Material_Flows([5])
    # SO2_500             = Material_Flows([6])
    # CSL_500             = Material_Flows([7])
    # Corn_Oil_500        = Material_Flows([8])         Don't know if these are needed beyond
    # Ammon_Sulf_500      = Material_Flows([9])         The input matrix
    # Potass_Phosph_500   = Material_Flows([10])
    # Mag_Sulf_500        = Material_Flows([11])
    # Calc_Chlor_500      = Material_Flows([12])
    # DAP_500             = Material_Flows([13])
    
    #   Block 600 - Fermentation 
    
    Corn_Beer           = Hydrolysate
    Matl_Handling_E_600 = 50.21
    
    Glucose_Proportion  = 0.406815352
    Xylose_Proportion   = 0.210313
    Gay_Lussac_Yield    = 0.511         #   Maximum stoichiometric yield
    Overall_Yield_Eff   = 0.931
    Gluc_to_Eth         = 0.95
    Xylose_to_Eth       = 0.83
    
    Biomass_To_Eth = (Glucose_Proportion * Gluc_to_Eth)+(Xylose_Proportion * Xylose_to_Eth)
    
    Ethanol = Biomass_To_Eth * Biomass * Gay_Lussac_Yield * Overall_Yield_Eff
    
    #   Block 700 - Distillation and Dehydration 
    
    Matl_Handling_E_700 = 3089.34
    Heating_Power_700   = 11960.03
    
    Ethanol = round(Ethanol)
    
    Matl_Handl_Series = pd.Series([Matl_Handling_E_200, Matl_Handling_E_300, Matl_Handling_E_400,
                                  Matl_Handling_E_500, Matl_Handling_E_600, Matl_Handling_E_700],
                                  ["MHE_200","MHE_300","MHE_400","MHE_500","MHE_600","MHE_700"])
    
    return Ethanol
