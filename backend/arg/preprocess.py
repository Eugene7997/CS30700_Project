from math import isnan
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Preprocessing Weather API Data

# Preprocessing Temperature CSV Data
#%%
#data = pd.read_csv("tempcsvfile")

date = data['DATE'].tolist()

dates = {}

max = data['TMAX'].tolist()
min = data['TMIN'].tolist()

for i in range(len(max)):
    if (isnan(max[i]) == False) and (isnan(min[i]) == False):
        if date[i] not in dates.keys():
            dates[date[i]] = [max[i], min[i]]
        else:
            nmax = (dates[date[i]][0] + max[i]) / 2
            nmin = (dates[date[i]][1] + min[i]) / 2
            dates[date[i]] = [nmax, nmin]

# Preprocessing Precipitation CSV Data
#%%

precip_dates = {}

precip = data['PRCP'].tolist()

precip_new = []

for i in precip:
    if (isnan(i)):
        precip_new.append(0.0)
    else:
        precip_new.append(i)

for i in range(len(date)):
    if (isnan(precip_new[i]) == False):
        if date[i] not in precip_dates.keys():
            precip_dates[date[i]] = [precip_new[i]]
        else:
            nprecip = (precip_dates[date[i]][0] + precip_new[i]) / 2
            precip_dates[date[i]] = [nprecip]