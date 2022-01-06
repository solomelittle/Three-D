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

#%% Reading csv and initializing

decompositiondata = pd.read_csv('data_cleaned/THREE-D_clean_decomposition_fall_2021.csv') # read csv with tea bag info
Rfielddata = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv') # read csv with turfID and fluxID filtered for type SoilR
m,n=np.shape(decompositiondata) # dimensions for easy sizing later arrays

id_list = ['125 WN7C 183','126 AN7C 126','147 WN9C 194','149 AN9C 149','3 WN1C 85','4 AN1C 4','40 WN10N 119','41 WN7C 122',
           '43 AN7C 43','69 WN9C 150','7 AN1N 7','70 AN9C 70','81 AN1C 81','85 WN1C 162','87 WN1N 164','88 AN1N 88'] # Corresponding to SoilR. Determined simply by set(Rfielddata['turfID']). 

new_greendata = np.zeros((len(id_list)), dtype = list) # decomposition data only for green tea
new_reddata = np.zeros((len(id_list)), dtype = list) # decomposition data only for rooibos tea
NaN_bags = np.ones(n)*999 # marker for missing data

for i in range(len(id_list)):
    new_greendata[i] = []
    new_reddata[i] = []
for i in range(m): # Looping over each data point
    current_point = decompositiondata.iloc[i,:] # Label the current data point being inspected
    for j in range(len(id_list)):     # Looping over the possible turfIDs
        if current_point["turfID"] == id_list[j] and current_point["tea_type"]=='green':  # if the FluxID of the current data point is equal to some j and tea type green, add it to the j list
            new_greendata[j].append(current_point)
        elif current_point["turfID"] == id_list[j] and current_point["tea_type"]=='red': # same but for red
            new_reddata[j].append(current_point)
# Filling empty entries with marker for missing data          
new_reddata[1].append(NaN_bags) 
new_reddata[15].append(NaN_bags)
new_greendata[1].append(NaN_bags)
new_greendata[8].append(NaN_bags)
new_greendata[10].append(NaN_bags)            

# Restructure the list of arrays into a bigger array
for i in range(len(new_reddata)):
    new_reddata[i] = np.array(new_reddata[i]) # note: where 1 ('126 AN7C 126') and 15('88 AN1N 88') are missing
    new_greendata[i] = np.array(new_greendata[i]) # note: where 1 ('126 AN7C 126') and 8 ('43 AN7C 43')and 10 ('7 AN1N 7')are missing

#%% Green Tea - S
# a is labile, 1-a is recalcitrant. Because green tea is fast to decompose we get recalcitrant info from this.
a_g = np.zeros(len(new_greendata)) # fraction of green tea actually decomposed
S = np.zeros(len(new_greendata)) # stabilization factor (Keuskamp et al. 2013)

H_g = 0.842*np.ones(len(new_greendata)) # Hydrolyzeable (chemically decomposable) fraction of green tea (from Quantifying Litter Decomposition Rates on a Semi-Intensive Green Roof, Lasalle 2019)
              
for i in range(len(new_greendata)):
    if new_greendata[i][0][15]==999: 
        a_g[i] = 'NaN' # Marker now does not exist
    else:
        a_g[i] = new_greendata[i][0][14]/new_greendata[i][0][18] # (actual mass loss)/(pre-decomposition mass)

S = np.ones(len(new_greendata))-(a_g/H_g) # This is the equation for S = 1-a_g/H_g

#%% Rooibos Tea - k
a_r = np.zeros(len(new_reddata)) # fraction of rooibos tea actually decomposed
k =  np.zeros(len(new_reddata)) # decomposition rate [d^-1], based on rooibos tea because it decomposes slowly
H_r = 0.552*np.ones(len(new_reddata)) # placeholder, hydrolyzeable fraction rooibos tea 
a_r = H_r*(np.ones(len(new_reddata)) - S)
# Weight at time t = ae^(-kt)+(1-a)
for i in range(len(new_reddata)):
    k[i] = -np.log(a_r[i]*(new_reddata[i][0][-2]-(1-a_r[i])))/new_reddata[i][0][15]

