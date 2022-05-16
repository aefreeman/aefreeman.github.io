#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:48:25 2020

@author: andrew
"""
"""
This job was used to clean up the WNBA salary data, which had the following format
rank
player
team
pos
salary

This converts it to

player team pos salary

"""

import pandas as pd

df = pd.read_csv("WNBA_Salaries_Temp.csv")
players, teams, position, salary, rnk = [df.iloc[i::5]['1'].tolist() for i in range(5)]
salary = [float(x[1:].replace(',','')) for x in salary]
df_new = pd.DataFrame(list(zip(players,teams,position,salary)), columns = ['Player','Team', 'Position', 'Salary'])
df_new.to_csv('WNBA_Salaries.csv')