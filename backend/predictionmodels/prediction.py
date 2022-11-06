# Prediction Model Code

#Steps
import requests
import pandas as pd
import json
import numpy as np
from matplotlib import pyplot
from prophet import Prophet


# Temperature
df_t = pd.read_csv("historical temp csv")
df_t=df_t[['date column', 'temperature column']]
df_t.fillna(0)


df_t.columns = ['ds', 'y'] # Must rename two columns to 'ds' and 'y', where 'ds' is the date and 'y' is the attribute to predict

m_temp = Prophet()
m_temp.fit(df_t)  # df_t is a pandas.DataFrame with 'y' and 'ds' columns
future_temp = m_temp.make_future_dataframe(periods=30)
forecast_temp = m_temp.predict(future_temp)

f_temp = forecast_temp.tail(30)
f_temp = f_temp[['ds', 'yhat']]
f_temp.columns = ['date', 'Predicted Temperature']

# Precipitation
df_p = pd.read_csv("historical precipitation csv")
df_p=df_p[['date column', 'preciptation data column']]
df_p.fillna(0)


df_p.columns = ['ds', 'y']

m_precip = Prophet()
m_precip .fit(df_p)  # df_p is a pandas.DataFrame with 'y' and 'ds' columns
future_precip  = m_precip .make_future_dataframe(periods=30)
forecast_precip  = m_precip .predict(future_precip)

f_precip  = forecast_precip .tail(30)
f_precip  = f_precip [['ds', 'yhat']]
f_precip.columns = ['date', 'Predicted Precipitation']
