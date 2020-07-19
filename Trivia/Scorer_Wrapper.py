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
            Scorer.standings, Scorer.four_q, Scorer.quarter_bonus, Scorer.final_qs, Scorer.teams, Scorer.no_teams, Scorer.repo, Scorer.html_temp = Scorer.setup()
            Scorer.files = [r'/home/andrew/Documents/aefreeman.github.io/Trivia/Live_Tracker.html',
                           r'/home/andrew/Documents/aefreeman.github.io/Trivia/img/fig1.png']
            Scorer.scores = [[0] for team in Scorer.teams]
            Scorer.counter = 2
            questions = [['Quarter', i//4+1,i%4+1] for i in range(16)]
            bonuses = [4,9,14]
            for q in bonuses:
                questions.insert(q, ['Bonus',q//5+1,1])
            questions.extend([['Final',1,1],['Final',1,2]])
            Scorer.questions = questions
            quest_order = iter(questions)
            print('Setup')
        else:
            Scorer.update(TYPE, QTR, QUESTION)
            Scorer.counter += 1
        print("Press enter when ready for the next question. Ctrl-c to kill")
        sys.stdin.readline()
        TYPE, QTR, QUESTION = next(quest_order)
        QTR = int(QTR)
        QUESTION = int(QUESTION)
        reload(Scorer)
