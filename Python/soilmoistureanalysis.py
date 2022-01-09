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
import scipy.stats as st
import math

soilmoisture = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/data_cleaned/Three-D_soil-moisture_2021.csv')
metaturfID = pd.read_csv('/Users/emmalittle/Documents/GitHub/Three-D/Three-D_metaturfID.csv')

#for i in range(len(soilmoisture)):
soilmoisture.insert(6, "Site",0)
soilmoisture.insert(7, "Treatment",0)

for i in range(len(soilmoisture)): # Looping over each data point
    current_point = soilmoisture.iloc[i,:] # Label the current data point being inspected
    for j in range(len(metaturfID)):     # Looping over the possible turfIDs
        if soilmoisture.iloc[i,0] == metaturfID.iloc[j,-1]:  # if the FluxID of the current data point is equal to some j and tea type green, add it to the j list
            soilmoisture.iloc[i,6] = metaturfID.iloc[j,6]
            soilmoisture.iloc[i,7] = metaturfID.iloc[j,2]
          
            
#%%
        

campaigns=np.zeros((4,3))
# need to do per campaign average, not total
def site_avg(c, soilmoisture):
    sum_moisture_Lia=0
    L=0
    sum_moisture_Joa=0
    J=0
    sum_moisture_Vik=0
    V=0
    for i in range(len(soilmoisture)):
        if soilmoisture.iloc[i,6]=='Lia' and int(soilmoisture.iloc[i,4])==c:
            sum_moisture_Lia=soilmoisture.iloc[i,2]+sum_moisture_Lia
            L=L+1
        elif soilmoisture.iloc[i,6]=='Joa' and str(soilmoisture.iloc[i,5]) == "nan" and soilmoisture.iloc[i,4]==c:
            sum_moisture_Joa=soilmoisture.iloc[i,2]+sum_moisture_Joa
            J=J+1
        elif soilmoisture.iloc[i,6]=='Vik' and soilmoisture.iloc[i,4]==c:
            sum_moisture_Vik=soilmoisture.iloc[i,2]+sum_moisture_Vik
            V=V+1
    avg_moisture = [(sum_moisture_Lia/L),(sum_moisture_Joa/J),(sum_moisture_Vik/V)]
    return avg_moisture

for i in range(1,len(campaigns)+1):
    campaigns[i-1,:] = site_avg(i,soilmoisture)
#avg_moisture_Joa=sum_moisture_Joa/J
#avg_moisture_Vik=sum_moisture_Vik/V

fig1 = plt.figure('Moisture', figsize = (5,4))
plt.scatter([1,2,3,4], campaigns[:,0],c='red') # LIa
plt.scatter([1,2,3,4], campaigns[:,1],c='blue') # Joa
plt.scatter([1,2,3,4], campaigns[:,2],c='green') #Vik
plt.ylabel('Average Soil Moisture (%)')
plt.xlabel('Campaign') 
#plt.xticks([1,2,3,4])
plt.savefig('Soilmoisture_campaign.png')
            
