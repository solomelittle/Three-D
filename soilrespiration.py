#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 19:12:51 2021

@author: emmalittle
"""

import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
# %%
# Importing csv -> already cleaned in R (cut vs. keep). Collar area and above ground volume calculated already.
collar_dim  = pd.read_csv('data/c-flux/summer_2021/Three-D_soilR-chambers-size.csv') #read collar dimensions
Rfielddata = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv')
Rfielddata = pd.merge(Rfielddata, collar_dim, on="turfID")
# Removing cut entries 
Rfielddata = Rfielddata[Rfielddata.cut != 'cut']
#Tair = Rfielddata.groupby(['fluxID']).mean()
groupedID = Rfielddata.groupby(['fluxID'])

 #%% Organizing Array by FluxID
#FluxIDs corresponding to type SoilR
id_list = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
         587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
         1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381]

data = Rfielddata[["datetime", "CO2", "temp_air", "turfID", "campaign", "fluxID", "campaign", "area_m2", "volume_L"]]
# create a new data array that has the number of entries = number of id numbers 
new_data = np.zeros((len(id_list)), dtype = list)

for i in range(len(id_list)):
    new_data[i] = []

# loop over each data point
for i in range(len(data)):
    # label the current data point that we are inspecting
    current_point = data.iloc[i,:]
    #print(current_point)

    # loop over the possible ID values
    for k in range(len(id_list)):

        # if the ID number of the current data point is equal to some k, add it to the k list
        if current_point[5] == id_list[k]:
            new_data[k].append(current_point)

# restructure the list of arrays into a bigger array
for i in range(len(new_data)):
    new_data[i] = np.array(new_data[i])


# %% Slope calculation

for i in range(len(new_data)):
    dates = pd.to_datetime(new_data[i][:,0])
    tempdates = (dates[:]-dates[:].min())/np.timedelta64(1,'s')
    new_data[i][:,0] = tempdates

slopelist=np.zeros(len(new_data))
# 60 NEEDS FIXING
for i in range(len(new_data)):
    
    slopelist[i] = np.polyfit(new_data[i][:,0].astype(float), new_data[i][:,1].astype(float),1)[0]

#%%

def soil_respiration(m):
    atm_pressure = 1 # atmospheric pressurre, assumed 1 atm
    R = 0.082057 #gas constant, in L*atm*K^(-1)*mol^(-1)
   # new_data[:,2] = new_data[:,2]+273.15 # converting to Kelvin for flux calc FIX THIS THIS IS POORLY INDEXED
    flux = (slope * atm_pressure *(tube_volume + volume_L)/(R * temp_airavg * area_m2)

