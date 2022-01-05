#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 03:24:59 2022

@author: emmalittle

" Additional Thesis Nov 2021-January 2022, in collaboration with THREE-D Project (University of Bergen)
  This script calculates the stabilization factor S and decomposition constant k from field data according
  to standard protocol for the Teabag Index (TBI) by Keuskamp et al."
  
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import math

#%%

decompositiondata = pd.read_csv('data_cleaned/THREE-D_clean_decomposition_fall_2021.csv') #read csv
TBIdata=decompositiondata[["origPlotID", "destPlotID", "turfID","tea_type","weight_loss_g"]]

 # Organizing new cleaned array by TurfID
 
# FluxIDs corresponding to type SoilR
id_list = 
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

#%% Green Tea - S
# a is labile, 1-a is recalcitrant. Fast decomposing so we get recalc from this
# Weight at time t = ae^(-kt)+(1-a)
# S = 1-a_g/H_g where ag is actual decompposed fraction of green tea and Hg is chemically possible decomposable fraction of green tea



#%% Rooibos Tea - k
# can only get k early on and can only get a late in decomposition

# a_r = H_r(1-S)