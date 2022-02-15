#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 21:41:01 2022

@author: emmalittle

"""
# Importing modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% Read csv 

soilmoisture = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/data_cleaned/Three-D_soil-moisture_2021.csv')
metaturfID = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/Three-D_metaturfID.csv')
climatedata = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/data/THREE_D_Gridded_MonthlyClimate_2009-2019.csv')

#for i in range(len(soilmoisture)):
soilmoisture.insert(6, "Site",0)
soilmoisture.insert(7, "Treatment",0)

for i in range(len(soilmoisture)): # Looping over each data point
    current_point = soilmoisture.iloc[i,:] # Label the current data point being inspected
    for j in range(len(metaturfID)):     # Looping over the possible turfIDs
        if soilmoisture.iloc[i,0] == metaturfID.iloc[j,-1]:  # if the FluxID of the current data point is equal to some j and tea type green, add it to the j list
            soilmoisture.iloc[i,6] = metaturfID.iloc[j,6]
            soilmoisture.iloc[i,7] = metaturfID.iloc[j,2]
          
#%%  Location climates: helpful for report, not relevant for soil moisture analysis

Vikclim = np.zeros((len(climatedata),2))
Joaclim = np.zeros((len(climatedata),2))
Liaclim = np.zeros((len(climatedata),2))

for i in range (len(climatedata)):
    if climatedata.iloc[i,5] == 'temperature' :
        if climatedata.iloc[i,0]=='Vik':
            Vikclim[i,0] = climatedata.iloc[i,6]
        elif climatedata.iloc[i,0]=='Joa':
            Joaclim[i,0] = climatedata.iloc[i,6]
        elif climatedata.iloc[i,0]=='Lia':
            Liaclim[i,0] = climatedata.iloc[i,6]      
    if climatedata.iloc[i,5] == 'precipitation' :
        if climatedata.iloc[i,0]=='Vik':
            Vikclim[i,1] = climatedata.iloc[i,6]
        elif climatedata.iloc[i,0]=='Joa':
            Joaclim[i,1] = climatedata.iloc[i,6]
        elif climatedata.iloc[i,0]=='Lia':
            Liaclim[i,1] = climatedata.iloc[i,6]            
#Viktemp = np.delete(Viktemp, np.argwhere(Viktemp ==0),0) # removing empty entries
#Joatemp = np.delete(Joatemp, np.argwhere(Joatemp ==0),0) # removing empty entries
#Liatemp = np.delete(Liatemp, np.argwhere(Liatemp ==0),0) # removing empty entries
Vikclim[Vikclim == 0] = np.nan
Joaclim[Joaclim == 0] = np.nan
Liaclim[Liaclim == 0] = np.nan

Vikavg = np.nanmean(Vikclim, axis=0)
#Vikstd = np.nanstd(Vikclim, axis = 0)
Vikavg[1] = 365.24*Vikavg[1]
#Vikstd[1] = 365.24*Vikstd[1]

Joaavg = np.nanmean(Joaclim, axis=0) 
#Joastd = np.nanstd(Joaclim, axis = 0)
Joaavg[1] = 365.24*Joaavg[1]
#Joastd[1] = 365.24*Joastd[1]

Liaavg = np.nanmean(Liaclim, axis=0)
#Liastd = np.nanstd(Liaclim, axis = 0)
Liaavg[1] = 365.24*Liaavg[1]
#Liastd[1] = 365.24*Liastd[1]

#%% Soil Moisture Statistics
        
nr = [1,2,3,4]
campaigns=np.zeros((4,3))
Lia_m = np.zeros((4,(len(soilmoisture))))
Joa_m = np.zeros((4,(len(soilmoisture))))
Vik_m = np.zeros((4,(len(soilmoisture))))
stdL = np.zeros(4)
stdJ = np.zeros(4)
stdV = np.zeros(4)

# Calculating averages and standard deviations for error bars

def site_avg(c, soilmoisture):
    sum_moisture_Lia=0
    L=0
    Lia = np.zeros((len(soilmoisture)))
    sum_moisture_Joa=0
    J=0
    Joa = np.zeros((len(soilmoisture)))
    sum_moisture_Vik=0
    V=0
    Vik = np.zeros((len(soilmoisture)))
    for i in range(len(soilmoisture)):
        if soilmoisture.iloc[i,6]=='Lia' and int(soilmoisture.iloc[i,4])==c:
            sum_moisture_Lia=soilmoisture.iloc[i,2]+sum_moisture_Lia
            Lia[i] = soilmoisture.iloc[i,2]
            L=L+1
        elif soilmoisture.iloc[i,6]=='Joa' and str(soilmoisture.iloc[i,5]) == "nan" and soilmoisture.iloc[i,4]==c:
            sum_moisture_Joa=soilmoisture.iloc[i,2]+sum_moisture_Joa
            J=J+1
            Joa[i]=soilmoisture.iloc[i,2]
        elif soilmoisture.iloc[i,6]=='Vik' and soilmoisture.iloc[i,4]==c:
            sum_moisture_Vik=soilmoisture.iloc[i,2]+sum_moisture_Vik
            V=V+1
            Vik[i]=soilmoisture.iloc[i,2]
    avg_moisture = [(sum_moisture_Lia/L),(sum_moisture_Joa/J),(sum_moisture_Vik/V)]
    Vik_moist=Vik
    Joa_moist=Joa
    Lia_moist=Lia

    return avg_moisture, Lia_moist, Joa_moist, Vik_moist

for i in range(1,len(campaigns)+1):
    campaigns[i-1,:] = site_avg(i,soilmoisture)[0]
    Lia_m[i-1,:] = site_avg(i,soilmoisture)[1]
    stdL[i-1]=np.nanstd(np.where(np.isclose(Lia_m[i-1,:],0), np.nan, Lia_m[i-1,:]))
    Joa_m[i-1,:] = site_avg(i,soilmoisture)[2]
    stdJ[i-1]=np.nanstd(np.where(np.isclose(Joa_m[i-1,:],0), np.nan, Joa_m[i-1,:]))
    Vik_m[i-1,:] = site_avg(i,soilmoisture)[3]
    stdV[i-1]=np.nanstd(np.where(np.isclose(Vik_m[i-1,:],0), np.nan, Vik_m[i-1,:]))
    
#%% Plotting

fig1 = plt.figure('Moisture', figsize = (5,4))
plt.scatter(nr, campaigns[:,0],c='red') # LIa
plt.scatter(nr, campaigns[:,1],c='blue') # Joa
plt.scatter(nr, campaigns[:,2],c='green') #Vik
plt.ylabel('Average Soil Moisture (%)')
plt.xlabel('Campaign') 
plt.savefig('Soilmoisture_campaign_rgb.png')
            
