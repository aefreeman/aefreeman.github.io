#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:41:09 2020

@author: andrew
"""

import pandas as pd
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dd
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol
from plotly.offline import plot
#from operator import itemgetter



df = pd.read_csv('Clean_Position_Salaries_Data.csv')
df.rename(columns = {'Z_Score':'League_Z_Score'}, inplace = True)
highest_paid = df.loc[df.index.isin(df.groupby(['League', 'Position']).Pos_Z_Score.idxmax().tolist())][['League', 'Position','Team', 'Player', 'Salary', 'Pos_Z_Score']]
#lowest_paid = df.loc[df.index.isin(df.groupby(['League', 'Position']).Pos_Z_Score.idxmin().tolist())][['League', 'Position','Team', 'Player', 'Salary', 'Pos_Z_Score']]
stats = df.groupby(['League','Position']).Salary.describe()[['mean', 'std','min','max']]
stats.reset_index(inplace=True)
stats = stats.merge(highest_paid[['League', 'Position', 'Player','Pos_Z_Score']], on = ['League', 'Position'], how = 'left')
stats.rename(columns = {'Player':'Max_Player', 'Pos_Z_Score':'Max_Pos_Z_Score'}, inplace=True)
tbl_data = df[['Player','League', 'Team', 'Position', 'Salary', 'League_Z_Score', 'Pos_Z_Score']]
cols = [{"name": i, "id": i} for i in tbl_data.columns]
cols[4]['type'] = 'numeric'
cols[4]['format'] = FormatTemplate.money(0)
for i in [5,6]:
    cols[i]['type'] = 'numeric'
    cols[i]['format'] = Format(precision = 3, scheme = Scheme.fixed)
def make_fig(league=None, position = None, sort_by = 'Salary'):
    asc = True
    if sort_by in ['Salary', 'League_Z_Score', 'Pos_Z_Score']:
        asc = False
    if league != None:
        data = df.loc[df.League.isin(league)]
    else:
        data = df
    if position != None:
        data = data.loc[data.Position.isin(position)]
    plt_1 = go.Histogram(x=data.Salary)
    #plt_2 = go.Histogram(x=data.Pos_Z_Score)
    fig = go.Figure(data = [plt_1], layout=go.Layout())
    tbl_data = data[['Player', 'League', 'Team', 'Position', 'Salary', 'League_Z_Score', 'Pos_Z_Score']].sort_values(sort_by, ascending = asc).to_dict('records')
    
#    fig.update_layout(
#    annotations=[
#        dict(
#            x=data.Salary.max()+data.Salary.min()*2/3,
#            y=1,
#            xref="x",
#            yref="y",
#            text=f'Highest Paid Player: {data.loc[data.Salary.idxmax()].Player} - ${data.loc[data.Salary.idxmax()].Salary:,.2f}',
#            showarrow=True,
#            arrowhead=1,
#            ax=0,
#            ay=-50
#        )
#    ]
#    )
    return fig, tbl_data
def highlight(fig, t):
    #TODO: Make this not broken
    fig['data'] = [fig['data'][0]]
    fig['data'].append(go.Histogram(x=t.Salary, nbinsx = 1))
    fig['layout']['barmode'] = 'overlay'
    fig['layout']['showlegend'] = False
    return fig

fig, t_data = make_fig()
tbl = dash_table.DataTable(id = 'table', columns = cols, data = t_data,style_cell={'textAlign': 'center'},)

app = dash.Dash('Salary')
server = app.server
app.layout = html.Div(children=[
        html.Div(children=[dcc.Dropdown(id = 'League', value = None,multi = True, options = [{'label':i, 'value':i} for i in sorted(stats.League.unique().tolist())])]),
        html.Div(children=[dcc.Dropdown(id = 'Position', value = None,multi = True, options = [{'label':i, 'value':i} for i in sorted(stats.Position.unique().tolist())])]),
        html.Div(children=[dcc.Dropdown(id = 'sort_by', value = 'Salary', options = [{'label':i, 'value':i} for i in tbl_data.columns])]),
        html.Div(
            children = [dcc.Graph(id = 'fig', figure=fig)]
            ),
        html.Div(children = tbl),
        html.Div(id = 'hid', children = [], style={'display': 'none'} )
        ])
@app.callback(
        [dd.Output('fig', 'figure'), dd.Output('table', 'data'), dd.Output('Position', 'options'), dd.Output('hid', 'children')],
    [dd.Input('League', 'value'),dd.Input('Position', 'value'), dd.Input('sort_by', 'value'),dd.Input('fig', 'clickData')],
    [dd.State('fig', 'figure'), dd.State('Position', 'options'), dd.State('table', 'data'), dd.State('hid', 'children')])
def switch(league, position, sort_by, clickData, last_fig, last_options, tbl_data, last_click):
    #raise ValueError(league)
    ctx = dash.callback_context.triggered[0]
    #raise ValueError(ctx)
    if (ctx['prop_id'] == 'fig.clickData'):
        c = ctx['value']['points'][0]['pointNumbers']
        if c == last_click:
            pass
        #raise ValueError(last_fig)
        else:
            options = last_options
            tmp = pd.DataFrame(t_data)
            asc = True
            if sort_by in ['Salary', 'League_Z_Score', 'Pos_Z_Score']:
                asc = False
            #raise ValueError(f['data'])
            data = last_fig['data'][0]['x']
            sals = [data[x] for x in c]
            t = tmp.loc[tmp.Salary.isin(sals)]
            f = highlight(last_fig, t)
            t.sort_values(sort_by, inplace = True, ascending = asc)
            t = t.to_dict('Records')
            return f, t, options, c
    if league == []:
        league = None
    if position == []:
        position = None
    f, t = make_fig(league, position, sort_by)
    if league != None:
        options = [{'label':i, 'value':i} for i in sorted(stats.loc[stats.League.isin(league)].Position.unique().tolist())]
    else:
        options = [{'label':i, 'value':i} for i in sorted(stats.Position.unique().tolist())]
    return f,t, options, []


if __name__ == '__main__':
    app.run_server(debug=True)

