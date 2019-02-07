#!/usr/bin/env python
# coding: utf-8

# pandas 0.23.4
# - important module in Data Analysis in Python
# 
# pycountry 18.12.8
# - provides the ISO databases.
# 

# In[32]:


import pandas as pd
import pycountry as pc


# Open `plik.csv` as dataframe `plik` without header and with `,` as separator in csv

# In[22]:


plik=pd.read_csv("plik.csv", header=None, sep=",")


# Print `plik` with a large file, display the first 5 results `plik.head()`

# In[23]:


plik


# It gives new headings for ease of operation: 
# - Data
# - Subdivisions
# - Number
# - Percent

# In[24]:


plik.columns = ['Data', 'Subdivisions', 'Number','Percent']


# change the column Data to datatime format

# In[25]:


plik['Data'] = pd.to_datetime(plik['Data'], format='%m/%d/%Y')


# change the column Percent to float without "%"

# In[26]:


plik['Percent'] = (plik['Percent'].str.rstrip('%')).astype('float')


# Create new column `CountryCode` with country code format `XXX` for subdivisions

# In[27]:


def get_country_code(name):
    """find the country code to the subdivisions name"""
    for co in pc.subdivisions:
        if name in co.name:
            return co.country_code
    return 'XXX'

def get_country_code_alpha_3(name):
    """find the country code format XXX to country code format XX"""
    for co in pc.countries:
        if name == 'XXX':
            return 'XXX'
        if name in co.alpha_2:
            return co.alpha_3
    return 'XXX'
kod=[]
names = plik['Subdivisions']
for name in names:
    code = get_country_code(name)
    kod.append(code)
    
names2 = kod
kod_alpha_3 = []
for name in names2:
    code = get_country_code_alpha_3(name)
    kod_alpha_3.append(code)
    
plik['CountryCode'] = kod_alpha_3


# Create new column `Clicks` that are the value of equation `( number * percent )/100`

# In[28]:


plik.insert(loc=5, column='Clicks', value=(round(((plik.Number * plik.Percent)/100),0)).astype('int'))


# Group by columns `Data` and `CountryCode`

# In[29]:


group = plik.groupby(by=["Data", 'CountryCode'])


# Print new group with sum of values in rows for columns `Number` and `Click`

# In[30]:


group['Number', 'Clicks'].sum().head()


# Write group to `new.csv` with separator `,`, with new header, without index. New plik will be saved in the same folder as this notebook. 

# In[31]:


group['Number', 'Clicks'].sum().reset_index().to_csv('new.csv')

