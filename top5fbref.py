#!/usr/bin/env python
# coding: utf-8

# In[16]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import Edge, EdgeOptions
import time
import re


# In[17]:


url = 'https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats'
global data
#Changing Fbref's HTML so all tables are redable by bs4
html_content = requests.get(url).text.replace('<!--', '').replace('-->', '')
df = pd.read_html(html_content)
data=df[1]


# In[18]:


column_names = ["_".join(col) for col in data.columns.values]
column_names = [col.replace("Unnamed: ","").replace('_level_0','') for col in column_names]
data.columns = column_names
# If need to drop NaN's from the start, uncomment the code below
#data = data.dropna()
data[data.columns[0]]
display(data)
data.to_excel('other.xlsx',index=False)


# In[ ]:




