#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:18:25 2020

@author: andrew
"""

import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
"""This does the same thing as MLB Salary Scraper, except it gets all of the players.

The original issue is that the site only loads 100 players unless you scroll down.
This scrolls, waits for the site to load, then scrapes it.
"""


url = "https://www.mlssoccer.com/stats/season?year=2019&group=shots&sort=desc&order=SOG"
driver = webdriver.Chrome(executable_path = '/home/andrew/Chromedriver/chromedriver')
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
table = soup.findAll("table")[0]
df = pd.read_html(str(table))[0]

for page in range(1, 25):
    page_url = "https://www.mlssoccer.com/stats/season?page="+str(page)+"&year=2019&group=shots&sort=desc&order=SOG"
    driver = webdriver.Chrome(executable_path = '/home/andrew/Chromedriver/chromedriver')
    driver.get(page_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    table = soup.findAll("table")[0]
    df_new = pd.read_html(str(table))[0]
    df = df.append(df_new)

df.to_csv('MLS_Attacking_Stats.csv')