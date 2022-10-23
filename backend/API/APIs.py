#!/usr/bin/env python
# coding: utf-8

# In[15]:


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


# In[42]:


response = requests.get('https://www.worldtides.info/api/v3?heights&date=2022-10-23&lat=44.34&lon=10.99&key=2ff4df9a-2263-4c2c-a8b8-e8c11d46331f')


# In[51]:


json_data = response.json()
json_data


# In[50]:


json_data['requestLat']


# Greenhouse gas emissions

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




