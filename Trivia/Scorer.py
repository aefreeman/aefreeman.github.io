# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:06:56 2020

@author: Andrew
"""

import gspread
import numpy as np
import plotly.graph_objects as go
from oauth2client.service_account import ServiceAccountCredentials
from plotly.offline import plot
from git import Repo

def setup():
    REPO_DIR = r'C:\Users\Andrew\Documents\GitHub\aefreeman.github.io'
    spr_key = "1_58RHEKoNIKDze4SQeCFtnd7qsbLaQteoc0V8vYj_WQ"
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(spr_key)
    standings = sheet.get_worksheet(1)
    four_q = sheet.get_worksheet(2)
    quarter_bonus = sheet.get_worksheet(3)
    final_qs = sheet.get_worksheet(4)
    
    teams = standings.col_values(1)[1:]
    no_teams = len(teams)
    repo = Repo(REPO_DIR)
    return standings, four_q, quarter_bonus, final_qs, teams, no_teams, repo

def generate_plot():
    scores = standings.col_values(2)[1:]
    plt = go.Bar(x = teams, y = scores)
    fig = go.Figure(data = plt, layout = go.Layout())
    return fig

def get_stats(TYPE, QTR, QUESTION):
    if TYPE == "Quarter":
        strt = 2+((QTR-1)*4+(QUESTION-1))*no_teams
        end = strt + no_teams
        correct = four_q.col_values(6)[strt:end].count('x')
        return f'{correct} {"people" if correct != 1 else "person"} ({100*correct/no_teams:.0f}%) got question {QTR}-{QUESTION} correct.'
    elif TYPE == "Bonus":
        correct = list(map(int, quarter_bonus.col_values(2+(QTR-1)*3)[2:]))
        return f'The average number of {"points" if QTR == 2 else "correct answers"} was {np.mean(correct):.2f}. The maximum was {np.max(correct)}.'
    else:
        strt = 2+(QUESTION-1)*no_teams
        end = strt+no_teams
        correct = final_qs.col_values(6)[strt:end].count('x')
        wagers = list(map(int, final_qs.col_values(4)[strt:end]))
        pts = list(map(int,final_qs.col_values(7)[strt:end]))
        return f'{correct} {"people" if correct != 1 else "person"} ({100*correct/no_teams:.0f}%) got the previous question correct. The average wager was {np.mean(wagers):.2f}. The average points awarded was {np.mean(pts):.2f}'

def update(TYPE, QTR, QUESTION):
    fig = generate_plot()
    words = get_stats(TYPE, QTR, QUESTION)
    fig.write_image("img/fig1.png")
    html = open('words.txt', 'w')
    html.write(words)
    html.close()
    repo.index.add(files)
    repo.index.commit('Live Edits')
    origin = repo.remote('origin')
    origin.push()
    
        
    

