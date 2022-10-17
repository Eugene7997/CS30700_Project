# Prediction Model Code

import pandas as pd
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

# Earthquake

# Tsunami