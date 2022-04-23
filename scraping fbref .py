#!/usr/bin/env python
# coding: utf-8

# In[47]:


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


# In[48]:


global ooc_stats
global fa_stats


# In[78]:


def scrape_fa(url,names_fa,ind):
    ind=ind
    #Defining variables - url to the website + the table of choice (starting from 0 for the first table on the top)
    url = url
    global data
    #Changing Fbref's HTML so all tables are redable by bs4
    html_content = requests.get(url).text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    tno=[]
    for i in range(0,len(df)-1):
        if "Unnamed: 0_level_0" in df[i]:
            tno.append(i)
            break
    data=df[tno[0]]
    # Changing column names from tuples to strings 
    column_names = ["_".join(col) for col in data.columns.values]
    column_names = [col.replace("Unnamed: ","").replace('_level_0','') for col in column_names]
    data.columns = column_names
    
 
    # If need to drop NaN's from the start, uncomment the code below
    #data = data.dropna()
    data[data.columns[0]]
    if data.columns[0] == "0_Rk":
        data[data['1_Player'] != 'Player']
        del data['0_Rk']
    elif data.columns[0] == '0_Player':
        data[data['0_Player'] != 'Player']
    #display(data)
    club=(data['2_Squad'].astype(str).tolist())
    for i in data.columns:
        if i=='1_Age'or i=='3_Country'or i=='5_LgRank':
            data=data.drop(i,axis=1)
    #display(data)
    #display(fa_stats)
    l = [i for i, item in enumerate(club) if "Club" in item]
    #display(l)
    #display(club[6])
    #l=[ i for i, word in enumerate(club) if word.endswith('ubs') ]
    #display(data)
    #display(club)
    entry = data.loc[data['2_Squad'] == club[l[0]]]
    df=pd.DataFrame(entry)
    #display(df)
    df.insert(loc=0, column='Index', value=ind)
    df_reset=df.set_index('Index')
    return df

#scrape_fa(url,names_fa,i)


# In[79]:


def scrape_ooc(url,names_ooc,ind):
    ind=ind
    #Defining variables - url to the website + the table of choice (starting from 0 for the first table on the top)
    url = url
    global data
    #Changing Fbref's HTML so all tables are redable by bs4
    html_content = requests.get(url).text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    tno=[]
    for i in range(0,len(df)-1):
        if "Unnamed: 0_level_0" in df[i]:
            tno.append(i)
            break
    data=df[tno[0]]
    # Changing column names from tuples to strings 
    column_names = ["_".join(col) for col in data.columns.values]
    column_names = [col.replace("Unnamed: ","").replace('_level_0','') for col in column_names]
    data.columns = column_names
    
 
    # If need to drop NaN's from the start, uncomment the code below
    #data = data.dropna()
    data[data.columns[0]]
    if data.columns[0] == "0_Rk":
        data[data['1_Player'] != 'Player']
        del data['0_Rk']
    elif data.columns[0] == '0_Player':
        data[data['0_Player'] != 'Player']
    #display(data)
    club=(data['2_Squad'].astype(str).tolist())
    for i in data.columns:
        if i=='1_Age'or i=='3_Country'or i=='5_LgRank':
            data=data.drop(i,axis=1)
    #display(data)
    #display(fa_stats)
    l = [i for i, item in enumerate(club) if "Club" in item]
    #display(data)
    entry = data.loc[data['2_Squad'] == club[l[0]]]
    df=pd.DataFrame(entry)
    
    df.insert(loc=0, column='Index', value=ind)
    df_reset=df.set_index('Index')
    return df
  


# In[73]:


ooc=pd.read_excel('D:/college stuff/WINTER21-22/AI/out of contract1.xlsx')
fa=pd.read_excel('D:/college stuff/WINTER21-22/AI/FREE AGENT.xlsx')
names_ooc=ooc['Name'].tolist()
names_fa=fa['Name'].tolist()
#ooc_stats
#fa_stats
#names_ooc

fax=pd.DataFrame()
fax.insert(loc=0, column='Index', value=list(range(0,len(names_fa))))

oocx=pd.DataFrame()
oocx.insert(loc=0, column='Index', value=list(range(0,len(names_ooc))))


