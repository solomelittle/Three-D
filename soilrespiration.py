#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 19:12:51 2021

@author: emmalittle
"""

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from scipy.stats import linregress
# %%
# Importing csv -> already cleaned in R (cut vs. keep). Collar area and above ground volume calculated already.
collar_dim  = pd.read_csv('data/c-flux/summer_2021/Three-D_soilR-chambers-size.csv') #read collar dimensions
Rfielddata = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv')
# Removing cut entries 
Rfielddata = Rfielddata[Rfielddata.cut != 'cut']
#Rfielddata = Rfielddata.groupby("fluxID")

#Then, we need to change the date to integer
Rfielddata['datetime'] = pd.to_datetime(Rfielddata['datetime'])  
Rfielddata['time_delta'] = (Rfielddata['datetime'] - Rfielddata['datetime'].min())/ np.timedelta64(1,'s')

# time = datetime
# s1 = '10:33:26'
# s2 = '11:15:49' # for example
# FMT = '%H:%M:%S'
# tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
#meteo_data['num_date'] = meteo_data['datetime'].astype(np.int64)/(1e9*3600*24)
#meteo_data.set_index('datetime',inplace=True)


#df['duration'] = df.groupby('user_id')['interval'].transform('sum')
# def soil_respiration:
#     atm_pressure = 1 # atmospheric pressurre, assumed 1 atm
#     R = 0.082057 #gas constant, in L*atm*K^(-1)*mol^(-1)
#     Rfielddata.iloc[:,4] = Rfielddata.iloc[:,4]+273.15 # converting to Kelvin for flux calc
#     slope = linregress(Rfluxdata.iloc[:,1],Rfielddata.iloc[:,2])
#     flux = (slope * atm_pressure *(tube_volume + volume_L)/(R * temp_airavg * area_m2)