#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:10:04 2020

@author: andrew
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

url = "https://www.nwslsoccer.com/stats?sort=g&season=2019#goalkeepers"
driver = webdriver.Chrome(executable_path = '/home/andrew/Chromedriver/chromedriver')
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
table_data = soup.find_all("span", class_= "table-cell jsx-3647524424")
saves = soup.find_all("span", class_= "table-cell jsx-3647524424 active")
player_first = soup.find_all("span", class_ = "stats-owner-info-cell__first-name")
player_last = soup.find_all("span", class_ = "stats-owner-info-cell__last-name")
players = [x.text + " " + player_last[i].text for i,x in enumerate(player_first)]
data = [x.text for x in table_data]
save_data = [x.text for x in saves]
#725
for i in range(2):
    time.sleep(1)
    #Each player is 75 tall
    height = 1050*i
    script = """
        ele = document.getElementsByClassName("ReactVirtualized__Grid ReactVirtualized__Table__Grid");
        ele[0].scrollTop ="""
    script += str(height) + ";"            
    driver.execute_script(script)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_data = soup.find_all("span", class_= "table-cell jsx-3647524424")
    saves = soup.find_all("span", class_= "table-cell jsx-3647524424 active")
    player_first = soup.find_all("span", class_ = "stats-owner-info-cell__first-name")
    player_last = soup.find_all("span", class_ = "stats-owner-info-cell__last-name")
    players += [x.text + " " + player_last[i].text for i,x in enumerate(player_first)]
    data += [x.text for x in table_data]
    save_data += [x.text for x in saves]
driver.close()
data_dic = {}
data_dic['Player'] = players
stats = "rnk, team, gp, gs, mins, ga, gaa, sog, cs, yc, rc".split(",")
for i in range(11):
    data_dic[stats[i].strip(" ")] = data[i::11]
data_dic['Saves'] = save_data
df = pd.DataFrame(data_dic)
df.drop_duplicates(inplace = True, subset = ['Player'])

df.to_csv('NWSL_Keeping_Stats.csv')