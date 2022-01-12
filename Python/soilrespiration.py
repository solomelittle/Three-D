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
collar_dim  = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/data/c-flux/summer_2021/Three-D_soilR-chambers-size.csv') #read csv, need soil collar volume and area (already calculated in csv)
Rfielddata = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/data/c-flux/summer_2021/Three-D_soilco2_2021.csv') # Importing csv -> cut vs. keep cleaning preliminarily done in R. 
Rfielddata = pd.merge(Rfielddata, collar_dim, on="turfID")
Rfielddata = Rfielddata[Rfielddata.cut != 'cut'] # Removing "cut" entries 

 #%% Organizing new cleaned array by FluxID
 
data = Rfielddata[["datetime", "CO2", "temp_air", "temp_soil", "turfID", "campaign", "fluxID", "area_m2", "volume_L", "destSiteID"]] # Removing useless columns
# FluxIDs corresponding to type SoilR
id_list = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
         587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
         1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381,1382]

new_data = np.zeros((len(id_list)), dtype = list) # New data array that has the number of entries = number of FluxIDs

for i in range(len(id_list)):
    new_data[i] = []
for i in range(len(data)): # Looping over each data point
    current_point = data.iloc[i,:] # Label the current data point being inspected

    for k in range(len(id_list)):     # Looping over the possible FluxIDs
        if current_point["fluxID"] == id_list[k]:  # if the FluxID of the current data point is equal to some k, add it to the k list
            new_data[k].append(current_point)

# Restructure the list of arrays into a bigger array
for i in range(len(new_data)):
    new_data[i] = np.array(new_data[i])

# Cleaning data by plt.plot(new_data[10][:,1]), removing outliers present
new_data[60]=np.delete(new_data[60],slice(0,15),0) # First 15 seconds of FluxID 1350

# %% CO2 flux slope calculation, adjusting temperature units C -> K

# Initializing
temp_airavg = np.zeros(len(new_data)) # Avg. air temperature for each FluxID
temp_soilavg = np.zeros(len(new_data)) # Avg. soil temperature for each FluxID
slopelist=np.zeros(len(new_data)) # Slope array for each FluxID
turfIDlist=np.zeros(len(new_data),dtype = tuple) # TurfID array in suitable type, useful for plotting later
campaignlist=np.zeros((len(new_data)),dtype = tuple) # 1,2,3,4: To be treated as a time series
treatmentlist=np.zeros((len(new_data)),dtype = tuple) # Ambient or Warming
sitelist=np.zeros((len(new_data)),dtype = tuple) # Destination SiteID
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
    sitelist[i] = new_data[i] [1,9]
    campaignlist[i] = new_data[i][1,5] 
    if 'W' in str(new_data[i][:,4]):
        treatmentlist[i] = 'W'
    else:
        treatmentlist[i] = 'A'
    # Original site (if it is a warming plot and is at lower elev. then move it up)
    if 'W' in str(new_data[i][:,4]) and new_data[i][1,-1] =='Vik':
        origsitelist[i] = 'Joa'
    elif 'W' in str(new_data[i][:,4]) and new_data[i][1,-1] =='Joa':
        origsitelist[i] = 'Lia'
    else: # In this case it is ambient, so dest=orig
        origsitelist[i] = sitelist[i]    
        

#%% Flux calculation

atm_p = 1 # atmospheric pressurre, assumed 1 atm
R = 0.082057 #gas constant, in L*atm*K^(-1)*mol^(-1)
tube_vol = 0.075 # tube volume in L
fluxes = np.zeros(len(new_data)) # Initializing

for i in range(len(new_data)): # Flux for each FluxID
    # Converting flux per second to per hour (*3600) and micromol to mmol (1/1000); more typical
    fluxes[i] = (3600/1000)*(slopelist[i] * atm_p *(tube_vol + new_data[i][1,-2])/(R * temp_airavg[i] * new_data[i][1,7])) # f=slope*pressure*(tube volume + above-ground-collar volume)/(R*air temp*area)
    
