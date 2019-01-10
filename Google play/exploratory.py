#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 23:40:04 2019

@author: lisa
"""

import os
path='/Users/lisa/machine-learning-for-python/Google play'
os.chdir(path)
print(os.listdir(path + '/Data'))

import pandas as pd
dat_store = pd.read_csv('Data/googleplaystore.csv')
dat_reviews = pd.read_csv('Data/googleplaystore_user_reviews.csv')

import pprint