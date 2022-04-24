#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas as pd , numpy as np

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
page = "https://www.transfermarkt.com/statistik/vertragslosespieler" 
pageTree = requests.get(page, headers=headers)
pageSoup = BeautifulSoup(pageTree.content, 'html.parser')


# In[6]:


Players = pageSoup.find_all("td", {"class": "hauptlink"})
Values = pageSoup.find_all("td", {"class": "hauptlink rechts"})
nationality=pageSoup.find_all("td",{"class": "zentriert"})
Age = pageSoup.find_all("td", {"class": "zentriert"})
oocs=pageSoup.find_all("td", {"class": "zentriert"})


# In[7]:


PlayersList = []
ValuesList = []
AgeList = []
NationalityList=[]
FreeSince=[]
name=[]
val=[]
pl=[]
nat=[]
fs=[]
ag=[]
for i in range(0,len(Players)):
    if i%2==0:
        name.append(str(Players[i]))
    else:
        val.append(str(Players[i]))
for i in range(0,len(name)):
    pl.append(str(name[i]).split('">"',1)[0].split(' title="',1)[1])
#display(pl)
for i in range(0,len(name)):
    PlayersList.append(str(pl[i]).split('</a> ',1)[0].split('">',1)[1])
#display(PlayersList)
for i in range(0,len(name)):
    ValuesList.append(str(val[i]).split('</td>',1)[0].split('">€',1)[1])
#ValuesList
#Values


# In[8]:


for i in range(0,len(nationality)):
    if i%3==0:
        nat.append(str(nationality[i]))
#nat
nat1=[]
for i in range(0,len(nat)):
    nat1.append(str(nat[i]).split('"/><',1)[0].split('title="',1)[1])
#first nationality
nat1=nat1[0:-5]
#nat1
#nat2=[]
#for i in range(0,len(nat)):
#    if 'br' for 'br' in nat if "" in s:
#        nat2.append(str(nat[i]).split(' class',1)[0].split('br/><img alt="',1)[1])
#second nationality??
#nat2


# In[9]:


age0=[]
#Age
for i in range(1,len(Age),3):
    age0.append(str(Age[i]))
age0=age0[0:-5]
#age0
for i in range(0,len(age0)):
    AgeList.append(str(age0[i]).split('</td>',1)[0].split('zentriert">',1)[1])
#AgeList


# In[12]:


for i in range(2,len(Age),3):
    fs.append(str(Age[i]))
fs=fs[0:-5]
fs
for i in range(0,len(fs)):
     FreeSince.append(str(fs[i]).split('</td>',1)[0].split('zentriert">',1)[1])
#FreeSince


# In[11]:


df=pd.DataFrame({"Name":PlayersList,"Value":ValuesList,"Age":AgeList,"Nationality":nat1,"Free Since":FreeSince})
df.head()
df.to_csv('free agent.csv', index=False)