# Array for plotting: TurfID, fluxes, avg. soil temp, campaigns, treatments, sites and moisture
plotarray = np.vstack([turfIDlist.astype(object),fluxes.astype(float),temp_soilavg.astype(float),campaignlist.astype(object),treatmentlist.astype(object),sitelist.astype(object),origsitelist.astype(object),np.zeros(len(sitelist))])
plotarray = np.transpose(plotarray)

#%% Moisture Time Series Analysis
# Initializing
avg_soilmoisture = np.array([[81.48625,33.50474684,6.82625 ],[45.629375, 27.186875, 16.6125],[48.838125, 38.0503125 , 17.4475],[34.66375, 12.0246875,  4.795625]]) # from soilmoistureanalysis, Lia/Joa/Vik
campaigns = [1,2,3,4]
moisturesummary = np.zeros(len(plotarray))

for i in range(1,len(campaigns)+1):
    for j in range(len(plotarray)):
        if plotarray[j,3]==i and plotarray [j,5]=='Lia':
            moisturesummary[j]=avg_soilmoisture[i-1,0]
        elif plotarray[j,3]==i and plotarray [j,5]=='Joa':
            moisturesummary[j]=avg_soilmoisture[i-1,1]
        elif plotarray[j,3]==i and plotarray [j,5]=='Vik':
            moisturesummary[j]=avg_soilmoisture[i-1,2]
            
plotarray [:,7] = moisturesummary # filling the zeros with correct moisture values
            
#%% Statistics/outlier removal

# Removing "outlier" fluxes only for the calculation of the exponential fit, 10 is negative, 51 and -4 are just very large
plotarray_fit=np.delete(plotarray,(-5,51,10),0)
plotarray_log = np.ndarray((61,5))
plotarray_poly = np.zeros((61,5))
tempsoilfix = 15

m1, b1 = np.polyfit(plotarray_fit[:,2].astype(float), plotarray_fit[:,1].astype(float), 1)
m2,b2,c2 = np.polyfit(plotarray_fit[:,2].astype(float), plotarray_fit[:,1].astype(float),2)
m3, b3 = np.polyfit(plotarray_fit[:,2].astype(float), np.log(plotarray_fit[:,1].astype(float)), 1, w=np.sqrt(plotarray_fit[:,1].astype(float)))
for i in range(len(plotarray_fit)):
    plotarray_log[i,1]=math.exp(m3*plotarray_fit[i,2]+b3)
    plotarray_poly[i,1] = plotarray[i,1]+m2*(tempsoilfix**2-plotarray[i,2]**2)+b2*(tempsoilfix-plotarray[i,2]) # Check temperature correction
    
#%% Plotting

# Flux for each 4 points of TurfID coloured by temp. could separate into lia joa and vik
# fig1 = plt.figure('Soil Temperature and Carbon Dioxide Flux by TurfID', figsize = (15,4))
# plt.scatter(plotarray[:,0], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='Reds')
# plt.colorbar()
# plt.xticks(fontsize=6)
# plt.ylabel('CO2 Flux (mmol/m2/h)')
# plt.xlabel('Turf ID') 
# plt.show()
# plt.savefig('SoilRespiration_Temp-TurfID.png')

# Linear flux (black), exp (red) and soil temp
# fig2=plt.figure('Flux vs. soil temperature, linear')
# plt.plot(plotarray[:,2], m1*plotarray[:,2] + b1, c = "gray")
# plt.scatter(plotarray[:,2], plotarray[:,1], c = "black", marker = ".") # Flux vs. soil temp
# plt.ylabel('CO2 Flux (mmol/m2/h) (red= exponential, black=linear)')
# plt.xlabel('Soil Temperature (C)') 
# plt.savefig('SoilRespiration_Trendline.png')

# Exponential fit for flux and soil temp, outliers removed.  
fig3=plt.figure('Flux vs. soil temperature, exponential fit')
plt.plot(plotarray_fit[:,2], plotarray_log[:,1], c = "black")
#plt.scatter(plotarray_fit[:,2], plotarray_poly[:,1], c = "blue") # Temperature corrected
#plt.scatter(plotarray_fit[:,2], plotarray_fit[:,1], c = "black", marker = ".") # Flux vs. soil temp
for i in range(len(plotarray_fit)):
    if plotarray[i,4]=='A' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,2], plotarray[i,1], marker='o',c = "blue")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,2], plotarray[i,1], marker='o',c = "red")
    if plotarray[i,4]=='A' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,2], plotarray[i,1], marker='^',c = "blue")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,2], plotarray[i,1], marker='^',c = "red")
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Soil Temperature (C)')
plt.legend()

