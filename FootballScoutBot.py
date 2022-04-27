#!/usr/bin/env python
# coding: utf-8

# In[3]:


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



# In[5]:


fa=pd.read_excel('fa.xlsx')
ooc=pd.read_excel('ooc.xlsx')
other=pd.read_excel('other.xlsx')
#display(fa)
#display(ooc)
#fa.fillna(0)
#ooc.fillna(0)
#display(other)


# In[ ]:


def get_budget(x):
    url = 'https://www.fifagamenews.com/fifa-22-career-mode-transfer-budgets/'
    #Changing Fbref's HTML so all tables are redable by bs4
    html_content = requests.get(url).text.replace('<!--', '').replace('-->', '')
    df = pd.read_html(html_content)
    Teams=[]
    for i in df:
        Teams.append(str(i).split('Name: 0, dtype: object'))

    t = ' '.join([str(elem) for elem in Teams])

    t=list(t.split("\\n"))
    #t=pd.DataFrame(t)

    #display(Teams[0])
    tno=[]
    x=x
    a=[]
    b=[]
    c=[]
    for i in t:
            a=x.split(" ")
            for j in a:
                j=j.capitalize()
                b.append(j)
            c.append(' '.join([str(elem) for elem in b]))
            break
    bud=[]      
    budget=[]
    for i in t:
        if c[0].lower()==x:
            if c[0] in i:
                i=i.split(c[0])
                x=i[1].split("  ")
                for i in range(1,len(x)):
                        p=x[i].split(" ")
                        if p[0]==" ":
                            bud.append(p[1:])
                            break
                        else:
                            bud.append(p[0:])
                            break
    budget.append('£')
    budget.append('.'.join([str(elem) for elem in bud[0]]))
    budget.append('m')
    return("".join([str(elem) for elem in budget]))


# In[ ]:


# Define the base time-series chart.
def get_chart(data):
    hover = alt.selection_single(
        fields=["Value"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Relation between Value and Age")
        .mark_line()
        .encode(
            x="Value",
            y="Age",
            color="Area",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Value",
            y="Age",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Value", title="Value (GBP)"),
                alt.Tooltip("Age", title="Age"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()




# In[ ]:


st.title("\t\t\t\t Welcome to The Football Scout Bot!     ")
st.title("Players will be shown from the following datasets:\ni)Out of contract \n ii)Free Agents\n iii)All other players in the top 5 Leagues (England,Spain,France,Germany,Italy)")    
if st.checkbox('Show Out of contract players',key='ooc'):
    st.subheader("Players Going Out Of Contract Names, Details and Statistics:")
    st.write(ooc)
if st.checkbox('Show free agents',key='fa'):
    st.subheader("Players Available For Free:")
    st.title("Players Available For Free")
    st.write(fa)
if st.checkbox("All others:"):
    st.title("Other players")
    st.write(other)


# In[67]:


st.title("But first, some observations!")
og=ooc.groupby(['Area']).mean()
of=fa.groupby(['Area']).mean()
st.write(og.iloc[: , -3:])
st.write(of.iloc[: , -3:])
st.write("We can see some obvious information such as Attackers have more npXg and Xg than defenders \n but something interesting to note is that midfielders play more minutes no matter what the age ")

st.subheader("For 'out of contracts dataset':")
st.area_chart(og)


st.subheader("For 'free agents dataset':")
st.area_chart(of)


# In[ ]:


chart_o = get_chart(ooc)
chart_f= get_chart(fa)
st.write("We can see that the price for defenders and midfielders rises with age while it drops for attackers.")
st.subheader("For 'out of contracts dataset':")
st.altair_chart(chart_o.interactive(), use_container_width=True)
st.subheader("For 'free agents dataset':")
st.altair_chart(chart_f.interactive(), use_container_width=True)


# In[71]:


name = st.text_input("Enter Team Name to search players for")
if(st.button('Submit')):
    x=get_budget(name)
    st.subheader('The budget of the selected team is: ')
    st.subheader(x)


# In[153]:


ooc.drop(ooc[ooc['Current Team']==name.capitalize()].index, inplace = True)
ooc.insert(loc=0, column='Total Efficiency', value=ooc['Non Penalty Efficiency']-ooc['Performance_CrdY']-ooc['Performance_CrdR'])
ooc=ooc.sort_values(by=['Age','Value','Total Efficiency'],ascending=[True,False,True])
fa.drop(fa[fa['Previous Team']==name.capitalize()].index, inplace = True)
fa.insert(loc=0, column='Total Efficiency', value=fa['Non Penalty Efficiency']-fa['Performance_CrdY']-fa['Performance_CrdR'])
fa=fa.sort_values(by=['Age','Value','Total Efficiency'],ascending=[True,False,True])


# In[154]:


ooc=ooc.drop(['Total Efficiency'],axis = 1)
fa=fa.drop(['Total Efficiency'],axis = 1)


# In[130]:


st.subheader("Suggested players:")
if st.checkbox('Show Out of contract players',key=3):
    st.subheader("Best Players Going Out Of Contract Names, Details and Statistics:")
    st.write(ooc.loc[:10, :])
if st.checkbox('Show free agents',key=4):
    st.subheader("Best Players Available For Free:")
    st.write(fa.loc[:10, :])
