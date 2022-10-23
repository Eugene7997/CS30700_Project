#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
import arrow


# Humidity

# In[2]:


response_API = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid=37cde85ed34605798aa360d4c26dc586')


# In[11]:


res = response_API.text
parse_json = json.loads(res)


# In[12]:


parse_json


# In[13]:


parse_json['coord']


# In[14]:


parse_json['main']['humidity']


# Rising sea levels

# In[38]:


start = arrow.now()
end = arrow.now()

response = requests.get(
  'https://api.stormglass.io/v2/tide/sea-level/point',
  params={
    'lat': 44.34,
    'lng': 10.99,
    'start': start.to('UTC').timestamp(),  # Convert to UTC timestamp
    'end': end.to('UTC').timestamp(),  # Convert to UTC timestam
  },
  headers={
    'Authorization': '2a05815c-5266-11ed-a654-0242ac130002-2a0581f2-5266-11ed-a654-0242ac130002'
  }
)

# Do something with response data.
json_data = response.json()


# In[39]:


json_data


# In[52]:


response = requests.get('https://www.worldtides.info/api/v3?heights&date=2022-10-23&lat=44.34&lon=10.99&key=2ff4df9a-2263-4c2c-a8b8-e8c11d46331f')


# In[53]:


json_data = response.json()
json_data


# In[50]:


json_data['requestLat']


# Greenhouse gas emissions

# In[64]:


response = requests.get('https://api.v2.emissions-api.org'
        + '/api/v2/carbonmonoxide/average.json'
        + '?country=DE&begin=2022-10-20&end=2022-10-22')


# In[65]:


response.json()


# In[11]:


response = requests.get('https://api.co2signal.com/v1/latest?lon=10.99&lat=44.34',
                       headers={
                           'auth-token': 'S3Hlk9xkYNaGmqYn8G1JoIH0QPiJsn55'
                       })


# In[12]:


response.json()


# In[13]:


response = requests.get('https://api.ambeedata.com/latest/by-lat-lng?lat=12&lng=77',
                       headers={
                           "x-api-key": "b1637cd664e7dce01cbd651b44e311e27b269c4717eb903fe290388116354b69",
                       })


# In[14]:


response.json()


# In[15]:


API = '37cde85ed34605798aa360d4c26dc586'
response = requests.get('http://api.openweathermap.org/data/2.5/air_pollution?lat=44.34&lon=10.99&appid=37cde85ed34605798aa360d4c26dc586')


# In[22]:


res = response.text
parse_json = json.loads(res)


# In[44]:


parse_json['list'][0]['components']['o3'] # ozone


# In[45]:


parse_json['list'][0]['components']['no2']


# In[ ]:




