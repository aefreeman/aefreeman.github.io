# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 16:46:47 2020

@author: Andrew
"""

import sys
import Scorer
from importlib import reload

TYPE = None
QTR = None
QUESTION = None
if __name__ == "__main__":
    while True:
        if not TYPE:
            Scorer.standings, Scorer.four_q, Scorer.quarter_bonus, Scorer.final_qs, Scorer.teams, Scorer.no_teams, Scorer.repo = Scorer.setup()
            Scorer.files = ['Trivia/Live_Tracker.html',
                           'Trivia/words.txt',
                           'Trivia/img/fig1.png']
            print('Setup')
        else:
            Scorer.update(TYPE, QTR, QUESTION)
        print("Enter TYPE, QTR, QUESTION, CTRL-C to exit. TYPE options: Quarter, Bonus, Final")
        TYPE, QTR, QUESTION = sys.stdin.readline().split(',')
        QTR = int(QTR)
        QUESTION = int(QUESTION)
        reload(Scorer)
