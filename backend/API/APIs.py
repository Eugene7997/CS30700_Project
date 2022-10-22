#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json


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

# In[ ]:





# In[ ]:





# In[ ]:





# Greenhouse gas emissions

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




