# Prediction Model Code

import requests
import pandas as pd
import json
import numpy as np
import os

import sklearn 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

# Temperature

weather_y = df.pop('TAVG')
weather_x = df


tr_x, te_x, tr_y,te_y = train_test_split(weather_x, weather_y, test_size=0.2, random_state=4)

model = LinearRegression()
model.fit(tr_x, tr_y)

prediction = model.predict(te_x)

print(prediction)
print(np.mean(prediction-te_y)**2)

pd.DataFrame({"actual":te_y, "prediction":prediction, "diff":(te_y-prediction)})


# Percipitation

url = "https://meteostat.p.rapidapi.com/point/daily"

querystring = {"lat":"40.4237","lon":"-86.9212","start":"2021-10-01","end":"2022-10-22","alt":"184"}

headers = {
	"X-RapidAPI-Key": "a55f8d2207msh7820f88d8aa6766p179d54jsn08e649f0be3c",
	"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

df = json.loads(response.text)

df=df[['tmax', 'tmin', 'prcp', 'wdir', 'tavg', 'wspd', 'pres']]

df['tmax'] = df['tmax'].fillna(0)
df['tmin'] = df['tmin'].fillna(0)
df['wdir'] = df['wdir'].fillna(0)
df['tavg'] = df['tavg'].fillna(0)
df['wspd'] = df['wspd'].fillna(0)
df['pres'] = df['pres'].fillna(0)

weather_y = df.pop('prcp')
weather_x = df


tr_x, te_x, tr_y,te_y = train_test_split(weather_x, weather_y, test_size=0.4, random_state=6)

model = LinearRegression()
model.fit(tr_x, tr_y)

prediction = model.predict(te_x)

print(np.mean(prediction-te_y)**2)

pd.DataFrame({"actual":te_y, "prediction":prediction, "diff":(te_y-prediction)})

# Earthquake

# Tsunami