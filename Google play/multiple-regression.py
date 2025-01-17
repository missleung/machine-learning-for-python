#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 17:45:19 2019

@author: lisa
"""

# Set directory
import os
path='/Users/lisa/machine-learning-for-python/Google play'
os.chdir(path)

import numpy as np
import pandas as pd

# Read data
dat_store = pd.read_csv('Data/googleplaystore_clean.csv') # 7930 observations

dat_y = dat_store[['Rating']]
dat_X = dat_store.drop(columns=['Rating','Unnamed: 0','Reviews',
                                'Price','Installs', 'Size',
                                'App', 'Last Updated', 'Android Ver',
                                'Current Ver'])

# Need to re-label the categorical variables
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
le=LabelEncoder()
dat_X[['codeCat', 
       'codeType', 
       'codeContRating', 
       'codeGenres']] = dat_X[['Category', 
                    'Type', 
                    'Content Rating', 
                    'Genres']].apply(le.fit_transform)



dat_X.columns
# Get ready to split data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(dat_X, dat_y, test_size=0.33, random_state=42)

# Let's predict ratings using linear regression

from sklearn import linear_model as lm

reg = lm.LinearRegression()

# Work the trained data set to the linear regression
reg.fit(X_train, y_train)

