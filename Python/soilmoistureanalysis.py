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

soilmoisture = pd.read_csv('data_cleaned/Three-D_soil-moisture_2021.csv')
metaturfID = pd.read_csv('Three-D_metaturfID.csv')

#for i in range(len(soilmoisture)):

for i in range(len(soilmoisture)): # Looping over each data point
    current_point = soilmoisture.iloc[i,:] # Label the current data point being inspected
    for j in range(len(metaturfID)):     # Looping over the possible turfIDs
        if current_point["turfID"] == metaturfID.iloc[i,9]:  # if the FluxID of the current data point is equal to some j and tea type green, add it to the j list
            soilmoisture[j].append(current_point)
     #   elif current_point["turfID"] == id_list[j] and current_point["tea_type"]=='red': # same but for red
       #     new_reddata[j].append(current_point)