# By campaign
fig4 = plt.figure('Flux over summer season (by campaign)', figsize = (5,4))
plt.scatter(plotarray[:,3], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='viridis')
plt.colorbar(label='Temperature (C)')
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Campaign') 
plt.xticks(campaigns)
plt.savefig('SoilRespiration_temp_campaign.png')

# By treatment
fig5 = plt.figure('Soil Temperature and Carbon Dioxide Flux by orig site', figsize = (5,4))
plt.scatter(plotarray[:,4], plotarray[:,1], edgecolors='none',c=plotarray[:,2],cmap='viridis')
plt.colorbar(label='Temperature (C)')
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Original Site')

# Moisture
fig6 = plt.figure('Temperature-corrected flux (15 C) vs. moisture', figsize = (5,4)) 
plt.scatter(plotarray_fit[:,3], plotarray_poly[:,1], edgecolors='none',c=plotarray_fit[:,7],cmap='viridis')
plt.colorbar(label="Soil Moisture (%)")
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Campaign') 
plt.xticks(campaigns)
plt.savefig('SoilRespiration_moisture_campaign.png')

# fig6 = plt.figure('Temp. corrected flux vs. moisture', figsize = (5,4)) 
# for i in range(len(plotarray_fit)):
#     if plotarray_fit [i,5] == 'Lia':
#         plt.scatter(plotarray_fit[i,3], plotarray_poly[i,1], c='red')
#     elif plotarray_fit [i,5] == 'Joa':
#         plt.scatter(plotarray_fit[i,3], plotarray_poly[i,1], c='blue')
#     elif plotarray_fit [i,5] == 'Vik':
#         plt.scatter(plotarray_fit[i,3], plotarray_poly[i,1], c='green')
# plt.ylabel('CO2 Flux (mmol/m2/h)')
# plt.xlabel('Campaign') 
# plt.xticks([1,2,3,4])
# plt.savefig('SoilRespiration_campaign.png')

fig7 = plt.figure('Flux vs. Temperature', figsize = (5,4)) 
for i in range(len(plotarray_fit)):
    if plotarray[i,4]=='A' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,7], plotarray[i,1], marker='o',c = "blue", label ="Alpine Ambient")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,7], plotarray[i,1], marker='o',c = "red",label ="Alpine Warming")
    if plotarray[i,4]=='A' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,7], plotarray[i,1], marker='^',c = "blue",label ="High Alpine Ambient")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,7], plotarray[i,1], marker='^',c = "red",label =" High Alpine Warming")
# plt.scatter(plotarray_fit[:,7], plotarray_poly[:,1], c='red')
# plt.scatter(plotarray_fit[:,7], plotarray_fit[:,1], c = "blue") # Temperature corrected (15 C)
plt.ylabel('CO2 Flux (mmol/m2/h)')
plt.xlabel('Moisture (%)') 
#plt.legend(handles=[A,W])
plt.savefig('SoilRespiration_moisture_campaign.png')

fig8=plt.figure('Temp-corrected Lia Flux vs Moisture',figsize=(5,4))
for i in range(len(plotarray_fit)):
    if plotarray[i,4]=='A' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,7], plotarray_poly[i,1], marker='o',c = "blue")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Joa':
        plt.scatter(plotarray_fit[i,7], plotarray_poly[i,1], marker='o',c = "red")
        
fig9=plt.figure('Temp-corrected Lia Flux vs Moisture',figsize=(5,4))     
for i in range(len(plotarray_fit)):
    if plotarray[i,4]=='A' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,7], plotarray_poly[i,1], marker='^',c = "blue")
    elif plotarray[i,4]=='W' and plotarray[i,6]=='Lia':
        plt.scatter(plotarray_fit[i,7], plotarray_poly[i,1], marker='^',c = "red")

