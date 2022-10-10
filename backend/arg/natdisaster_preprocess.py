from math import isnan
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Earthquake Preprocess

#data = pd.read_csv("all_hour.csv")

print(data.columns)

date = data['time'].tolist()

lat = data['latitude'].tolist()
long = data['longitude'].tolist()
mag = data['mag'].tolist()


earthquake = {}

for i in range(len(date)):
    if (isnan(lat[i]) == False) and (isnan(long[i]) == False) and (isnan(mag[i]) == False):
        earthquake[date[i]] = [lat, long, mag]