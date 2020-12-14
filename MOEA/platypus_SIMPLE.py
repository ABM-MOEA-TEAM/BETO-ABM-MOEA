"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time
import pass_through

start = time.time()

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

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
    
# simulation model (function to be evaluated by MOEA)
def simulate(
        vars, # energy produced gallons each fuel
        pu_costs = per_unit_costs, # costs
        pu_GHG = per_unit_GHG, # emissions
        pu_land = per_unit_land,
        pu_N = per_unit_N # N fertilizer
        ):
    
    # Empty variables 
    total_costs = 0 # $
    total_GHG = 0 # g
    total_land = 0# m2
    total_N = 0 #g
    
    Constraints = [] # constraints
    
    for i in range(0,len(pu_costs)):
        
        total_costs += vars[i]*pu_costs[i] 
        total_GHG += vars[i]*pu_GHG[i]*energy_content[i]*1000
        total_land += vars[i]*pu_land[i]*energy_content[i]
        total_N +=vars[i]*pu_N[i]*energy_content[i]
        Constraints.append(-vars[0])
        
    Constraints.append(12000000000 - sum(vars))
    Constraints = list(Constraints)
    
    # convert back to per unit
    price = total_costs/sum(vars) # $/gal
    ghg = (total_GHG/sum(vars))*(1/energy_content[0])*(1/1000)#g CO2/MJ
    land = (total_land/sum(vars))*(1/energy_content[0]) #m2/yr/GJ
    N = (total_N/sum(vars))*(1/energy_content[0]) #g N/GJ
    
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

variables = ["Soybean HEPA","Corn AF","Forestry Biomass FT","Grasses FT","Marine Microalgae HTL"]
df_D.columns = variables
for i in range(0,len(variables)):
    df_O[variables[i]] = df_D[variables[i]]
    
N = []

for i in range(0,len(df_O)):
    total_N = 0
    gals = 0
    
    for j in variables:
        
        var_idx = variables.index(j)
        total_N += df_O.loc[i,j]*per_unit_N[var_idx]*energy_content[var_idx]
        gals += df_O.loc[i,j]

    N.append(total_N*(1/gals)*(1/energy_content[0]))

df_O['N'] = N
    

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 3D plot

