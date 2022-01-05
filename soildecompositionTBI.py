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
Rfielddata = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv')
#TBIdata=decompositiondata[["origPlotID", "destPlotID", "turfID","tea_type","weight_loss_g"]]

greendata = np.ndarray((len(decompositiondata),22)) # New data array that has the number of entries = number of FluxIDs
reddata = np.ndarray((len(decompositiondata),22))
id_list = ['125 WN7C 183','126 AN7C 126','147 WN9C 194','149 AN9C 149','3 WN1C 85','4 AN1C 4','40 WN10N 119','41 WN7C 122',
           '43 AN7C 43','69 WN9C 150','7 AN1N 7','70 AN9C 70','81 AN1C 81','85 WN1C 162','87 WN1N 164','88 AN1N 88'] #determined easily by set(Rfielddata['turfID']), the ones for soil respiration

new_greendata = np.zeros((len(id_list)), dtype = list)
new_reddata = np.zeros((len(id_list)), dtype = list)

for i in range(len(id_list)):
    new_greendata[i] = []
    new_reddata[i] = []
for i in range(len(decompositiondata)): # Looping over each data point
    current_point = decompositiondata.iloc[i,:] # Label the current data point being inspected

    for k in range(len(id_list)):     # Looping over the possible FluxIDs
        if current_point["turfID"] == id_list[k] and current_point["tea_type"]=='green':  # if the FluxID of the current data point is equal to some k, add it to the k list
            new_greendata[k].append(current_point)
        elif current_point["turfID"] == id_list[k] and current_point["tea_type"]=='red':
            new_reddata[k].append(current_point)
            
            
#new[np.where(new=='')] = 'NaN'
# fill empty entries with Nan!!!

# Restructure the list of arrays into a bigger array
for i in range(len(new_reddata)):
    new_reddata[i] = np.array(new_reddata[i])
    new_greendata[i] = np.array(new_greendata[i])

#%% Green Tea - S
# a is labile, 1-a is recalcitrant. Fast decomposing so we get recalc from this
a_g = np.zeros(len(new_greendata))
S = np.zeros(len(new_greendata))
# Weight at time t = ae^(-kt)+(1-a)
H_g = 0.9*np.ones(len(new_greendata) # placeholder, hydrolyzeable fraction green tea

for i in range(len(new_greendata)):
    a_g[i] = new_greendata[i][0][15]/new_greendata[i][0][18] # mass loss/predecomposition mass

S = np.ones(len(new_greendata))-(a_g/H_g)

# S = 1-a_g/H_g where ag is actual decompposed fraction of green tea and Hg is chemically possible decomposable fraction of green tea

# S = 1 - actual_decomp_green/hydrolyz_green

#%% Rooibos Tea - k
# can only get k early on and can only get a late in decomposition

# a_r = H_r(1-S)