# In[121]:


# create webdriver object

path_to_extension = r'C:\Users\SHARAF\Desktop\3.12_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
#driver = Edge()
s=Service(ChromeDriverManager().install())
# Launch Microsoft Edge (Chromium)
#options = EdgeOptions()
#options.use_chromium = True
#driver = Edge(options = options)
#driver = webdriver.Edge(EdgeChromiumDriverManager().install(),chrome_options=options)
driver = webdriver.Chrome(service=s,chrome_options=chrome_options)
driver.maximize_window()
driver.create_options()
time.sleep(10)
window_name = driver.window_handles[1]
driver.switch_to.window(window_name=window_name)
time.sleep(10)
driver.close()
driver.switch_to.window(driver.window_handles[0])


# In[123]:


driver.get("https://fbref.com/en/")
x=[]
for i in range(98,len(names_fa)):
    
    # get element 
    element = driver.find_element(by=By.CLASS_NAME, value="ac-input")
    # create action chain object
    action = ActionChains(driver)
    element1= driver.find_element(by=By.CSS_SELECTOR, value=("input[type='search']"))
    action.click(on_element=element1)
    action.perform()
    element.send_keys(names_fa[i])
    #driver.execute_script("arguments[0].value=names_ooc[i]",element)
    element2=driver.find_element(by=By.CSS_SELECTOR, value=("input[type='submit']"))
    action.click(on_element=element2)
    action.perform()
    url=driver.current_url
    if "search" in url:
        driver.get("https://fbref.com/en/")
        continue
    #time.sleep(2)
    if i==0:
        ofax=scrape_fa(url,names_fa,i)
    #driver.switch_to.window(driver.window_handles[0])
    else:
        ofa1=scrape_ooc(url,names_fa,i)
        ofax= pd.concat([ofax,ofa1])
    x.append(i)


# In[126]:


driver.get("https://fbref.com/en/")
x=[]
for i in range(62,len(names_ooc)):
    
    # get element 
    element = driver.find_element(by=By.CLASS_NAME, value="ac-input")
    # create action chain object
    action = ActionChains(driver)
    element1= driver.find_element(by=By.CSS_SELECTOR, value=("input[type='search']"))
    action.click(on_element=element1)
    action.perform()
    element.send_keys(names_ooc[i])
    #driver.execute_script("arguments[0].value=names_ooc[i]",element)
    element2=driver.find_element(by=By.CSS_SELECTOR, value=("input[type='submit']"))
    action.click(on_element=element2)
    action.perform()
    url=driver.current_url
    if "search" in url:
        driver.get("https://fbref.com/en/")
        continue
    #time.sleep(2)
    if i==0:
        oocx=scrape_ooc(url,names_ooc,i)
    #driver.switch_to.window(driver.window_handles[0])
    else:
        ooc1=scrape_ooc(url,names_ooc,i)
        oocx= pd.concat([oocx,ooc1])
    x.append(i)


# In[128]:


ooc_stats=pd.DataFrame({'Player Name':names_ooc})
ooc_stats.insert(loc=0, column='Index', value=list(range(0,len(names_ooc))))
ooc_stats['Player Name'].astype(str)
ooc_stats=pd.merge(ooc_stats,oocx,on='Index')
ooc_stats.drop_duplicates('Player Name', keep='last',inplace = True)
#ooc_stats
ooc_stats.to_csv('ooc.csv',mode='a',index=False,header=False)
if x[-1]==0:
    ooc_stats.to_csv('ooc.csv',mode='a',index=False)
else:
    ooc_stats.to_csv('ooc.csv',mode='a',index=False,header=False)


# In[125]:


fa_stats=pd.DataFrame({'Player Name':names_fa[98:]})
fa_stats.insert(loc=0, column='Index', value=list(range(98,100)))
fa_stats['Player Name'].astype(str)
fa_stats=pd.merge(fa_stats,ofax,on='Index')
fa_stats.drop_duplicates('Player Name', keep='last',inplace = True)
fa_stats
if x[-1]==0:
    fa_stats.to_csv('fa.csv',mode='a',index=True)
else:
    fa_stats.to_csv('fa.csv',mode='a',index=True,header=False)

