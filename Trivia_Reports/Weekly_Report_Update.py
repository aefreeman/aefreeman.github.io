#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 22:58:29 2020

@author: andrew
"""

from Weekly_Report import Trivia
from plotly.offline import plot
import plotly.graph_objects as go
import numpy as np
from colour import Color


weeks = [1,2,3,4,5,6]
trivia = Trivia(weeks)

def color_split(x, dark=0):
    x = x.split(',')
    if not dark:
        return f'hsl({x[0]},{x[1]},{x[2]})'
    return f'hsl({x[0]},{x[1]},{int(x[2])-20*dark})'
        

def make_standings_table(trivia):
    data = trivia.season_df
    data.index = data.index.set_names(['Team'])
    try:
        data.reset_index(inplace=True)
    except ValueError:
        pass
    data['highlights'] = data.loc[:, ~data.columns.isin(['Total', 'Team'])].apply(lambda x: np.argsort(x.values)[-5:][::-1], axis=1)
    header = dict(values = ["Team", "Total"] + [f"Week {x}" for x in range(1,11)],
                   line_color='darkslategray')
    data = data.reindex(["Team", "Total"] + [f"Week_{x}" for x in range(1,11)] + ['highlights'], axis=1)
    data = data.round(2)
    data.reset_index(inplace=True, drop=True)
    fill_df = data.merge(trivia.colors, how = 'left', on = 'Team')
    fill_col=fill_df.Color.apply(lambda x: color_split(x)).tolist()
    fill_col_dark=fill_df.Color.apply(lambda x: color_split(x,dark=1)).tolist()
    fill_col_darker=fill_df.Color.apply(lambda x: color_split(x,dark=1.5)).tolist()
    fill_col = list(zip(fill_col, fill_col_dark, fill_col_darker))
    fill_color = []
    scores = data.loc[:, ~data.columns.isin(['Total', 'Team', 'highlights'])].values.tolist()
    for i, team in enumerate(data.Team.tolist()):
        fill_tmp = [fill_col[i][1]] *2 + [fill_col[i][2] if scores[i][x] == 100 else fill_col[i][0] if not x in data.loc[data.Team == team].highlights.values[0] else fill_col[i][1] for x in range(10)]
        fill_color.extend(fill_tmp)
    fill_color = [fill_color[x::12] for x in range(12)]
    fonts = ['black' for i in range(12*len(data.Team))]
    white = [data.Team.tolist().index('Team MBF'), data.Team.tolist().index('Team Name')]
    for c in white:
        fonts[12*c:12*c+12] = ['white' for i in range((12))]
    fonts= [fonts[x::12] for x in range(12)]
    cells = dict(values = data.loc[:, data.columns != 'highlights'].T.values,
                  line_color='darkslategray',
                  fill_color = fill_color,
                  font_color = fonts)

    fig = go.Figure(data = [go.Table(
            columnwidth = [50] + [20 for x in range(11)],
            header=header, cells=cells)])
    
    #plot(fig)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html("Write_Up/img/Standings.html")
    


def make_records(trivia):
    best_text = []
    for best in [['q1', 'First Quarter Bonus'], ['h', 'Halftime Bonus'],
                 ['q3','Third Quarter Bonus'], ['f', 'Final Bonus']]:
        a = getattr(trivia.season_overall, f'best_{best[0]}')
        b = f'{a[0][0]} by {a[0][1]}, Week {a[1]}'
        best_text.append(b)
    a = getattr(trivia.season_overall, 'best_t')
    record = f'{a[0][0]} by {a[0][1]}, Week {a[1]}'
    best_text.append(record)
    cols = ['Best Q1 Bonus', 'Best Halftime Bonus', 'Best Q3 Bonus',
            'Best Final Questions', 'Highest Total']
    cells = dict(values = [cols]+[best_text],
              line_color='darkslategray',
              )
    header = dict(values = ['Metric', 'Record'],
                   line_color='darkslategray'
                   )
    fig = go.Figure(data = [go.Table(
            header=header, cells=cells)])

    file_name = f"Write_Up/img/Records.html"
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html(file_name)


def make_color(b):
    global colors
    a = min(int(len(colors)*b), len(colors)-1)
    return colors[a].hex


def make_cats(trivia):
    df = trivia.season_overall.cats_df
    df.index = df.index.set_names(['Category'])
    try:
        df.reset_index(inplace=True)
    except ValueError:
        pass
    df.index = df.index.set_names(['Ind'])
    df.sort_values('Category', inplace=True)
    cols = ['Category', 'Correct Answers', 'Total Answers', 'Points Earned',
            'Points Wagered', 'Percent Correct', 'Percent of Points']
    header = dict(values = cols,
                   line_color='darkslategray'
                   )
    df = df.round(2)
    t_data = df.T.values[1:]
    m = [max(y) for y in t_data]
    b_color = []
    for i, t in enumerate(t_data):
        b_color.append([s/m[i] for s in t])
    
    fill_color = [['white' for i in range(len(df))]] + [[make_color(x) for x in b] for b in  b_color]
    #fill_color = [fill_color[x::len(df.columns)] for x in range(len(df.columns))]
    cells = dict(values = df.T.values,
                 fill_color = fill_color,
                  line_color='darkslategray',
                  format = [[],[],[],[],[],['%'],['%']])

    fig = go.Figure(data = [go.Table(
            header=header, cells=cells)])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    #plot(fig)
    fig.write_html("Write_Up/img/Cats.html")

def make_cats_team(trivia, team):
    df = trivia.team_season[team].cats_df
    df.index = df.index.set_names(['Category'])
    try:
        df.reset_index(inplace=True)
    except ValueError:
        pass
    df.index = df.index.set_names(['Ind'])
    df.sort_values('Category', inplace=True)
    cols = ['Category', 'Correct Answers', 'Total Answers', 'Points Earned',
            'Points Wagered', 'Percent Correct', 'Percent of Points']
    header = dict(values = cols,
                   line_color='darkslategray'
                   )
    df = df.round(2)
    t_data = df.T.values[1:]
    m = [max(y) for y in t_data]
    b_color = []
    for i, t in enumerate(t_data):
        b_color.append([s/m[i] for s in t])
    
    fill_color = [['white' for i in range(len(df))]] + [[make_color(x) for x in b] for b in  b_color]
    #fill_color = [fill_color[x::len(df.columns)] for x in range(len(df.columns))]
    cells = dict(values = df.T.values,
                 fill_color = fill_color,
                  line_color='darkslategray',
                  format = [[],[],[],[],[],['%'],['%']])

    fig = go.Figure(data = [go.Table(
            header=header, cells=cells)])
    
    #plot(fig)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Cats.html"
    fig.write_html(file_name)

def make_butterfly(trivia, team):
    fig = trivia.team_season[team].Butterfly
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Butterfly.html"
    fig.write_html(file_name)

def make_season_plots(trivia, team):
    fig = trivia.team_season[team].weekly_plots
    fig.update_layout(xaxis_title = "Week", yaxis_title= "Score")
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Weekly.html"
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html(file_name)

def make_season_all(trivia, team):
    fig = trivia.team_season[team].weekly_clean
    fig.update_layout(xaxis_title = "Question", yaxis_title= "Score")
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_All_Weeks.html"
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html(file_name)

def make_week_score(trivia, team, week):
    fig = trivia.team_weeks[team][week][1].running_plot
    fig.update_layout(xaxis_title = "Question", yaxis_title= "Score")
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Week_{week}.html"
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.write_html(file_name)

def make_week_cat(trivia, team, week):
    df = trivia.team_weeks[team][week][1].cats_df
    df.index = df.index.set_names(['Category'])
    try:
        df.reset_index(inplace=True)
    except ValueError:
        pass
    df.index = df.index.set_names(['Ind'])
    df.sort_values('Category', inplace=True)
    cols = ['Category', 'Correct Answers', 'Total Answers', 'Points Earned',
            'Points Wagered', 'Percent Correct', 'Percent of Points']
    header = dict(values = cols,
                   line_color='darkslategray'
                   )
    df = df.round(2)
    t_data = df.T.values[1:]
    m = [max(y) for y in t_data]
    b_color = []
    for i, t in enumerate(t_data):
        b_color.append([s/m[i] for s in t])
    
    fill_color = [['white' for i in range(len(df))]] + [[make_color(x) for x in b] for b in  b_color]
    #fill_color = [fill_color[x::len(df.columns)] for x in range(len(df.columns))]
    cells = dict(values = df.T.values,
                 fill_color = fill_color,
                  line_color='darkslategray',
                  format = [[],[],[],[],[],['%'],['%']])

    fig = go.Figure(data = [go.Table(
            header=header, cells=cells)])
    
    #plot(fig)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Week_{week}_Cats.html"
    fig.write_html(file_name)

def make_running_table(trivia, team, week):
    data = trivia.team_weeks[team][week][1]
    bonus_q1_total = data.total_q1
    bonus_q3_total = data.total_q3
    bonus_funny = data.total_bonus
    bonus_half = data.total_h
    bonus_final = data.total_f
    df = data.running_score
    q1_total = df[3]
    q2_total = df[8]-df[4]
    q3_total = df[13]-df[9]
    q4_total = df[18]-df[14]
    total = df[-1]
    optimality = data.optimality
    l = [q1_total, bonus_q1_total, q2_total, bonus_half, q3_total, bonus_q3_total,
         q4_total, bonus_final, bonus_funny, total, optimality]
    cols = ['Quarter 1 Score',
             'Quarter 1 Bonus',
             'Quarter 2 Score',
             'Halftime Bonus',
             'Quarter 3 Score',
             'Quarter 3 Bonus','Quarter 4 Score',
             'Final Points',
             'Bonus Points',
             'Total Score',
             'Wager Optimality']
    
    cells = dict(values = [cols]+[l],
                  line_color='darkslategray',
                  )
    header = dict(values = ['Round', 'Points'],
                   line_color='darkslategray'
                   )
    fig = go.Figure(data = [go.Table(
            header=header, cells=cells)])
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    file_name = f"Write_Up/img/{team.replace(' ', '_')}_Week_{week}_Breakdown.html"
    fig.write_html(file_name)
    
s_col = Color("#fa8575")
colors = list(s_col.range_to(Color("#009c50"),10))
#Overall
make_standings_table(trivia)# -> to HTML
make_records(trivia)# -> local var
make_cats(trivia)# -> to HTML
#Individual
teams = trivia.teams
for team in teams:
    print(f'Making Team: {team}')
    print('.....Overall')
    team_weeks = [x[0] for x in trivia.team_weeks[team]]
    make_butterfly(trivia, team)
    make_season_plots(trivia, team)
    make_season_all(trivia, team)
    ##        make_cats_team(trivia, team)
    for i, week in enumerate(team_weeks):
        print(f'.....Week {week}')
        make_week_score(trivia, team, i)
        make_week_cat(trivia, team, i)
        make_running_table(trivia, team, i)