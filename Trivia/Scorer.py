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

"""
To remove Aa from legend:
    plotly.min.js
    find x.tx
    set it equal to ""
"""


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
    template = open('HTML_Format.txt', 'r')
    html_temp = template.read()
    template.close()
    
    return standings, four_q, quarter_bonus, final_qs, teams, no_teams, repo, html_temp

def generate_plot():
    new_scores = [float(x) for x in standings.col_values(2)[1:]]
    s_scores = sorted(new_scores, reverse = True)[:3]
    labs = [f'{x[0]} {x[1]} - {x[2]}' if x[0] == 'Quarter' else f'Quarter {x[1]} Bonus' if x[0] == 'Bonus' else f'Final Question {x[2]}' for x in questions[:counter]]
    labs.insert(0, 'Game Start')
    fig = go.Figure()
    for i, team in enumerate(new_scores):
        scores[i].append(team)
        data_labs = [None for j in range(counter-1)] + [teams[i] if team in s_scores else None]
        fig.add_trace(go.Scatter(x = labs,y =scores[i], name = teams[i],mode="lines+text", text = data_labs, textposition = "middle right"))
    fig.update_layout(xaxis_type='category',
                  width = 1050, xaxis_range = [-0.5, counter + (counter//10)+0.5])
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
    print('...generating data')
    fig = generate_plot()
    words = get_stats(TYPE, QTR, QUESTION)
    data = html_temp.replace('<Text here>', words)
    fig.write_image("img/fig1.png")
    print('...updating html')
    html = open('Live_Tracker.html', 'w')
    html.write(data)
    html.close()
    repo.index.add(files)
    repo.index.commit('Live Edits')
    origin = repo.remote('origin')
    print('...pushing to github')
    origin.push()
    print(f'...done! {TYPE} - {QTR} - {QUESTION}')
    
    
        
    

