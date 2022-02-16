# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:06:38 2021

@author: 77978
"""

import pickle

import numpy             as np
import re
import sklearn
import xgboost           as xgb
import seaborn           as sns
import matplotlib.pyplot as plt

model = open(r'D:\gzx\work\JAKA\zdt\zdt_v1\ml\model\xgboost\xgboost_0816_v1.0.pickle', 'rb')

xgb_model = pickle.load(model)