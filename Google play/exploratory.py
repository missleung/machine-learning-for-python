#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 23:40:04 2019

@author: lisa
"""
# Setting directory

import os
path='/Users/lisa/machine-learning-for-python/Google play'
os.chdir(path)
print(os.listdir(path + '/Data'))

### Reading in the data

import numpy as np
import pandas as pd
dat_store = pd.read_csv('Data/googleplaystore.csv')
dat_reviews = pd.read_csv('Data/googleplaystore_user_reviews.csv')

# Explore what we have for the data sets

list(dat_store) #get column names
list(dat_reviews)

dat_store.shape #(10841, 13)
dat_reviews.shape #(64295, 5)

# Look at summary tables

dat_store.describe() # some numeric values aren't being read as numeric: reviews, size, installs, price
dat_reviews.describe()

### Data cleaning 

# Change variables to numeric
# Changing reviews 
def check_na(dat, old_var, new_var):
    print (dat[['App',old_var]][dat[new_var].isna()])

dat_store['newReviews'] = pd.to_numeric(dat_store['Reviews'], errors='coerce')
    
# Note: Life Made WI-Fi Touchscreen Photo Frame some how had 3.0M Reviews. Wrong record and will remove

# Change price
    
dat_store['newPrice'] = pd.to_numeric(dat_store['Price'].str.replace('$', ''), errors="coerce")
print (check_na(dat_store, 'Price', 'newPrice'))

# Note: Life Made WI-Fi Touchscreen Photo Frame has 'Everyone' in Price. Wrong record and will remove    

# Changing installs

dat_store['newInstalls'] = pd.to_numeric(dat_store['Installs'].str.replace('+', '').str.replace(',',''), errors='coerce')
print (check_na(dat_store, 'Installs', 'newInstalls'))

# Note: Life Made WI-Fi Touchscreen Photo Frame has 'Everyone' in Price. Wrong record and will remove    

# Changing size to Mb

dat_store['newSize'] = pd.to_numeric(dat_store['Size'].str.replace('M', '',case=False).str.replace('k','',case=False), errors='coerce')
INDEX_Kb = dat_store['Size'].str.contains('k', case=False)
dat_store.newSize[INDEX_Kb] = dat_store.newSize[INDEX_Kb]*0.001

print (check_na(dat_store, 'Size', 'newSize'))


# Some duplicates are completely duplicated (ie. all the values are exactly the same). Remove those

dat_store.drop_duplicates(keep=False,inplace=True)

# There's also some analysts who says there's a couple of duplicates for apps.

names_dups = dat_store.App[dat_store.duplicated(subset='App')] # there are 1170 duplicates

# Take a look at the duplicates

dat_dups = dat_store[dat_store.App.isin(names_dups)].sort_values(by='App')
dat_dups.head()

dat_uniqueDups = dat_store[dat_store.duplicated()]


### Exploratory analysis - plots
### Look at basic plots to understand the data
    
from matplotlib import pyplot as pt
    
# Look at dat_store data set first

pt.plot(dat_store['Rating'])# there's a rating that is really weird
dat_store[['App', 'Rating']][dat_store.Rating > 5] # let's take a look
#App called Life Made WI-Fi Touchscreen Photo Frame has rating of 19.0, that's weird!
dat_store = dat_store[dat_store.Rating <=5] #filtering for ratings less than or equal to 5


dat_store[['Category','Rating']].boxplot(by='Category')
