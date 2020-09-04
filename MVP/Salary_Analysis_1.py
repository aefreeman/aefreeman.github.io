#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Aug  5 22:35:37 2020

@author: andrew
"""

import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 8)

nhl = pd.read_csv('NHL_Salaries.csv')
mlb = pd.read_csv('MLB_Salaries.csv')
nfl = pd.read_csv('NFL_Salaries.csv')
nba = pd.read_csv('NBA_Salaries.csv')
wnba = pd.read_csv('WNBA_Salaries.csv')
mls = pd.read_csv('MLS_Salaries.csv')

nhl['League'] = "nhl"
mlb['League'] = "mlb"
nfl['League'] = "nfl"
nba['League'] = "nba"
wnba['League'] = "wnba"
mls['League'] = "mls"
#Add in NBA Positions
nba_2 = pd.read_csv('NBA_Stats.csv')
nba = nba.merge(nba_2[['Player_ID', 'Pos']], how = 'left', on = 'Player_ID').dropna(subset = ['Player', 'Pos'])

#Add in NHL Positions
nhl_2 = pd.read_csv("NHL_Skater_Stats.csv")
nhl_3 = pd.read_csv("NHL_Goalie_Stats.csv")
nhl = nhl.merge(nhl_2[['Player', 'Pos']], how = 'left', on = 'Player')
nhl.loc[nhl.Player.isin(nhl_3.Player.tolist()), 'Pos'] = 'G'

#No position means they are a rookie in 2019-2020, drop from data
    #This also might mean we are excluding players who retired after 2019
nhl.dropna(subset = ['Pos'], inplace=True)
nhl.rename(columns = {'Pos':'Position'}, inplace = True)

tm = [nhl, wnba, nfl, nba]
for df in tm:
    df.rename(columns={'Tm': 'Team'}, inplace = True)

#Pos = [nba,nfl]
#POS = [mlb]
#Position(s)  = [mls]
nba.rename(columns = {'Pos': 'Position'}, inplace = True)
nfl.rename(columns = {'Pos': 'Position'}, inplace = True)
mlb.rename(columns = {'POS': 'Position'}, inplace = True)
mls.rename(columns = {'Position(s)': 'Position'}, inplace = True)

mls.rename(columns={'Club':'Team', 'Base Salary':'Salary'}, inplace = True)
mls['Player'] = mls['First Name'] + ' ' + mls['Last Name']
mls.loc[mls.Player.isna(), 'Player'] = mls['Last Name']
nba.rename(columns={'2019-20':'Salary'}, inplace = True)
salary_df = pd.DataFrame()
for df in [nhl, mlb, nfl, nba, wnba, mls]:
    if df.Salary.dtype == np.object:
        df.Salary = df.Salary.str.replace('[,$]', '').astype(float)
    if salary_df.empty:
        salary_df = nhl
    else:
        salary_df = salary_df.append(df)
        
salary_df = salary_df[['Player', 'Salary', 'Team', 'League', 'Position']]

salary_df.to_csv('Comb_Salary_Data.csv')

