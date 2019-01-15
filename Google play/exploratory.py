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

# Note: Life Made WI-Fi Touchscreen Photo Frame has wrong record and will remove    

# Changing size to Mb

dat_store['newSize'] = dat_store['Size'].str.replace('M', '',case=False).str.replace('k','',case=False)
dat_store['newSize'] = pd.to_numeric(dat_store['newSize'], errors='coerce')
INDEX_Kb = dat_store['Size'].str.contains('k', case=False)
dat_store.newSize[INDEX_Kb] = dat_store.newSize[INDEX_Kb]*0.001

print (check_na(dat_store, 'Size', 'newSize'))

# Some duplicates are completely duplicated (ie. all the values are exactly the same). Remove those

dat_store.drop_duplicates(keep=False,inplace=True)

# There's also some analysts who says there's a couple of duplicates for apps.

names_dups = dat_store.App[dat_store.duplicated(subset='App')] # there are 566 duplicates

# Take a look at the duplicates

dat_dups = dat_store[dat_store.App.isin(names_dups)].sort_values(by='App')
dat_dups.head()

# It seems that apps that are duplicates are varied by number of reviews, etc.
# Will assume that the one with more reviews are the most updated one.
# Filter all apps by taking the max number of reviews

INDEX_nodups = dat_store.groupby('App')['newReviews'].transform(max)==dat_store['newReviews'] 
# nts: transform() adds new column to the data set. It's finding the rows where the max 
# newReview values matches the newReviews
dat_store = dat_store[INDEX_nodups] #results in 9386 rows

### Summary analysis on numerical values
dat_store.describe()

# there's a rating that is really weird
# App called Life Made WI-Fi Touchscreen Photo Frame has rating of 19.0. 
# This row is clearly misrecorded. Will remove this as well
dat_store = dat_store[dat_store.Rating <=5] #filtering for ratings less than or equal to 5


### Exploratory analysis - plots
### Look at basic plots to understand the data
    
from matplotlib import pylab as pt
import seaborn as sb
    
sb.set(style= "whitegrid")

# Look at dat_store data set first

bp_cat_rating = sb.boxplot(x='Category', y='Rating',data=dat_store)
for item in bp_cat_rating.get_xticklabels():
    item.set_rotation(90)
# We can see that all ratings from the categories have longer tails towards the low ratings
# and are skewed with most people giving higher ratings. Ignoring the outliers and interestingly, 
# we find two categories, dating and map/navigation are towards the lower ratings (I can see why...)
# We also see that the categories with more apps with lower ratings are Finance and Tools. 
# Of note, judgying by the medians, Books & Reference, Comics, Education, Events, and Health & Fitness
# seem to do a relatively better job. The next step (following these boxplots)
# is to see how many apps per categories are out there.
    
dat_cat_sum = dat_store.groupby('Category').count()
hist_cat_sum = sb.barplot(x='Category',y='App',data=dat_cat_sum)
# Interesting, Family is the categor 