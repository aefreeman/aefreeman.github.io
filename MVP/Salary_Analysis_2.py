#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:39:10 2020

@author: andrew
"""

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import time

df = pd.read_csv('Comb_Salary_Data.csv')
df.drop(columns = ['Unnamed: 0'], inplace=True)
df.dropna(subset = ['Position'], inplace=True)
df.League = df.League.str.upper()

data = []
for league in ['MLS', 'WNBA', 'NBA', 'NHL', 'NFL','MLB']:
    tmp_plot = go.Histogram(x =df.loc[df.League == league].Salary, name = league)
    data.append(tmp_plot)
    tmp_fig = go.Figure(data = [tmp_plot])
    tmp_fig.update_layout(title = league)
#    plot(tmp_fig)
#    time.sleep(0.5)
fig = go.Figure(data = data)
fig.update_layout(barmode='stack')
#plot(fig)
df.drop_duplicates(inplace = True, subset = ['Player', 'League', 'Team'])

df = df.join(df.groupby('League').Salary.mean(), on = 'League', rsuffix = '_mean')
df = df.join(df.groupby('League').Salary.std(), on = 'League', rsuffix = '_std_dev')
df['Z_Score'] = (df.Salary-df.Salary_mean)/df.Salary_std_dev
data = []
for league in ['MLS', 'WNBA', 'NBA', 'NHL', 'NFL','MLB']:
    tmp_plot = go.Histogram(x =df.loc[df.League == league].Z_Score, name = league + ' Z_Score')
    data.append(tmp_plot)
    tmp_fig = go.Figure(data = [tmp_plot])
    tmp_fig.update_layout(title = league + " Z_Score")
 #   plot(tmp_fig)
  #  time.sleep(0.5)
fig = go.Figure(data = data)
fig.update_layout(barmode='stack')
#plot(fig)

#Note: Kovalchuk's Salary is so low because it's a half year contract

#By position, by league
#Clean up positions
#list:
#for league in ['MLS', 'WNBA', 'NBA', 'NHL', 'NFL','MLB']:
 #   print(league + " ")
  #  print(df.loc[df.League==league].Position.unique())
   # print("\n")
#Anybody with two positions e.g. (SF-SG, QB/TE) is marked as the first one
df.Position = df.Position.str.split('[-/]', expand = True)[0]

#Synonyms:
    #NHL: RW, LW, W (1 guy - Jesper Bratt -LW)
    #MLB: RP, SP, P; CF, LF, RF, OF
        #All P, OF are rookies/minors, so we'll just exclude the position from analysis
        #Note that since we already did by league, dropping the data doesn' hurt
    #WNBA: Point Guard (only 2), Guard
    #NFL:['QB' 'DE' 'WR' 'LB' 'DT' 'OT' 'DB' 'CB' 'G' 'T' 'OLB' 'DL' 'ILB' 'FS' 'C'
            #'OL' 'TE' 'OG' 'LT' 'RB' 'K' 'FB' 'S' 'SS' 'P' 'LG' 'NT' 'EDGE' 'LS' 'HB']
    #Classed:
        #QB
        #WR
        #RB/HB/FB
        #TE
        #OL/OG/OT/T/G/C/LG/LT/LS = OL
        #DL/DT/DE/EDGE/NT = DL
        #DB/LB/CB/OLB/ILB/FS/S/SS = DB
        #K
        #P
    #Needs to because otherwise what's T vs OT, S vs. SS vs. FS vs. DB?
#NHL
df.loc[(df.League == "NHL")&(df.Position.isin(['W'])), 'Position'] = 'LW'
#Drop P, OF from MLB
df = df.loc[~((df.League=='MLB')&(df.Position.isin(['P', 'OF'])))]
#WNBA make em guards
df.loc[(df.League == "WNBA")&(df.Position.isin(['POINT GUARD'])), 'Position'] = 'GUARD'
#NFL
df.loc[(df.League == "NFL")&(df.Position.isin(['RB','HB','FB'])), 'Position'] = 'RB'
df.loc[(df.League == "NFL")&(df.Position.isin(['OL', 'OG', 'OT', 'T', 'G', 'C', 'LG', 'LT', 'LS'])), 'Position'] = 'OL'
df.loc[(df.League == "NFL")&(df.Position.isin(['DL', 'DT', 'DE', 'EDGE', 'NT'])), 'Position'] = 'DL'
df.loc[(df.League == "NFL")&(df.Position.isin(['DB', 'LB', 'CB', 'OLB', 'ILB', 'FS', 'S', 'SS'])), 'Position'] = 'DB'

df = df.join(df.groupby(['League','Position']).Salary.mean(), on = ['League', 'Position'], rsuffix = '_pos_mean')
df = df.join(df.groupby(['League','Position']).Salary.std(), on = ['League', 'Position'], rsuffix = '_pos_std_dev')
df['Pos_Z_Score'] = (df.Salary-df.Salary_pos_mean)/df.Salary_pos_std_dev

df.to_csv('Clean_Position_Salaries_Data.csv')

#df.loc[df.index.isin(df.groupby(['League', 'Position']).Pos_Z_Score.idxmax().tolist())][['League', 'Position','Team', 'Player', 'Salary', 'Pos_Z_Score']]

