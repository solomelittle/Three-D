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
Rfielddata['datetime'] = pd.to_datetime(Rfielddata['datetime'])  
groupedID = Rfielddata.groupby(['fluxID'])#.apply(['datetime']-['datetime'].min())

#groupedID['time_delta'] = (groupedID['datetime'] - groupedID['datetime'].min())/ np.timedelta64(1,'s')


 #%% Organizing Array by FluxID
 
id_list = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
         587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
         1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381]

data = Rfielddata
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
        if current_point[16] == id_list[k]:

            new_data[k].append(current_point)

# restructure the list of arrays into a bigger array
for i in range(len(new_data)):
    new_data[i] = np.array(new_data[i])
    new_data[i][:,1] = pd.to_datetime(new_data[i][:,1])
# if I want to isolate the data with id number 100 or 200 and look at the concentrations then
time_delta = np.array(len(id_list))

for i in range(len(id_list)):
  time_delta[i,:]  = (new_data[i][:,1] - new_data[i][:,1].min())/ np.timedelta64(1,'s')
  
conc100s = new_data[0][:,1:2]
conc200s = new_data[1][:,1:2]
print(conc100s)
print(conc200s)



# %%

# IDlist = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
#          587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
#          1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381]
# N = len(IDlist)
# for i in len(Rfielddata):
#     for k in len(IDlist):
#         if Rfielddata['fluxID'][i] == IDlist[k]:
#             Rfielddata['datetime','CO2','fluxID'][i]
        
#df_new = Tair.groupby.get_group['47']R
#def date_delta(Rfielddata)
# for Rfielddata['fluxID'] == 47:
#     Rfielddata['time_delta'] = (Rfielddata['datetime'] - Rfielddata['datetime'].min())/ np.timedelta64(1,'s')
       # return Rfielddata
#Rfielddata.groupby('fluxID').pipe(lambda grp: grp.datetime / grp.size().sum())
#Then, we need to change the date to integer
#%%
slopes = np.ones(64) # placeholder for when I figure out the time_delta for each fluxID

#df['duration'] = df.groupby('user_id')['interval'].transform('sum')
 # def soil_respiration(m):
 #     atm_pressure = 1 # atmospheric pressurre, assumed 1 atm
 #     R = 0.082057 #gas constant, in L*atm*K^(-1)*mol^(-1)
 #     Rfielddata.iloc[:,4] = Rfielddata.iloc[:,4]+273.15 # converting to Kelvin for flux calc
 #     slope = ones(10)
 #     for i in range(10)
 #     slope(i) = linregress(Rfielddata.iloc[:,1,],Rfielddata.iloc[:,2])[1]
 #     flux = (slope * atm_pressure *(tube_volume + volume_L)/(R * temp_airavg * area_m2)


# def model(Rfielddata, delta):
#     y = Rfielddata[['CO2']].values
#     X = Rfielddata[['date_delta']].values
#     return np.squeeze(LinearRegression().fit(X, y).predict(delta))

# def group_predictions(df, date):
#     date = pd.to_datetime(date)
#     df.date = pd.to_datetime(df.date)

#     day = np.timedelta64(1, 's')
#     mn = df.date.min()
#     df['date_delta'] = df.date.sub(mn).div(day)

#     dd = (date - mn) / day

#     return df.groupby('group').apply(model, delta=dd)