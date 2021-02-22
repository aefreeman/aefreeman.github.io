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
for page in range(19):
    url = "http://www.nhl.com/stats/skaters?reportType=season&seasonFrom=20182019&seasonTo=20182019&gameType=2&filter=gamesPlayed,gte,1&sort=points&page="+str(page)+"&pageSize=50"
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
stats = "rnk, player, season, team, shoots, pos, gp, g, a, pts, plus_minus, pim, p_gp, evg, evp, ppg, ppp, shg, shp, otg, gwg, s, s_percent, to_gp, fow_percent".split(",")
for i in range(25):
    data_dic[stats[i].strip(" ")] = data[i::25]
df = pd.DataFrame(data_dic)
df.replace('\xa0', np.nan, inplace=True)
df.dropna(subset = ['player'], inplace = True)

df.to_csv('NFL_Skater_Stats.csv')