_min = min(df_O['Price'])
_max = max(df_O['Price'])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(df_O['Price'], df_O['GHG'], df_O['Land'], c=df_O['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=df_O['GHG'],alpha=1)
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

# plot decision variables
labels = ["Soybean\nHEPA","Corn\nAF","Forestry\nBiomass FT","Grasses\nFT","Marine\nMicroalgae HTL"]

# min price
price_list = list(df_O['Price'])
idx = price_list.index(min(price_list))
plt.figure()
plt.bar(labels,df_D.iloc[idx,:])
plt.xticks(fontsize=8,wrap=True)
plt.ylabel('Gallons')
plt.xlabel('Source')
plt.savefig('fig5.tiff',dpi=300)
plt.show()

# min GHG
GHG_list = list(df_O['GHG'])
idx = GHG_list.index(min(GHG_list))
plt.figure()
plt.bar(labels,df_D.iloc[idx,:])
plt.xticks(fontsize=8,wrap=True)
plt.ylabel('Gallons')
plt.xlabel('Source')
plt.savefig('fig6.tiff',dpi=300)
plt.show()

# min land
land_list = list(df_O['Land'])
idx = land_list.index(min(land_list))
plt.figure()
plt.bar(labels,df_D.iloc[idx,:])
plt.xticks(fontsize=8,wrap=True)
plt.ylabel('Gallons')
plt.xlabel('Source')
plt.savefig('fig7.tiff',dpi=300)
plt.show()


# scenario - Cost <$8/gge and post-combustion GHG <70 g/MJ
A = df_O[df_O['Price']<8]
B = A[A['GHG']<70]
C = pd.concat([df_O,B]).drop_duplicates(keep=False)

# 3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(C['Price'], C['GHG'], C['Land'], c=C['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=C['GHG'],alpha=0.2)
b = ax.scatter(B['Price'], B['GHG'], B['Land'], c=B['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=B['GHG'],alpha=1)
ax.view_init(35, 130)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('GHG (g CO2/MJ)')
ax.set_zlabel('Land (m2/GJ)')

cbar = plt.colorbar(b, fraction=0.05, pad=0.1, shrink=0.5)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels, title='GHG (g CO2/MJ)',loc='upper left',fontsize=8,framealpha=1)

plt.savefig('fig8.tiff',dpi=300)
plt.show()


# parallel axis plot of decision variable values
    
columns = list(B.columns)
min_price = min(B['Price'])
max_price = max(B['Price'])

for j in columns:
    B[j] = B[j]/max(df_O[j])
B['E'] = B['Price']
B = B.sort_values(by='Price')
    
from pandas.plotting import parallel_coordinates

fig = plt.figure()

labels = ["Price","GHG","Land","N","Soybean HEPA","Corn AF","Forestry Biomass FT","Grasses FT","Marine Microalgae HTL"]
ax = parallel_coordinates(B,'E',cols=labels,colormap = 'coolwarm')
ax.legend().remove()

plt.savefig('fig9.tiff',dpi=300)
plt.show()

import matplotlib as mpl

fig, ax = plt.subplots(figsize=(6, 1))

cmap = mpl.cm.coolwarm
norm = mpl.colors.Normalize(vmin=min_price, vmax=max_price)

cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='horizontal')
cb1.set_label('Price ($/gge)')
# fig.show()
# plt.savefig('colorbar.tiff',dpi=300)


# scenario #2 - Cost <$8/gge and post-combustion GHG <70 g/MJ and Land < 90m2/GJ
A = df_O[df_O['Price']<8]
B = A[A['GHG']<70]
C = B[B['Land']<90]
D = pd.concat([df_O,C]).drop_duplicates(keep=False)

# 3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(D['Price'], D['GHG'], D['Land'], c=D['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=D['GHG'],alpha=0.2)
b = ax.scatter(C['Price'], C['GHG'], C['Land'], c=C['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=C['GHG'],alpha=1)
ax.view_init(35, 130)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('GHG (g CO2/MJ)')
ax.set_zlabel('Land (m2/GJ)')

cbar = plt.colorbar(b, fraction=0.05, pad=0.1, shrink=0.5)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels, title='GHG (g CO2/MJ)',loc='upper left',fontsize=8,framealpha=1)

plt.savefig('fig10.tiff',dpi=300)
plt.show()


# parallel axis plot of decision variable values

columns = list(C.columns)
min_price = min(C['Price'])
max_price = max(C['Price'])

for j in columns:
    C[j] = C[j]/max(df_O[j])
C['E'] = C['Price']
C = C.sort_values(by='Price')
    
from pandas.plotting import parallel_coordinates

fig = plt.figure()

labels = ["Price","GHG","Land","N","Soybean HEPA","Corn AF","Forestry Biomass FT","Grasses FT","Marine Microalgae HTL"]
ax = parallel_coordinates(C,'E',cols=labels,colormap = 'coolwarm')
ax.legend().remove()

plt.savefig('fig11.tiff',dpi=300)
plt.show()

# scenario #3 - Cost <$8/gge and post-combustion GHG <70 g/MJ and Land < 90m2/GJ and N < 700 g/MJ

A = df_O[df_O['Price']<8]
B = A[A['GHG']<70]
C = B[B['Land']<90]
D = C[C['N']<700]
E = pd.concat([df_O,D]).drop_duplicates(keep=False)

# 3D plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
p = ax.scatter(E['Price'], E['GHG'], E['Land'], c=E['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=E['GHG'],alpha=0.2)
b = ax.scatter(D['Price'], D['GHG'], D['Land'], c=D['Price'], cmap=cm.PiYG, vmin = _min, vmax = _max, edgecolor = 'black', linewidth = 0.2,s=D['GHG'],alpha=1)
ax.view_init(35, 130)
ax.set_xlabel('Price ($/gge)')
ax.set_ylabel('GHG (g CO2/MJ)')
ax.set_zlabel('Land (m2/GJ)')

cbar = plt.colorbar(b, fraction=0.05, pad=0.1, shrink=0.5)
cbar.set_label('Price ($/gge)',rotation=270,labelpad=12)
cbar.ax.tick_params(labelsize=8) 

# produce a legend with a cross section of sizes from the scatter
handles, labels = p.legend_elements(prop="sizes", alpha=1)
legend2 = ax.legend(handles, labels, title='GHG (g CO2/MJ)',loc='upper left',fontsize=8,framealpha=1)

plt.savefig('fig12.tiff',dpi=300)
plt.show()


# parallel axis plot of decision variable values

columns = list(D.columns)
min_price = min(D['Price'])
max_price = max(D['Price'])

for j in columns:
    D[j] = D[j]/max(df_O[j])
D['E'] = D['Price']
D = D.sort_values(by='Price')
    
from pandas.plotting import parallel_coordinates

fig = plt.figure()

labels = ["Price","GHG","Land","N","Soybean HEPA","Corn AF","Forestry Biomass FT","Grasses FT","Marine Microalgae HTL"]
ax = parallel_coordinates(D,'E',cols=labels,colormap = 'coolwarm')
ax.legend().remove()

plt.savefig('fig13.tiff',dpi=300)
plt.show()


