#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 19:36:31 2020

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


url = "https://www.spotrac.com/mlb/rankings/"
driver = webdriver.Chrome(executable_path = '/home/andrew/Chromedriver/chromedriver')
driver.get(url)
driver.execute_script("window.scrollBy(0,10000)")
time.sleep(5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.close()
table = soup.findAll("table")[0]
df = pd.read_html(str(table))[0]
df.drop(columns = 'Unnamed: 0', inplace=True)
df.rename(columns = {'Player':'tmp', 'salary':'Salary'}, inplace = True)
new = df.tmp.str.split('  ', n = 1, expand =True)
df['Player'], df['Team'] = new[0], new[1]
df.drop(columns = 'tmp', inplace=True)

df.to_csv('MLB_Salaries.csv')