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

# Reading in the data
import pandas as pd
dat_store = pd.read_csv('Data/googleplaystore.csv')
dat_reviews = pd.read_csv('Data/googleplaystore_user_reviews.csv')

# Explore what we have for the data sets
list(dat_store) #get column names
list(dat_reviews)

dat_store.shape #(10841, 13)
dat_reviews.shape #(64295, 5)

# Look at basic plots to understand the data
## Look at dat_store data set first
from matplotlib import pyplot as pt

pt.plot(dat_store['Rating'])# there's a rating that is really weird
dat_store[['App', 'Rating']][dat_store.Rating > 5] # let's take a look
#App called Life Made WI-Fi Touchscreen Photo Frame has rating of 19.0, that's weird!
dat_store = dat_store[dat_store.Rating <=5] #filtering for ratings less than or equal to 5

dat_store[['Category','Rating']].boxplot(by='Category')
