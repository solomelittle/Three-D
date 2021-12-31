import numpy as np
import pandas as pd

# suppose your data are arranged in an array called data with columns [time, conc, id]
data = pd.read_csv('data/c-flux/summer_2021/Three-D_soilco2_2021.csv')

# create list of ID numbers
id_list = [27,42,47,72,112,121,158,176,201,210,231,256,292,305,308,339,363,385,419,439,466,477,548,561,580,
         587,632,635,666,669,693,702,739,756,793,796,827,830,874,897,908,923,962,985,1007,1012,1031,1053,
         1159,1162,1193,1196,1246,1274,1277,1294,1312,1317,1332,1333,1350,1374,1381]

# create a new data array that has the number of entries = number of id numbers
new_data = np.zeros((len(id_list)), dtype = list)

print(new_data)

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

print(new_data)

# now, if we just want to look at one id number, we look at
#for i in range(len(id_list)):
   # print('\nthese data are related to the id number',id_list[i],':',new_data[i])

# if I want to isolate the data with id number 100 or 200 and look at the concentrations then
conc100s = new_data[0][:,4]
conc200s = new_data[1][:,4]
print(conc100s)
print(conc200s)
