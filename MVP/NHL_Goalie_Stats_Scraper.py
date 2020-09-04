#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:24:01 2020

@author: andrew
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import numpy as np
import time

driver = webdriver.Chrome(executable_path = '/home/andrew/Chromedriver/chromedriver')
table_data, points, name = [],[],[]
for page in range(2):
    url = "http://www.nhl.com/stats/goalies?reportType=season&seasonFrom=20182019&seasonTo=20182019&gameType=2&filter=gamesPlayed,gte,1&sort=wins,savePct&page="+str(page)+"&pageSize=50"
    driver.get(url)
    driver.execute_script("window.scrollBy(0,10000)")
    driver.execute_script('document.getElementById("root").click();')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_data += soup.find_all("div", class_= "rt-td")
 #   points += soup.find_all("div", class_= "rt-td primarySort")
#    name += soup.find_all("div", class_= "rt-td rthfc-td-fixed-left rthfc-td-fixed-left-last")
    
    
    time.sleep(1)
driver.close()
data = [x.text for x in table_data]
points_data = [x.text for x in points]

data_dic = {}
stats = "rnk, player, season, team, shoots, pos, gp,w, l, t, ot, sa, svs, ga, sv_percent, gaa, toi, so, g, a, p, pim".split(",")
for i in range(len(stats)):
    data_dic[stats[i].strip(" ")] = data[i::len(stats)]
df = pd.DataFrame(data_dic)
df.replace('\xa0', np.nan, inplace=True)
df.dropna(subset = ['player'], inplace = True)

df.to_csv('NFL_Goalie_Stats.csv')

