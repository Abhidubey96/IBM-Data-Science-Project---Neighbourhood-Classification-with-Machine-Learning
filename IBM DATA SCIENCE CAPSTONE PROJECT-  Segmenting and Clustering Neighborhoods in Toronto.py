#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto
# 
# 
# 
# ## Required to explore, segment, and cluster the neighborhoods in the city of Toronto. 
# 
# 
# 
# ## Part One - explore data 

# ### Extract Data Using Web Scraper

# In[2]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium # map rendering library

print('Libraries imported.')


# In[3]:


url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

dfs = pd.read_html(url)

len(dfs)


# ### Table extracted from website stored in dfs. Only Table 1  with index 0 we need for the analysis.

# In[5]:


df = dfs[0]


# In[23]:


df


# In[11]:


df.tail()


# In[9]:


df.shape


# ### As we can see df is not clean. So lets start the cleaning process.
# 
# ### The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood.
# 
# ### Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
# 
# ### Check Postal Code should be unique.

# In[14]:


df1 = df.drop(df[df.Borough == "Not assigned"].index)


# In[25]:


df1.shape


# In[16]:


df1


# In[19]:


df1["Postal Code"].nunique()


# In[21]:


df1["Neighbourhood"]=="Not assigned"


# In[22]:


df1.reset_index(drop=True)


# In[24]:


df1.shape


# ### Final Shape of our data ( 103 rows, 3 columns )

# # Segmenting Data

# ### we will use coordinates csv file
# 

# In[26]:


df_geo = pd.read_csv(r"C:\Users\Lucifer\Downloads\Geospatial_Coordinates.csv")

df_geo


# ### Lets merge df1 to df_geo on Postal Code as primary key

# In[28]:


df_final=pd.merge(df1, df_geo, on=['Postal Code'])


# In[29]:


df_final


# In[30]:


df_final.shape


# ### Final Data Frame will be of size ( 103, 5 )
# 
# ### Postal Code,	Borough,	Neighbourhood,	 Latitude, 	 Longitude

# # Clustering Data

# In[32]:


address = 'Toronto, Ontario, Canada'

geolocator = Nominatim(user_agent="ny_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto city are {}, {}.'.format(latitude, longitude))


# In[37]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(df_final['Latitude'], df_final['Longitude'], df_final['Borough'], df_final['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto


# ## Final Output Map of Toronto with clustered neighbourhood

# ### @Abhishek Dubey

# In[ ]:




