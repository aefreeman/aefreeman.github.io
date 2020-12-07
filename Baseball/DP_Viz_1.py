#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 11:56:36 2020

@author: andrew
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
#from plotly.offline import plot
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies as dd
import dash_daq as daq
from PIL import Image

full_df = pd.read_csv('All_DPs_Clean.csv', usecols = [1, 4,5,9,10,11,12], dtype = {'DP':'object', 'Cleaned_Play':'object'})
full_df.drop_duplicates(subset = ['Game', 'Inning'], inplace = True)
full_df['length'] = full_df.DP.str.len()
full_df.Inning = full_df.Inning.apply(lambda x: x[0].upper() + x[1:])
full_df['URL_Act'] = full_df['URL'].apply(lambda x: f'[{x}]({x})')
f = go.Figure(data = [go.Scatter(x = [0,10], y = [0,10])])
node_df = pd.read_csv('Sankey_Node.csv')
link_df = pd.read_csv('Sankey_Link.csv')
sankey = go.Sankey()
sankey['node']['label'] = node_df.iloc[1].tolist()[1:]
sankey['node']['color'] = node_df.iloc[0].tolist()[1:]
sankey['link']['source'] = link_df.iloc[1].astype(int).tolist()[1:]
sankey['link']['color'] = link_df.iloc[0].tolist()[1:]
sankey['link']['value'] = link_df.iloc[3].astype(int).tolist()[1:]
sankey['link']['target'] = link_df.iloc[2].astype(int).tolist()[1:]
del node_df
del link_df
#sankey = make_init_sankey(node, link)
# Add trace
img = Image.open('Field.jpg')
# Add images
f.add_layout_image(
        dict(
            source=img,
            xref="x",
            yref="y",
            x=0,
            y=10,
            sizex=10,
            sizey=10,
            sizing="stretch",
            opacity=1,
            layer="below")
)
f.update_xaxes(range = [0,10], showgrid=False, showticklabels = False)
f.update_yaxes(range = [0,10], showgrid=False, showticklabels = False)
f.update_layout(showlegend = False)
layout = f['layout']
sankey_label = ['Batter'] + [str(i) for i in range(1,10)]*full_df.length.max(),
node_init= dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = sankey_label[0],
          color = ["blue" for _ in sankey_label[0]]
        )


def update_fig_data(df, string=''):
    x = [5,5,6.5,5.6,3.6,4.4,2.5,5,7.8]
    y = [3.2,1,4,5.2,4,5.2,7,8,7]
    df = df.loc[df.DP.str[:len(string)] == string]
    dps = df.DP.unique().tolist()
    dps = list(set([x[:len(string)+1] for x in dps]))
    if string == '':
        last = ''
    else:
        last = string[-1]
    colors = []
    for position in range(1,10):
        if last == str(position):
            colors.append('rgb(0,0,256)')
        elif (string + str(position)) in dps:
            colors.append('rgb(0,0,0)')
        else:
            colors.append('rgba(0,0,0,0)')
    plt_1 = go.Scatter(x = x, y = y, marker_color = colors, mode='markers', marker_size = 18, text = [i if not colors[i-1] == 'rgba(0,0,0,0)' else '' for i in range(1,10)], hoverinfo='text')
    if len(string)<2:
        data = [plt_1]
    else:
        x_coords = [x[int(f)-1] for f in string[:-1]]
        y_coords = [y[int(f)-1] for f in string[:-1]]
        x_2 = [x[int(f)-1] for f in string[-2:]]
        y_2 =[y[int(f)-1] for f in string[-2:]]
        lines = 'black'
        lines_2 = 'blue'
        plt_2 = go.Scatter(x = x_coords, y = y_coords, line_color = lines, marker_line_color = 'red',marker_line_width = 2, marker_size = 18, marker_color = 'rgba(0,0,0,0)')
        plt_3 = go.Scatter(x = x_2, y = y_2, mode = 'lines', line_color = lines_2)
        data = [plt_2, plt_3, plt_1]
    return data
