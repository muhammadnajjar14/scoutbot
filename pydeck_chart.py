#!/usr/bin/env python
# coding: utf-8

# In[11]:


import streamlit as st
import pandas as pd
import subprocess
import sys
import numpy as np
import requests
import time
import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import pydeck as pdk


# In[20]:


df = pd.read_csv('https://raw.githubusercontent.com/jokecamp/FootballData/master/other/stadiums-with-GPS-coordinates.csv')
df1=pd.DataFrame()
df1.insert(loc=0, column='lon', value=df['Longitude'])
df1.insert(loc=1, column='lat', value=df['Latitude'])
t=df['Team'].tolist()
#display(df)
x='chelsea'
a=[]
b=[]
c=[]
row=[]
a=x.split(" ")
for j in a:
    j=j.capitalize()
    b.append(j)
    c.append(' '.join([str(elem) for elem in b]))
    break
if c[0].lower()==x:

    for i in t:
        row = df.loc[df["Team"] == c[0]+' ']

pos=(row.iloc[: , -3:-1])
lat=str(pos['Latitude'].tolist()[0]).split(" ")
lon=str(pos['Longitude'].tolist()[0]).split(" ")
#display(lat[0])
#display(lon[0])
time.sleep(5)
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=lat,
         longitude=lon,
         zoom=5,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df1,
            get_position="[lat[0],lon[0]]",
            radius=200,
            elevation_scale=4,
            elevation_range=['0, 1000'],
            pickable=True,
            extruded=True,
         ),
        pdk.Layer(
         'ScatterplotLayer',
         data=df1,
         get_position="[lat[0],lon[0]]",
         get_color='[200, 30, 0, 160]',
         get_radius=200,
     ),
 ],
))
#display(pos)


# In[ ]:




