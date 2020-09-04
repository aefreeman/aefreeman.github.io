#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 19:01:43 2020

@author: andrew
"""
"""
This function pulls all of the salary data for the MLB
from https://www.spotrac.com/mlb/rankings/
"""



import pandas as pd

#Only gets 100 rows for unknown reason
df = pd.read_html('https://www.spotrac.com/mlb/rankings/')[0]
df.drop(columns = 'Unnamed: 0', inplace=True)
df.rename(columns = {'Player':'tmp', 'salary':'Salary'}, inplace = True)
new = df.tmp.str.split('  ', n = 1, expand =True)
df['Player'], df['Team'] = new[0], new[1]
df.drop(columns = 'tmp', inplace=True)

#df.to_csv('MLB_Salaries.csv')