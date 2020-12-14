# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 10:49:51 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np

def p(V):
    
    #####################################################################
    ##########           IMPORT DATA           ##########################
    #####################################################################
    
    # import county level data
    df_data = pd.read_csv('simple_paths.csv',header=0)
    
    per_unit_costs = df_data['Cost ($/gge)'] 
    per_unit_GHG = df_data['Post-Combustion GHG (g CO2e/MJ)']
    per_unit_land = df_data['Arable Land (m2/GJ/yr)']
    per_unit_N = df_data['Nitrogen (g/GJ)']
    energy_content = df_data['Energy Content (GJ/gal)']
    
    pu_costs = per_unit_costs, # costs
    pu_GHG = per_unit_GHG, # emissions
    pu_land = per_unit_land,
    pu_N = per_unit_N # N fertilizer
        
    # Empty variables 
    total_costs = 0 # $
    total_GHG = 0 # g
    total_land = 0# m2
    total_N = 0 #g
            
    for i in range(0,len(pu_costs)):
        
        total_costs += V[i]*pu_costs[i] 
        total_GHG += V[i]*pu_GHG[i]*energy_content[i]*1000
        total_land += V[i]*pu_land[i]*energy_content[i]
        total_N += V[i]*pu_N[i]*energy_content[i]
    
    # convert back to per unit
    price = total_costs/sum(V) # $/gal
    ghg = (total_GHG/sum(V))*(1/energy_content[0])*(1/1000)#g CO2/MJ
    land = (total_land/sum(V))*(1/energy_content[0]) #m2/yr/GJ
    N = (total_N/sum(V))*(1/energy_content[0]) #g N/GJ
    
    # Returns list of objectives, Constraints
    return [price, ghg, land, N]
