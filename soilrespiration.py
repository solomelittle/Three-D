#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 19:12:51 2021

@author: emmalittle
" Additional Thesis Nov 2021-January 2022, in collaboration with THREE-D Project (University of Bergen)
  This script calculates the carbon flux from carbon dioxide concentrations over time for bare soil collars,
  comparing the results by soil temperature and moisture"
  
"""
# Importing modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import math

# %% Read csv
collar_dim  = pd.read_csv('data/c-flux/summer_2021/Three-D_soilR-chambers-size.csv') #read csv, need soil collar volume and area (already calculated in csv)
Rfielddata = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv') # Importing csv -> cut vs. keep cleaning preliminarily done in R. 
Rfielddata = pd.merge(Rfielddata, collar_dim, on="turfID")
Rfielddata = Rfielddata[Rfielddata.cut != 'cut'] # Removing "cut" entries 
data = Rfielddata[["datetime", "CO2", "temp_air", "temp_soil", "turfID", "campaign", "fluxID", "area_m2", "volume_L", "destSiteID"]] # Removing useless columns

 #%% Organizing new cleaned array by FluxID
 
# FluxIDs corresponding to type SoilR
id_list = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
         587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
         1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381]

new_data = np.zeros((len(id_list)), dtype = list) # New data array that has the number of entries = number of FluxIDs

for i in range(len(id_list)):
    new_data[i] = []
for i in range(len(data)): # Looping over each data point
    current_point = data.iloc[i,:] # Label the current data point being inspected

    for k in range(len(id_list)):     # Looping over the possible FluxIDs
        if current_point[6] == id_list[k]:  # if the FluxID of the current data point is equal to some k, add it to the k list
            new_data[k].append(current_point)

# Restructure the list of arrays into a bigger array
for i in range(len(new_data)):
    new_data[i] = np.array(new_data[i])

# Cleaning data again by plt.plot(new_data[10][:,1]), removing outliers present
new_data[60]=np.delete(new_data[60],slice(0,15),0) # First 15 seconds of FluxID 1350

# %% CO2 flux slope calculation, adjusting temperature units C -> K
# Initializing
temp_airavg = np.zeros(len(new_data)) # Avg. air temperature for each FluxID
temp_soilavg = np.zeros(len(new_data)) # Avg. soil temperature for each FluxID
slopelist=np.zeros(len(new_data)) # Slope array for each FluxID
turfIDlist=np.zeros(len(new_data),dtype = tuple) # TurfID array in suitable type, useful for plotting later
destsitelist=np.zeros((len(new_data)),dtype = tuple) # Original [:,0] and destination [:,1] SiteID
origsitelist=np.zeros((len(new_data)),dtype = tuple) # Original [:,0] and destination [:,1] SiteID
# Timestamp to elapsed seconds, temperature to Kelvin
for i in range(len(new_data)): # Converting time to elapsed seconds for slope calculation 
    dates = pd.to_datetime(new_data[i][:,0])
    tempdates = (dates[:]-dates[:].min())/np.timedelta64(1,'s')
    new_data[i][:,0] = tempdates # Time elapsed calculated in seconds for each FluxID, useful for slope
    new_data[i][:,2] = new_data[i][:,2]+273.15 # Celsius to Kelvin
    
# Slope calculation, average temp. calculations, filling TurfID list
for i in range(len(new_data)):
    slopelist[i] = np.polyfit(new_data[i][:,0].astype(float), new_data[i][:,1].astype(float),1)[0]
    temp_airavg[i] = sum(new_data[i][:,2])/len(new_data[i][:,2])
    temp_soilavg[i] = sum(new_data[i][:,3])/len(new_data[i][:,3])
    turfIDlist[i] = new_data[i][1,4]
    destsitelist[i] = new_data[i][1,-1] # Destination site
    # Original site (if it is a warming plot and is at lower elev. then move it up)
    if 'W' in str(new_data[i][:,4]) and new_data[i][1,-1] =='Vik':
        origsitelist[i] = 'Joa'
    elif 'W' in str(new_data[i][:,4]) and new_data[i][1,-1] =='Joa':
        origsitelist[i] = 'Lia'
    else: # In this case it is ambient, so dest=orig
        origsitelist[i] = destsitelist[i]
        

#%% Flux calculation

atm_p = 1 # atmospheric pressurre, assumed 1 atm
R = 0.082057 #gas constant, in L*atm*K^(-1)*mol^(-1)
tube_vol = 0.075 # tube volume in L
fluxes = np.zeros(len(new_data)) # Initializing

for i in range(len(new_data)): # Flux for each FluxID
    # Converting flux per second to per hour (*3600) and micromol to mmol (1/1000); more typical
    fluxes[i] = (3600/1000)*(slopelist[i] * atm_p *(tube_vol + new_data[i][1,-2])/(R * temp_airavg[i] * new_data[i][1,7])) # f=slope*pressure*(tube volume + above-ground-collar volume)/(R*air temp*area)
    
# Array for plotting: TurfID, fluxes, avg. soil temp and moisture
plotarray = np.vstack([turfIDlist.astype(object),fluxes.astype(float),temp_soilavg.astype(float),destsitelist.astype(object),origsitelist.astype(object)])
plotarray = np.transpose(plotarray)

#%% Statistics/outlier removal

#avgfluxes = sum(plotarray[:,1])/len(plotarray[:,1])
#avgfluxes1 = st.mean(plotarray[:,1])
# Removing "outlier" fluxes only for the calculation of the exponential fit, 10 is negative, 51 and -4 are just very large

plotarray_log=np.delete(plotarray,-4,0)
plotarray_log=np.delete(plotarray_log,51,0)
plotarray_log=np.delete(plotarray_log,10,0)

m3, b3 = np.polyfit(plotarray_log[:,2].astype(float), np.log(plotarray_log[:,1].astype(float)), 1, w=np.sqrt(plotarray_log[:,1].astype(float)))
for i in range(len(plotarray_log)):
    plotarray_log[i,1]=math.exp(m3*plotarray_log[i,2]+b3)

#%% Plotting

# Flux for each 4 points of TurfID coloured by temp. could separate into lia joa and vik
fig1 = plt.figure('Soil Temperature and Carbon Dioxide Flux by TurfID', figsize = (15,4))
plt.scatter(plotarray[:,0], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='Reds')
plt.colorbar()
plt.xticks(fontsize=6)
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Turf ID') 
plt.show()
plt.savefig('SoilRespiration_Temp-TurfID.png')

# Linear flux (black), exp (red) and soil temp
fig2=plt.figure('Flux vs. soil temperature, linear')
m, b = np.polyfit(plotarray[:,2].astype(float), plotarray[:,1].astype(float), 1)
plt.plot(plotarray[:,2], m*plotarray[:,2] + b, c = "gray")
plt.plot(plotarray_log[:,2], plotarray_log[:,1], c = "red")
plt.scatter(plotarray[:,2], plotarray[:,1], c = "black", marker = ".") # Flux vs. soil temp
plt.ylabel('CO2 Flux (mmol/m2/h) (red= exponential, black=linear)')
plt.xlabel('Soil Temperature (C)') 
plt.savefig('SoilRespiration_Trendline.png')

# # Exponential flux and soil temp, outliers removed, sca
# fig3=plt.figure('Flux vs. soil temperature, exponential with outlier removal')
# plt.plot(plotarray_log[:,2], plotarray_log[:,1], c = "red")
# plt.scatter(plotarray[:,2], plotarray[:,1], c = "black", marker = ".") # Flux vs. soil temp
# plt.ylabel('CO2 Flux (mmol/m2/h)')
# plt.xlabel('Soil Temperature (C)')

# By destination site
fig4 = plt.figure('Soil Temperature and Carbon Dioxide Flux by dest site', figsize = (5,4))
plt.scatter(plotarray[:,3], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='Blues')
plt.colorbar()
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Destination Site') 
plt.savefig('SoilRespiration_destSite.png')

# By original site
fig5 = plt.figure('Soil Temperature and Carbon Dioxide Flux by orig site', figsize = (5,4))
plt.scatter(plotarray[:,4], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='Blues')
plt.colorbar()
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Original Site')

# Moisture
