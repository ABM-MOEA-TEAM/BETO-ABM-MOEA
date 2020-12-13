"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time

start = time.time()

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import county level data
df_data = pd.read_csv('simple_paths.csv',header=0)

per_unit_costs = df_data['Cost ($/gge)'] 
per_unit_GHG = df_data['Post-Combustion GHG (g CO2e/MJ)']
per_unit_land = df_data['Arable Land (m2/GJ/yr)']
energy_content = df_data['Energy Content (GJ/gal)']

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
    
# simulation model (function to be evaluated by MOEA)
def simulate(
        vars, # energy produced gallons each fuel
        pu_costs = per_unit_costs, # costs
        pu_GHG = per_unit_GHG, # emissions
        pu_land = per_unit_land
        ):
    
    # Empty variables 
    total_costs = 0 # $
    total_GHG = 0 # g
    total_land = 0# m2
    
    Constraints = [] # constraints
    
    for i in range(0,len(pu_costs)):
        
        total_costs += vars[i]*pu_costs[i] 
        total_GHG += vars[i]*pu_GHG[i]*energy_content[i]*1000
        total_land += vars[i]*pu_land[i]*energy_content[i]
        Constraints.append(-vars[0])
        
    Constraints.append(12000000000 - sum(vars))
    Constraints = list(Constraints)
    
    # convert back to per unit
    price = total_costs/sum(vars) # $/gal
    ghg = (total_GHG/sum(vars))*(1/energy_content[0])*(1/1000)#g CO2/MJ
    land = (total_land/sum(vars))*(1/energy_content[0]) #m2/yr/GJ
    
    # Returns list of objectives, Constraints
    return [price, ghg, land], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Define Platypus problem

# Number of variables, constraints, objectives
num_variables = len(per_unit_costs)
num_constraints = len(per_unit_costs) + 1
num_objs = 3

problem = Problem(num_variables,num_objs,num_constraints)
problem.types[:] = Real(0,12000000000)
problem.constraints[:] = "<=0"

#What function?
problem.function = simulate

# What algorithm?
algorithm = NSGAII(problem)

# Evaluate function # of times
algorithm.run(100000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# limit evalutaion to 'feasible' solutions
feasible_solutions = [s for s in algorithm.result if s.feasible]

D = np.zeros((len(feasible_solutions),num_variables))
O = np.zeros((len(feasible_solutions),num_objs))

for s in feasible_solutions:
    
    idx = feasible_solutions.index(s)
    # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)

    #record solution information
    for i in range(0,num_variables):
        D[idx,i] = s.variables[i]
    for j in range(0,num_objs):
        O[idx,j] = s.objectives[j]

df_D = pd.DataFrame(D)
df_D.to_csv('Decision_Variables.csv')

df_O = pd.DataFrame(O)
df_O.columns = ['Price','GHG','Land']
df_O.to_csv('Objective_Functions.csv')


from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# marker sizes
# S = (df_O['GHG']/max(df_O['GHG']))*60

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(df_O['Price'], df_O['GHG'], df_O['Land'], c=df_O['Price'], cmap=cm.PiYG, edgecolor = 'black', linewidth = 0.2,s=df_O['GHG'],alpha=1)
ax.view_init(35, 130)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('GHG (g CO2/MJ)')
ax.set_zlabel('Land (m2/GJ)')

cbar = plt.colorbar(p, fraction=0.05, pad=0.1, shrink=0.5)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels, title='GHG (g CO2/MJ)',loc='upper left',fontsize=8,framealpha=1)

plt.savefig('fig1.tiff',dpi=300)
plt.show()

# 2D tradeoff plots
fig = plt.figure()

ax = fig.add_subplot(111)
p = ax.scatter(df_O['Price'], df_O['GHG'], c=df_O['Price'], cmap=cm.PiYG, edgecolor = 'black', linewidth = 0.2,s=df_O['GHG'],alpha=1)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('GHG (g CO2/MJ)')

cbar = plt.colorbar(p, fraction=0.1, shrink=0.8)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels,title='GHG (g CO2/MJ)',loc='upper left',fontsize=8,frameon=False,framealpha=1)

plt.savefig('fig2.tiff',dpi=300)
plt.show()


fig = plt.figure()

ax = fig.add_subplot(111)
p = ax.scatter(df_O['Price'], df_O['Land'], c=df_O['Price'], cmap=cm.PiYG, edgecolor = 'black', linewidth = 0.2,s=df_O['GHG'],alpha=1)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('Land(m2/GJ)')

