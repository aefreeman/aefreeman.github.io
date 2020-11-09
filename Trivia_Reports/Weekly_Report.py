#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 21:03:03 2020

@author: andrew
"""

#import necessary libraries
from dataclasses import dataclass
import numpy as np
import pandas as pd
import plotly.graph_objects as go
#used to plot in spyder - example at bottom

#Dataclass
@dataclass
class Overall:
    """
    Overall Single Week values.
    Passed: list of single week results
    Returns: overall statistics as a class
    """
    #Variables being set initially, equivalent to 
    #self.__init__(self, teams):
    #       self.teams=teams
    #In a std class
    
    teams: list
    
    def __post_init__(self):
        #Automatically called after initializing
        self.get_main_stats()
        self.get_quarter_stats()
        self.get_half_stats()
        self.get_final_stats()
        self.update_plots()
        self.team_total = len(self.teams)
    
    def update_plots(self):
        r_score = [x.running_score for x in self.teams]
        self.r_score_mean = [np.average(x) for x in zip(*r_score)]
        self.r_score_max = [max(x) for x in zip(*r_score)]
        cat_list = [f'{i}-{j}' for i in range(1, 5) for j in range(1,5)]
        cat_list.insert(4,'Q1_Bonus')
        cat_list.insert(9, 'Halftime')
        cat_list.insert(14, 'Q3_Bonus')
        cat_list.insert(19, 'Final')
        self.running_plot_tmp_mean = go.Scatter(x = cat_list, y = self.r_score_mean, name='Mean', mode = 'markers+lines')
        self.running_plot_tmp_max = go.Scatter(x = cat_list, y = self.r_score_max, name='Max', mode = 'markers+lines')
        self.running_plot = go.Figure(data = [self.running_plot_tmp_mean, self.running_plot_tmp_max])
        self.total_plot = go.Figure(data = [x for y in [t.running_plot_data for t in self.teams] for x in y])
        for t in self.teams:
            t.running_plot_data.extend([self.running_plot_tmp_mean, self.running_plot_tmp_max])
            t.running_plot = go.Figure(data=t.running_plot_data)


        
        
    
    def get_main_stats(self):
        self.mean = np.average([t.total for t in self.teams])
        self.std= np.std([t.total for t in self.teams])
        hits = [x.hit_plot for x in self.teams]
        self.hit_plot = [sum(x) for x in zip(*hits)]
        self.cats_score = {c: [
             sum(t.cats_score[c][i] for t in self.teams) for i in range(4)
                ] for c in list(self.teams[0].cats_score.keys())}
        final_score = [x.final_score for x in self.teams]
        self.best_t = [max(final_score), self.teams[final_score.index(max(final_score))].name]
        
    
    def get_quarter_stats(self):
        q1_points = [x.total_q1 for x in self.teams]
        self.mean_q1 = np.average(q1_points)
        self.std_q1 = np.std(q1_points)
        q3_points = [x.total_q3 for x in self.teams]
        self.mean_q3 = np.average(q3_points)
        self.std_q3 = np.std(q3_points)
        self.best_q1 = [max(q1_points), self.teams[q1_points.index(max(q1_points))].name]
        self.best_q3 = [max(q3_points), self.teams[q3_points.index(max(q3_points))].name]
    
    def get_half_stats(self):
        half_points = [x.total_h for x in self.teams]
        self.mean_h = np.average(half_points)
        self.std_h = np.std(half_points)
        self.best_h = [max(half_points), self.teams[half_points.index(max(half_points))].name]
    
    def get_final_stats(self):
        final_points = [x.total_f for x in self.teams]
        self.mean_f = np.average(final_points)
        self.std_f = np.std(final_points)
        self.best_f = [max(final_points), self.teams[final_points.index(max(final_points))].name]
        
        
    
@dataclass    
class Trivia_Team:
    name: str
    df: pd.core.frame.DataFrame
    df_f: pd.core.frame.DataFrame
    df_h: pd.core.frame.DataFrame
    df_q: pd.core.frame.DataFrame
    cats: list
    week_number: int
    color: str
    def __post_init__(self):
        self.get_main_stats()
        self.get_quarter_stats()
        self.get_half_stats()
        self.get_final_stats()
        self.get_plots()
        
    def get_plots(self):
        self.running_score = self.df.loc[self.df.Question.str[0]=='1'].Points_Earned.cumsum().tolist()
        self.running_score.append(self.df_q.Q1_Correct.values[0]*2+self.running_score[-1])
        tmp = self.running_score[-1]
        self.running_score.extend([tmp + x for x in self.df.loc[self.df.Question.str[0]=='2'].Points_Earned.cumsum().tolist()])
        self.running_score.append(self.df_h.Points.sum()+self.running_score[-1]+self.total_bonus)
        tmp = self.running_score[-1]
        self.running_score.extend([tmp + x for x in self.df.loc[self.df.Question.str[0]=='3'].Points_Earned.cumsum().tolist()])
        self.running_score.append(self.df_q.Q3_Correct.values[0]*2+self.running_score[-1])
        tmp = self.running_score[-1]
        self.running_score.extend([tmp + x for x in self.df.loc[self.df.Question.str[0]=='4'].Points_Earned.cumsum().tolist()])
        self.running_score.append(self.df_f.Points.sum()+self.running_score[-1])
        cat_list = [f'{i}-{j}' for i in range(1, 5) for j in range(1,5)]
        cat_list.insert(4,'Q1_Bonus')
        cat_list.insert(9, 'Halftime')
        cat_list.insert(14, 'Q3_Bonus')
        cat_list.insert(19, 'Final')
        self.running_plot_data = [go.Scatter(x = cat_list, y = self.running_score, mode = 'markers+lines', name = self.name + '_' + str(self.week_number), marker_color = self.color)]
        self.final_score = self.running_score[-1]

    
    def get_main_stats(self):
        self.total = self.df.Points_Earned.sum()
        self.total_correct = self.df.loc[self.df.Points_Earned > 0].Points_Earned.count()
        self.mean = self.df.loc[self.df.Points_Earned > 0].Points_Earned.mean()
        self.wagers = {str(x):[self.df.loc[self.df.Wager==x].Points_Earned.sum(), self.df.loc[self.df.Wager==x].Wager.count()*x, self.df.loc[self.df.Wager==x].Wager.count()] for x in self.df.Wager.unique()}
        self.bet_strat = self.df.Wager.tolist()
        self.best_bet_strat, self.max_score = self.get_best_bet()
        self.optimality = self.total - self.max_score
        self.df['bin_correct'] = np.where(self.df.Correct=='x', 1, 0)
        self.hit_plot = self.df.bin_correct.tolist()
        self.made_cats = [self.cats[x] for x in range(len(self.cats)) if self.hit_plot[x]]
        cats_uniq = set(self.cats)
        cat_scores = list(zip(self.cats, self.hit_plot))
        self.cats_score = {c: 
            [sum(cat_scores[i][1] for i in range(len(cat_scores)) if cat_scores[i][0]==c),
             sum(1 for i in range(len(cat_scores)) if cat_scores[i][0]==c),
             sum(self.bet_strat[i] for i in range(len(cat_scores)) if cat_scores[i][0]==c and cat_scores[i][1]),
             sum(self.bet_strat[i] for i in range(len(cat_scores)) if cat_scores[i][0]==c)
             ] for c in cats_uniq}
        self.cats_score_helper = ['Correct', 'Answers', 'Points Earned', 'Points Wagered']
        self.cats_df = pd.DataFrame(self.cats_score,index = ['Answered_Correctly', 'Answered', 'Points_Earned', 'Points_Wagered']).T
        self.cats_df['Answered_Percent'] = self.cats_df['Answered_Correctly']/self.cats_df['Answered']
        self.cats_df['Points_Percent'] = self.cats_df['Points_Earned']/self.cats_df['Points_Wagered']
        
        
    def get_quarter_stats(self):
        self.total_q1 = self.df_q.Q1_Correct.sum()*2
        self.total_q3 = self.df_q.Q3_Correct.sum()*2
        self.total_bonus = self.df_q.Bonus_Correct.sum()
        
    def get_half_stats(self):
        self.total_h = self.df_h.Points.sum()
        
    def get_final_stats(self):
        self.total_f = self.df_f.Points.sum()
        
    def get_best_bet(self):
        best_bet_strat = []
        max_score = 0
        for quarter in [1,2,3,4]:
            tmp_df = self.df.loc[self.df.Question.str[0]==str(quarter)]
            wagers = [1,3,5,7]
            if quarter > 2:
                wagers = [x + 1 for x in wagers]
            for question in tmp_df.Question:
                if tmp_df.loc[tmp_df.Question==question].Correct.values[0] == 'x':
                    max_score += wagers[-1]
                    best_bet_strat.append(wagers.pop())
                else:
                    best_bet_strat.append(wagers.pop(0))
        return best_bet_strat, max_score

@dataclass
class Season_Team:
    weeks: list
    
    def __post_init__(self):
        self.get_main_stats()
        self.cats_score_helper = ['Correct', 'Answers', 'Points Earned', 'Points Wagered']
        
    def get_main_stats(self):
        self.all_cats = list(set([x for y in [list(w.cats_score.keys()) for w in self.weeks] for x in y]))
        self.cats_score = {c: [
             sum(t.cats_score[c][i] for t in self.weeks if c in t.cats_score) for i in range(4)
                ] for c in self.all_cats}
        self.weekly_plots = go.Figure(data = [go.Scatter(x = [a.week_number for a in self.weeks], y = [a.final_score for a in self.weeks])])
        self.weekly_running = [t.running_plot for t in self.weeks]
        self.weekly_running_clean_data = [a for b in [x.data for x in self.weekly_running] for a in b]
        self.weekly_running_clean_data = [x for x in self.weekly_running_clean_data if not x['name'] in ['Mean', 'Max']]
        self.weekly_clean = go.Figure(data = self.weekly_running_clean_data)
        self.weeks_played = [t.week_number for t in self.weeks]
        self.week_pair = list(zip(self.weeks_played, self.weeks))
        self.Season_Points = [0 for i in range(10)]
        self.optimality = [t.optimality for t in self.weeks]
        for week in self.week_pair:
            self.Season_Points[week[0]-1] = week[1].Season_Points
        self.cats_df = pd.DataFrame(self.cats_score,index = ['Answered_Correctly', 'Answered', 'Points_Earned', 'Points_Wagered']).T
        self.cats_df['Answered_Percent'] = self.cats_df['Answered_Correctly']/self.cats_df['Answered']
        self.cats_df['Points_Percent'] = self.cats_df['Points_Earned']/self.cats_df['Points_Wagered']

@dataclass
class Season_Total:
    weeks: list
    
    def __post_init__(self):
        self.get_main_stats()
        self.cats_score_helper = ['Correct', 'Answers', 'Points Earned', 'Points Wagered']
        
    def get_main_stats(self):
        self.all_cats = list(set([x for y in [list(w.cats_score.keys()) for w in self.weeks] for x in y]))
        self.cats_score = {c: [
             sum(t.cats_score[c][i] for t in self.weeks if c in t.cats_score) for i in range(4)
                ] for c in self.all_cats}
        self.cats_df = pd.DataFrame(self.cats_score,index = ['Answered_Correctly', 'Answered', 'Points_Earned', 'Points_Wagered']).T
        self.cats_df['Answered_Percent'] = self.cats_df['Answered_Correctly']/self.cats_df['Answered']
        self.cats_df['Points_Percent'] = self.cats_df['Points_Earned']/self.cats_df['Points_Wagered']    
        self.plot_data = [x for y in [t.total_plot['data'] for t in self.weeks] for x in y]
        self.plot_data = sorted(self.plot_data, key = lambda x: x['name'])
        self.total_plot = go.Figure(data = self.plot_data)
        q1_scores = [x.best_q1 for x in self.weeks]
        self.best_q1 = [max(q1_scores, key=lambda x:x[0]), q1_scores.index(max(q1_scores, key=lambda x:x[0]))+1]
        q3_scores = [x.best_q3 for x in self.weeks]
        self.best_q3 = [max(q3_scores, key=lambda x:x[0]), q3_scores.index(max(q3_scores, key=lambda x:x[0]))+1]
        h_scores = [x.best_h for x in self.weeks]
        self.best_h = [max(h_scores, key=lambda x:x[0]), h_scores.index(max(h_scores, key=lambda x:x[0]))+1]
        f_scores = [x.best_f for x in self.weeks]
        self.best_f = [max(f_scores, key=lambda x:x[0]), f_scores.index(max(f_scores, key=lambda x:x[0]))+1]
        t_scores = [x.best_t for x in self.weeks]
        self.best_t = [max(t_scores, key=lambda x:x[0]), t_scores.index(max(t_scores, key=lambda x:x[0]))+1]
        
class Trivia:
    def __init__(self, weeks, Colors_CSV = 'Teams.csv'):
        self.weeks = weeks
        self.colors = pd.read_csv(Colors_CSV)
        self.teams = self.colors.Team.tolist()
        self.team_weeks = {}
        self.overall_weeks = {}
        self.team_season = {}
        self.get_data()
        
        #self.season_overall
        #self.season_standings
        #self.cats_df
    
        
        
    def get_data(self):
        for week in self.weeks:
            week_tms = {}
            df = pd.read_csv(f'Week_{week}/Regulation.csv')
            df_f = pd.read_csv(f'Week_{week}/Final.csv')
            df_h = pd.read_csv(f'Week_{week}/Halftime.csv')
            df_q = pd.read_csv(f'Week_{week}/Quarter.csv')
            with open(f'Week_{week}/Categories.csv') as cats_file:
                read_data = cats_file.read()
            cats = [x.strip() for x in str(read_data).split(',')]
            week_teams = df.Team.unique().tolist()
            for team in week_teams:
                team_color = self.colors.loc[self.colors.Team == team].Color.values[0].split(',')
                color = f'hsla({team_color[0]}, {team_color[1]}, {str(int(team_color[2])-5*(week-1))},1)'
                tm = Trivia_Team(team, df.loc[df.Team == team],
                 df_f.loc[df_f.Team == team],
                 df_h.loc[df_h.Team == team],
                 df_q.loc[df_q.Team == team],
                 cats, week, color)
                if not team in self.team_weeks.keys():
                    self.team_weeks[team] = [[week,tm]]
                else:
                    self.team_weeks[team].append([week,tm])
                week_tms[team] = tm
            max_score = max([week_tms[t].final_score for t in week_teams])
            for team in week_teams:
                week_tms[team].Season_Points = week_tms[team].final_score/max_score*100
            self.overall_weeks[week] = Overall(list(week_tms.values()))
        for team in self.teams:
            games = [x[1] for x in self.team_weeks[team]]
            self.team_season[team] = Season_Team(games)
        self.season_overall = Season_Total(list(self.overall_weeks.values()))
        cats_df = pd.DataFrame(self.season_overall.cats_score, index = ['Answered_Correctly', 'Answered', 'Points_Earned', 'Points_Wagered']).T
        cats_df['Answered_Percent'] = cats_df['Answered_Correctly']/cats_df['Answered']
        cats_df['Points_Percent'] = cats_df['Points_Earned']/cats_df['Points_Wagered']
        self.cats_df = cats_df
        self.season_standings = {t:self.team_season[t].Season_Points for t in self.team_season.keys()}
        season_df = pd.DataFrame(self.season_standings)
        season_df.index = [f'Week_{i+1}' for i in range(10)]
        season_df = season_df.T
        season_df['Total'] = season_df.apply(lambda x: sum(sorted(x, reverse=True)[:5]), axis = 1)
        season_df.sort_values('Total', inplace=True, ascending=False)
        self.season_df = season_df
        for team in self.teams:
            a = self.team_season[team].cats_df.merge(self.cats_df, left_index=True, right_index=True, suffixes=['_Team', '_Total'])
            a.sort_index(inplace=True, ascending = False)
            data = []
            butter_color_template = self.colors.loc[self.colors.Team == team].Color.values[0].split(',')
            butter_color = f'hsl({butter_color_template[0]},{butter_color_template[1]},{butter_color_template[2]})'
            a['team_text'] = a.apply(lambda x: f'Correct: {int(x.Answered_Correctly_Team)}/{int(x.Answered_Team)} <br>Points: {x.Points_Earned_Team}/{x.Points_Wagered_Team}', axis =1)
            a['total_text'] = a.apply(lambda x: f'Correct: {int(x.Answered_Correctly_Total)}/{int(x.Answered_Total)} <br>Points: {x.Points_Earned_Total}/{x.Points_Wagered_Total}', axis =1)
            self.team_season[team].tmp = a.Answered_Percent_Team
            data.append(go.Bar(name = team, y=[i for i in range(len(a.Answered_Percent_Team))],x=a.Answered_Percent_Team, orientation = 'h', marker_color = butter_color, hovertext = a.team_text, hoverinfo = 'text', text = [f'{100*x:.0f}%' for x in a.Answered_Percent_Team], textposition = 'auto'))
            data.append(go.Bar(name = 'Total', y=[i for i in range(len(a.Answered_Percent_Team))],x=a.Answered_Percent_Total, orientation = 'h', xaxis = 'x2', yaxis = 'y2', marker_color = 'darkgrey',hovertext = a.total_text, hoverinfo = 'text', text = [f'{100*x:.0f}%' for x in a.Answered_Percent_Total], textposition = 'auto'))
            data.append(go.Scatter(x = [1 for i in range(len(a.Points_Percent_Team))], y = [i for i in range(len(a.Points_Percent_Team))], orientation = 'h', mode = 'text', text = list(a.index),xaxis = 'x3', yaxis = 'y3', hoverinfo = None, showlegend=False))
            fig = go.Figure(data = data, layout = go.Layout())
            numb_cats = len(a.index)
            fig.update_layout(
                xaxis=dict(
                    domain=[0, 0.45],
                    range = [1.02,0],
                ),
                yaxis=dict(
                    range = [-2,2+numb_cats],
                    visible = False
                ),
                xaxis2=dict(
                    domain = [0.55, 1],
                    range = [0,1.02],
                ),
                xaxis3=dict(
                    domain = [0.45, 0.55],
                    visible = False
                ),
                yaxis2 = dict(range = [-2,2+numb_cats],
                              visible = False),
                yaxis3 = dict(range = [-2,2+numb_cats],
                              visible = False)
            )
            self.team_season[team].Butterfly = fig
    @staticmethod
    def help():
        print("\n")
        print("Trivia_Weekly_Report".center(80, '_'))
        print("The main variables of this class are:")
        print("*teams: a list of teams")
        print("*team_weeks: a dictionary of teams")
        print(".....team_weeks[<team>] returns a list of [week_number, Trivia_Team object]")
        print("*team_season: a dictionary of teams")
        print(".....team_season[<team>] returns a Season_Team object")
        print("*overall_weeks: a dictionary of weeks")
        print(".....overall_weeks[<week>] returns an Overall object")
        print("*season_overall: a Season_Total object")
        print("*season_standings: a dictionary of season_standings")
        print("*season_df: season_standings as a dataframe")
        print("*cats_df: a dataframe of the overall categories with accuracy and points")
        print("\n")
        print("Examples of Data Calls".center(80, '_'))
        print("*team_season[<team>].weekly_plots")
        print(".....plot of scores(y) vs. week number(x)")
        print("*team_season[<team>].weekly_clean")
        print(".....plot of score(y) vs. question(x) over all weeks")
        print("*season_overall.total_plot")
        print(".....team_season.weekly_clean for all teams simultaneously")
        print("*team_weeks[<team>][<week>][1].running_plot")
        print(".....team_season.weekly_plots for one week with max and mean lines")
        print(".....note the [1] call to access the Trivia_Team object in the sublist")
        print(".....this should be replaced at some point")
        print("*team_season[<team>].Butterfly")
        print(".....plots a buttefly plot of <team>'s category accuracy vs. total")
        print("*team_weeks[<team>][<week>][1].optimality")
        print(".....returns a float <=0 representing a teams betting efficiency")
        print(".....calc'd by assuming correct questions would be correct")
        print(".....maximizes possible points by betting 100% accurately")
        print(".....returns difference between optimum and actual")
        print("\n")
        print("Notes".center(80, '_'))
        print("*Weeks are NOT 0 indexed")
        print("\n")
        
        
        
#t = Trivia([1,2,3,4,5])
#weeks = [1, 2, 3, 4, 5]
#teams = {}
#overall ={}
#colors = pd.read_csv('Teams.csv')
#for week in weeks:
#    week_tms = {}
#    df = pd.read_csv(f'Week_{week}/Regulation.csv')
#    df_f = pd.read_csv(f'Week_{week}/Final.csv')
#    df_h = pd.read_csv(f'Week_{week}/Halftime.csv')
#    df_q = pd.read_csv(f'Week_{week}/Quarter.csv')
#    with open(f'Week_{week}/Categories.csv') as cats_file:
#        read_data = cats_file.read()
#    cats = [x.strip() for x in str(read_data).split(',')]
#    week_teams = df.Team.unique().tolist()
#    for team in week_teams:
#        team_color = colors.loc[colors.Team == team].Color.values[0].split(',')
#        color = f'hsla({team_color[0]}, {team_color[1]}, {str(int(team_color[2])-5*(week-1))},1)'
#        tm = Trivia_Team(team, df.loc[df.Team == team],
#         df_f.loc[df_f.Team == team],
#         df_h.loc[df_h.Team == team],
#         df_q.loc[df_q.Team == team],
#         cats, week, color)
#        if not team in teams.keys():
#            teams[team] = [[week, tm]]
#        else:
#            teams[team].append([week, tm])
#        week_tms[team] = tm
#    max_score = max([week_tms[t].final_score for t in week_teams])
#    for team in week_teams:
#        week_tms[team].Season_Points = week_tms[team].final_score/max_score*100
#    overall[week] = Overall(list(week_tms.values()))
#    
#
#season_teams = {}
#
#for team in teams:
#    games = [x[1] for x in teams[team]]
#    season_teams[team] = Season_Team(games)
#season_overall = Season_Total(list(overall.values()))
#cats_df = pd.DataFrame(season_overall.cats_score, index = ['Answered_Correctly', 'Answered', 'Points_Earned', 'Points_Wagered']).T
#cats_df['Answered_Percent'] = cats_df['Answered_Correctly']/cats_df['Answered']*100
#cats_df['Points_Percent'] = cats_df['Points_Earned']/cats_df['Points_Wagered']*100
#season_standings = {t:season_teams[t].Season_Points for t in season_teams.keys()}
#season_df = pd.DataFrame(season_standings)
#season_df.index = [f'Week_{i+1}' for i in range(10)]
#season_df = season_df.T
#season_df['Total'] = season_df.apply(lambda x: sum(sorted(x, reverse=True)[:5]), axis = 1)
#season_df.sort_values('Total', inplace=True, ascending=False)
#for team in colors.Team.tolist():
#    a = season_teams[team].cats_df.merge(cats_df, left_index=True, right_index=True, suffixes=['_Team', '_Total'])
#    a.sort_index(inplace=True, ascending = False)
#    data = []
#    butter_color_template = colors.loc[colors.Team == team].Color.values[0].split(',')
#    butter_color = f'hsl({butter_color_template[0]},{butter_color_template[1]},{butter_color_template[2]})'
#    a['team_text'] = a.apply(lambda x: f'Correct: {int(x.Answered_Correctly_Team)}/{int(x.Answered_Team)} <br>Points: {x.Points_Earned_Team}/{x.Points_Wagered_Team}', axis =1)
#    a['total_text'] = a.apply(lambda x: f'Correct: {int(x.Answered_Correctly_Total)}/{int(x.Answered_Total)} <br>Points: {x.Points_Earned_Total}/{x.Points_Wagered_Total}', axis =1)
#    data.append(go.Bar(name = team, y=[i for i in range(len(a.Answered_Percent_Team))],x=a.Answered_Percent_Team, orientation = 'h', marker_color = butter_color, hovertext = a.team_text, hoverinfo = 'text', text = [f'{x:.0f}%' for x in a.Answered_Percent_Team], textposition = 'auto'))
#    data.append(go.Bar(name = 'Total', y=[i for i in range(len(a.Answered_Percent_Team))],x=a.Answered_Percent_Total, orientation = 'h', xaxis = 'x2', yaxis = 'y2', marker_color = 'darkgrey',hovertext = a.total_text, hoverinfo = 'text', text = [f'{x:.0f}%' for x in a.Answered_Percent_Total], textposition = 'auto'))
#    data.append(go.Scatter(x = [1 for i in range(len(a.Points_Percent_Team))], y = [i for i in range(len(a.Points_Percent_Team))], orientation = 'h', mode = 'text', text = list(a.index),xaxis = 'x3', yaxis = 'y3', hoverinfo = None, showlegend=False))
#    fig = go.Figure(data = data, layout = go.Layout())
#    fig.update_layout(
#        xaxis=dict(
#            domain=[0, 0.47],
#            range = [102,0],
#        ),
#        yaxis=dict(
#            range = [-2,20],
#            visible = False
#        ),
#        xaxis2=dict(
#            domain = [0.53, 1],
#            range = [0,102],
#        ),
#        xaxis3=dict(
#            domain = [0.47, 0.53],
#            visible = False
#        ),
#        yaxis2 = dict(range = [-2,20],
#                      visible = False),
#        yaxis3 = dict(range = [-2,20],
#                      visible = False)
#    )
#    season_teams[team].Butterfly = fig


    
#plot(season_teams['Skinny Legends'].weekly_plots)
#plot(season_teams['Skinny Legends'].weekly_clean)
#plot(season_overall.total_plot)
#plot(overall[1].total_plot)
#plot(teams['Skinny Legends'][3][1].running_plot)
#plot(season_teams['Skinny Legends'].Butterfly)

