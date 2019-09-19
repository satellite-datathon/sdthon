#!/usr/bin/env python
# coding: utf-8

# In[39]:


import json as j
import pandas as pd
import glob


# In[40]:


final = pd.DataFrame()
filenames = glob.glob(r'C:\datasets\phase-01\data\sentinel-2a-tile-7680x-10240y\metadata\*.json')
for f in filenames:
    df = pd.read_json(f,orient='index')
    final = final.append(df)
    
#df = pd.read_json(r'C:\datasets\phase-01\data\sentinel-2a-tile-7680x-10240y\metadata\2016-12-22.json',orient='index')


# In[82]:


final.shape


# In[71]:


df_cc = final.loc['cloud-cover',:]


# In[84]:


df_rest = final.drop(['cloud-cover'])
#df_rest['cloudCover']


# In[ ]:




