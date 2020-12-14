# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 14:15:56 2020

@author: Andre
"""

import pandas as pd

weeks = [1,2,3,4,5,6,7,8,9]
for week in weeks:
    with open(f'Week_{week}/Categories.csv') as cats_file:
        read_data = cats_file.read()
    if week == 1:
        cats = [x.strip() for x in str(read_data).split(',')]
    else:
        cats.extend([x.strip() for x in str(read_data).split(',')])
        
all_cats = set(cats)
cats_list = [[cat, cats.count(cat)] for cat in all_cats]