def update_table_data(df, string = '', end = False, old = True):
    df.sort_values('Date', inplace = True)
    if end == False:
        if old == True:
            d = df.loc[df.DP.str[:len(string)]== string].tail(10)[['Date', 'Home_Team', 'Away_Team', 'Inning', 'DP', 'URL_Act']].to_dict('records')
        else:
            d = df.loc[df.DP.str[:len(string)]== string].head(10)[['Date', 'Home_Team', 'Away_Team', 'Inning', 'DP', 'URL_Act']].to_dict('records')
        
    else:
        if old == True:
            d = df.loc[df.DP == string].tail(10)[['Date', 'Home_Team', 'Away_Team', 'Inning', 'DP', 'URL_Act']].to_dict('records')
        else:
            d = df.loc[df.DP == string].head(10)[['Date', 'Home_Team', 'Away_Team', 'Inning', 'DP', 'URL_Act']].to_dict('records')
        
    return d
#def make_init_sankey(node, link):
#
#    return go.Sankey(node = node, link=link)
def update_sankey(sankey, string = '', back = False, clear = False, ended = '0'):
    node_colors = sankey['node']['color']
    link_colors = sankey['link']['color']
    comb_links = list(zip(sankey['link']['source'], sankey['link']['target']))
    if not back and not clear:
        if len(string) < 2:
            cur_link = ''
        else:
            cur_link = comb_links.index((9*(len(string)-2) + int(string[-2]), 9*(len(string)-1) + int(string[-1])))
        if string == '':
            cur_node = 0
        else:
            cur_node = 9*(len(string)-1) + int(string[-1])
        node_colors = ['red' if c == 'rgb(0,0,256)' or c == 'red' else 'black' for c in node_colors]
        node_colors[cur_node] = 'rgb(0,0,256)'
        link_colors = ['rgba(153,153,153,1)' if c == 'blue' or c == 'rgba(153,153,153,1)' else 'rgba(209,209,209,0.8)' for c in link_colors]
        if cur_link != '':
            link_colors[cur_link] = 'blue'
    elif clear:
        node_colors = ['black' for c in node_colors]
        link_colors = ['rgba(209,209,209,0.8)' for c in link_colors]
    elif ended == '1':
        node_colors = node_colors
        link_colors = link_colors
    else:
        node_colors = ['black' if c == 'rgb(0,0,256)' or c == 'black' else 'red' for c in node_colors]
        if len(string) > 0:
            node_colors[len(node_colors)-node_colors[::-1].index('red')-1] = 'rgb(0,0,256)'
        link_colors = ['rgba(209,209,209,0.8)' if c == 'rgba(209,209,209,0.8)' or c == 'blue' else 'rgba(153,153,153,1)' for c in link_colors]
        if len(string) > 1:
            link_colors[len(link_colors)-link_colors[::-1].index('rgba(153,153,153,1)')-1] = 'blue'
    sankey['node']['color'] = node_colors
    sankey['link']['color'] = link_colors
    return sankey

table_cols = [{'name':i.replace('_', ' '), 'id':i} for i in ['Date', 'Home_Team', 'Away_Team', 'Inning', 'DP', 'URL_Act']]
table_cols[-1]['presentation'] = 'markdown'
table_cols[-1]['name'] = 'Link to Box Score'
table_cols[-2]['name'] = 'Double Play'
#print('Making Table')
table_data = update_table_data(full_df, '')
table = dash_table.DataTable(id = 'table', columns = table_cols, data = table_data, style_cell={'textAlign': 'center'})
#print('Making Sankey')

#print('Making Figure')
trace = update_fig_data(full_df, '')
trace_fig = go.Figure(data = trace, layout = layout)
sankey_fig = go.Figure(data = sankey)

