# Prediction Model Code

#Steps
import requests
import pandas as pd
import json
import numpy as np
from matplotlib import pyplot
from prophet import Prophet
import datetime

"""
Pass in Array of dates and corresponding attribute values

(Order Date Array so that the latest date is last) 
"""

def predict_future_data(date, attribute_data):
    data_dict = {'ds': date, 'y': attribute_data}
    df = pd.DataFrame(data_dict)

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=12, freq="h")
    forecast = m.predict(future)
    f = forecast.tail(12)
    f_ret = f[['ds', 'yhat']]
    
    Date_ret = []
    pred_ret = []

    for i in f_ret['ds']:
        Date_ret.append(str(i))

    for j in f_ret['yhat']:
        pred_ret.append(j)

    return Date_ret, pred_ret

#Returns list of both Date and Predicted Values Arrays