# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:49:58 2020

@author: Andrew
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:14:49 2020

@author: Andrew
"""

import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dd



"""To remove Aa from legend:
    plotly.min.js
    find x.tx
    set it equal to ""
"""



df = pd.read_csv('Games.csv')
divisions = pd.read_csv('Divisions.csv')
coordinates = pd.read_csv('Coordinates.csv')
df = df.loc[(df.Year == 2019)&(df.Week.str.isnumeric())]
divs = divisions.merge(coordinates, how = 'left', left_index=True, right_index=True)
divs.loc[divs.Team == 'LA/SD Chargers', 'Team'] = 'Los Angeles Chargers'
divs.loc[divs.Team == 'LA/STL Rams', 'Team'] = 'Los Angeles Rams'
colors = {'AFC North': '#990000', 'AFC East': '#ff3333', 'AFC West':'#cc0000', 'AFC South':'#ff6666',
          'NFC North': 'blue', 'NFC East': 'indigo', 'NFC South':'#2832c2', 'NFC West':'navy'}
divs['color'] = divs.Division.map(colors)
connections = {}
for team in divs.Team.tolist():
    connections[team] = df.loc[df['Winner/tie'] == team]['Loser/tie'].tolist()+df.loc[df['Loser/tie'] == team]['Winner/tie'].tolist()

def make_graph(highlight = {}):
    edge_x = []
    edge_y = []
    lines_x = []
    lines_y = []
    for team in divs.Team.tolist():
        team_x = divs.loc[divs.Team == team].x.values[0]
        team_y = divs.loc[divs.Team == team].y.values[0]
        for opp in connections[team]:
            if highlight.get(team, None) == opp:
                lines_x.append(team_x)
                lines_x.append(divs.loc[divs.Team == opp].x.values[0])
                lines_y.append(team_y)
                lines_y.append(divs.loc[divs.Team == opp].y.values[0])
            edge_x.append(team_x)
            edge_x.append(divs.loc[divs.Team == opp].x.values[0])
            edge_x.append(None)
            edge_y.append(team_y)
            edge_y.append(divs.loc[divs.Team == opp].y.values[0])
            edge_y.append(None)
            
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        name = 'Game(s) played',
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_traces = []
    if lines_x:
        lines_trace = go.Scatter(
                x=lines_x, y=lines_y,
                name = 'Highlight',
                line=dict(width=2, color='black'),
                hoverinfo='none',
                mode='lines')   
    divs_ordered = ['AFC East', 'AFC North', 'AFC South', 'AFC West',
                    'NFC East', 'NFC North', 'NFC South', 'NFC West']
    
    text_spots = {'AFC North': 'middle left', 'AFC East': 'middle left', 'AFC West':'middle left', 'AFC South':'middle left',
              'NFC North': 'middle right', 'NFC East': 'middle right', 'NFC South':'middle right', 'NFC West':'middle right'}
    divs['location'] = divs.Division.map(text_spots)
    adjust = {'Oakland Raiders':'top center',
              'Los Angeles Chargers':'top center',
              'Miami Dolphins': 'bottom center',
              'New England Patriots': 'bottom center',
              'Detroit Lions':'top center',
              'Chicago Bears':'top center',
              'Philadelphia Eagles': 'bottom center',
              'Washington Redskins': 'bottom center',
              }
    divs.loc[divs.Team.isin(adjust.keys()), 'location'] = divs.loc[divs.Team.isin(adjust)].Team.map(adjust) 
    for div in divs_ordered:
        texts = divs.loc[divs.Division == div].Team.tolist()
        texts = [t if not t in ['Washington Redskins','Miami Dolphins'] else ' <br> '.join(t.split()) for t in texts]
        node_traces.append(go.Scatter(
        x=divs.loc[divs.Division == div].x.tolist(), y=divs.loc[divs.Division == div].y.tolist(),
        name = div,
        mode='markers+text',
        text = texts,
        textposition=divs.loc[divs.Division == div].location.tolist(),
        hoverinfo='text',
        marker=dict(
            color=divs.loc[divs.Division == div].color.tolist(),
            size=10
            ),
            line_width=2))
    data=[edge_trace] + node_traces
    if lines_x:
        data .append(lines_trace)
    
    fig = go.Figure(data = data,
                 layout=go.Layout(
    #                title='<br>Network graph made with Python',
                         paper_bgcolor='#E4ECF5',
                         height = 600,width = 1500,
                    titlefont_size=16,
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range = [-130,130]),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

def find_conn(x,y):
    if x == y:
        return {}
    if y in connections[x]:
        return {x:y}
    for team in connections[x]:
        if y in connections[team]:
            return {x:team, y:team}
    return {}
        
        

fig = make_graph()

app = dash.Dash('NFL')
server = app.server
app.layout = html.Div(children=[
        html.Div(children=[dcc.Dropdown(id = 'Team_1', value = None, options = [{'label':i, 'value':i} for i in sorted(divisions.Team.tolist())])]),
        html.Div(children=[dcc.Dropdown(id = 'Team_2', value = None, options = [{'label':i, 'value':i} for i in sorted(divisions.Team.tolist())])]),
        html.Div(
            children = [dcc.Graph(id = 'fig', figure=fig)]
            )
        ])
@app.callback(
        dd.Output('fig', 'figure'),
    [dd.Input('Team_1', 'value'),
    dd.Input('Team_2', 'value')])
def switch(team_1,team_2):
    high = find_conn(team_1, team_2)
    return make_graph(high)

if __name__ == '__main__':
    app.run_server(debug=True)