app = dash.Dash('Double Plays')
server = app.server
app.layout = html.Div(children=[
        html.H1("MLB Double Play Tracker"),
#        html.Div(children=[dcc.Dropdown(id = 'Team_1', value = None, options = [{'label':i, 'value':i} for i in sorted(divisions.Team.tolist())])]),
#        html.Div(children=[dcc.Dropdown(id = 'Team_2', value = None, options = [{'label':i, 'value':i} for i in sorted(divisions.Team.tolist())])]),
        html.Button('Back', id='Back', n_clicks=0),
        html.Button('Reset', id='Clear', n_clicks=0),
        html.Div(),
        html.Div(
            children = [dcc.Graph(id = 'trace_fig', figure=trace_fig)],style = {'display': 'inline-block',  'width': '40%', 'margin-left':'10%'}
            ),
        html.Div(
            children = [dcc.Graph(id = 'sankey_fig', figure=sankey_fig)],style = {'display': 'inline-block', 'width': '40%'}
            ),
        html.Div(id = 'Counter', children = [html.Plaintext(f'There are {full_df.DP.count()} double plays in the database')], style = {'width': '50%', "margin":"0 auto"}),
        daq.ToggleSwitch(id = 'old_toggle', value = True, label = 'Show Newest DPs'),
        html.Div(
            children = [table], style = {'width': '50%', "margin":"0 auto"}
            ),
        html.Div(children = [html.H3('How to Use This'), html.Plaintext("""Select a position from the diamond. From there, you can select further positions. To go back one level, click back. 
To see plays that ended at a position, select it twice. For example, to see 3(U), click 3 twice. The table shows the 10 most recent double plays fitting your criteria. Data is from 1916-2019."""),
        html.Plaintext("""The information used here was obtained free of charge from and is copyrighted by Retrosheet.  Interested parties may contact Retrosheet at "www.retrosheet.org".""")]),
        html.Div(id = 'hid', children = [''], style={'display': 'none'}),
        html.Div(id = 'hid_2', children = [''], style={'display': 'none'})
        ])
#@app.callback(
#        dd.Output('fig', 'figure'),
#    [dd.Input('Team_1', 'value'),
#    dd.Input('Team_2', 'value')])
#def switch(team_1,team_2):
#    high = find_conn(team_1, team_2)
#    return make_graph(high)
@app.callback(
        [dd.Output('trace_fig', 'figure'),
         dd.Output('sankey_fig', 'figure'),
         dd.Output('table', 'data'),
         dd.Output('hid', 'children'),
         dd.Output('hid_2', 'children'),
         dd.Output('Counter', 'children')],
         [dd.Input('trace_fig', 'clickData'),
          dd.Input('Back', 'n_clicks'),
          dd.Input('Clear', 'n_clicks'),
          dd.Input('old_toggle', 'value')],
         [dd.State('hid', 'children'),
         dd.State('sankey_fig', 'figure'),
         dd.State('hid_2', 'children')])
def update(clickData, back_but, clear_clr, old_toggle,string, sankey, hid_2):
    string = string[0]
    back = False
    clear = False
    end = False
    ended = '0'
    ctx = dash.callback_context.triggered[0]
    sankey = sankey['data'][0]
    #raise ValueError(clickData)
    if ctx['prop_id'] == 'trace_fig.clickData':
        new_string = clickData['points'][0]['text']
        if len(string)>0:
            if new_string == string[-1]:
                end = True
                new_string = ''
                ended = '1'
        string += new_string
    #    raise ValueError(string)
    elif ctx['prop_id'] == 'Back.n_clicks':
        back = True
        if hid_2[0] != '1':
            string = string[:-1]
    elif ctx['prop_id'] == 'Clear.n_clicks':
        clear= True
        string = ''
    elif ctx['prop_id'] == 'old_toggle.value':
        ended = '1'
    new_trace_data = update_fig_data(full_df, string)
    new_table_data = update_table_data(full_df, string, end, old_toggle)
    new_sankey = update_sankey(sankey, string, back, clear, hid_2[0])
    new_sankey_fig = go.Figure(data = new_sankey)
    trace_fig = go.Figure(data = new_trace_data, layout = layout)
    if end or ended == '1':
        count = full_df.loc[full_df.DP == string].DP.count()
        if len(string) > 1:
            dp_string = "-".join(string)
        else:
            dp_string = string + '(U)'
    elif string == '':
        count = full_df.DP.count()
        dp_string = ""
    else:
        count = full_df.loc[full_df.DP.str[:len(string)]==string].DP.count()
        dp_string = "-".join(string) + "-___"
    counter = f'There {"are" if count!=1 else "is"} {count:,} {dp_string} double play{"s" if count != 1 else ""} in the database'
    return trace_fig, new_sankey_fig, new_table_data, [string], [ended], counter

if __name__ == '__main__':
    app.run_server(debug=True)