cbar = plt.colorbar(p, fraction=0.1, shrink=0.8)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels,title='GHG (g CO2/MJ)', loc='upper left',fontsize=8,frameon=False,framealpha=1)

plt.savefig('fig3.tiff',dpi=300)
plt.show()

fig = plt.figure()

ax = fig.add_subplot(111)
p = ax.scatter(df_O['GHG'], df_O['Land'], c=df_O['Price'], cmap=cm.PiYG, edgecolor = 'black', linewidth = 0.2,s=df_O['GHG'],alpha=1)
ax.set_xlabel('GHG (g CO2/MJ)')
ax.set_ylabel('Land(m2/GJ)')

cbar = plt.colorbar(p, fraction=0.1, shrink=0.8)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels,title='GHG (g CO2/MJ)',loc='upper right',fontsize=8,frameon=False,framealpha=1)

plt.savefig('fig4.tiff',dpi=300)
plt.show()


 

# obj1 = []
# obj2 = []

# for s in feasible_solutions:
#     obj1.append(s.objectives[0])
#     obj2.append(s.objectives[1])
    
# min_obj1_idx = obj1.index(min(obj1))
# min_obj2_idx = obj2.index(min(obj2))

# # find solutions' standardized distance to ideal (origin)
# distance_to_origin_pct = []

# for s in feasible_solutions:
#     d = ((s.objectives[0]/max(obj1))**2 + (s.objectives[1]/max(obj2))**2)**0.5
#     distance_to_origin_pct.append(d)

    
# # select range of standardized solutions to map
# sorted_distance = np.sort(distance_to_origin_pct)
# idx = []
# idx_obj1 = []
# for i in range(0,99,9):
#     idx.append(distance_to_origin_pct.index(sorted_distance[i]))
#     idx_obj1.append(obj1[i])
    
# # display the tradeoff frontier    
# import matplotlib.pyplot as plt

# plt.scatter([s.objectives[0]/1000 for s in feasible_solutions],
#             [s.objectives[1] for s in feasible_solutions],c='red',alpha=0.5)

# plt.scatter(obj1[min_obj1_idx]/1000,obj2[min_obj1_idx],s=60,c='cyan',edgecolors='gray')
# plt.scatter(obj1[min_obj2_idx]/1000,obj2[min_obj2_idx],s=60,c='cyan',edgecolors='gray')

# for i in idx:
    
#     plt.scatter(obj1[i]/1000,obj2[i],s=60,c='cyan',edgecolors='gray')
    
# plt.xlabel("Costs ($1000s)")
# plt.ylabel("Distance (km)")
# plt.show()


# # visualize (map) solutions
# from urllib.request import urlopen
# import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
# import plotly.express as px
# import plotly.io as pio
# pio.renderers.default='jpg'

# # plot in descending order from Obj1
# df_combined = pd.DataFrame()
# df_combined['idx'] = idx
# df_combined['obj1'] = idx_obj1
# df_sorted = df_combined.sort_values(by='obj1',ascending=False).reset_index(drop=True)


# # map minimum obj1 solution
# s = np.array(feasible_solutions[min_obj1_idx].variables)
# df_results = pd.DataFrame()
# df_results['fips'] = fips
# df_results['CS_ha'] = s
# df_results['fips'] = df_results['fips'].apply(str)
# fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 50),
#                            scope="usa",
#                            labels={'CS_ha':'Corn Stover Hectares'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()

# # map rest of selected solutions
# for i in range(0,len(df_sorted)):
#     j = df_sorted.loc[i,'idx']
#     s = np.array(feasible_solutions[j].variables)
#     df_results = pd.DataFrame()
#     df_results['fips'] = fips
#     df_results['CS_ha'] = s
#     df_results['fips'] = df_results['fips'].apply(str)
#     fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                                color_continuous_scale="Viridis",
#                                range_color=(0, 50),
#                                scope="usa",
#                                labels={'CS_ha':'Corn Stover Hectares'}
#                               )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.show()

# # map minimum obj2 solution
# s = np.array(feasible_solutions[min_obj2_idx].variables)
# df_results = pd.DataFrame()
# df_results['fips'] = fips
# df_results['CS_ha'] = s
# df_results['fips'] = df_results['fips'].apply(str)
# fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 50),
#                            scope="usa",
#                            labels={'CS_ha':'Corn Stover Hectares'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()


    
# # # plot status quo
# ax.scatter(x/1000,y,-z,c='blue',s=36)
# ax.set_xlabel("Developer Profits ($1000s)")
# ax.set_ylabel("Ratio")
# ax.set_zlabel("Monthly Variability")

# plt.show()



