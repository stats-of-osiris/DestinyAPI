# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:07:32 2016

@author: montgomeryj
"""

import pandas as pd
import destiny
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re

titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009215820974)

game_report = pd.DataFrame(titan_report.report_games())
game_report = game_report[::-1]

team_report = pd.DataFrame(titan_report.report_teams())


# Plotting here--------------------------------------------

# # Setting file name
# file_name = datetime.strptime(dfGames.iloc[0]['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d')+re.sub('[^A-Za-z0-9]+', '', dfIndiv.iloc[0]['map_name'])

# score by game

N = len(game_report)
our_scores = game_report['score']
their_scores = -1 * game_report['enemy_score']

ind = np.arange(1,N+1,1)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots(figsize=(10, 5))
rects1 = ax.bar(ind, our_scores, width, color='#3F73CE')
rects2 = ax.bar(ind, their_scores, width, color='#CE3F3F')

ax.set_ylabel('Scores')
ax.set_yticks(range(-5,6,1))
ax.set_yticklabels(range(-5,6,1))

ax.set_xticks(ind + width/2)
ax.set_xticklabels(ind)

#ax.set_xlim([0,N])
#ax.set_ylim([-5,5])

ax.margins(0.05)

plt.axhline(y=0, color='k')

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend((rects1[0], rects2[0]), ('Us', 'Them'), loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=2)

#plt.show()

plt.savefig('round_scores.png', transparent=True)

# % kill method

prim = team_report.iloc[0]['kills_primary']
spec = team_report.iloc[0]['kills_special']
heavy = team_report.iloc[0]['kills_heavy']
abil = team_report.iloc[0]['kills_melee']+team_report.iloc[0]['kills_grenade']
supers = team_report.iloc[0]['kills_super']

total = prim+spec+heavy+abil+supers

prim = prim/total*100
spec = spec/total*100
heavy = heavy/total*100
abil = abil/total*100
supers = supers/total*100

rows = ['primary','special','heavy','abilities','supers']

fig, ax = plt.subplots(figsize=(10, 1))

height = .05

bar_locations = 1

ax.barh(bar_locations, prim, height, color='#B2B2B2')
ax.barh(bar_locations, spec, height, color='#72B96C', left=prim)
ax.barh(bar_locations, heavy, height, color='#896CB7', left =(spec+prim))
ax.barh(bar_locations, abil, height, color='#CE3F3F', left=(spec+prim+heavy))
ax.barh(bar_locations, supers, height, color='#3F73CE', left=(spec+prim+abil))

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.4,
                 box.width, box.height * 0.6])

# Put a legend below current axis
ax.legend(rows, loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=5)

ax.margins(0.05)

plt.axis('off')

#plt.show()

plt.savefig('weapon_method.png', transparent=True, bbox_inches='tight')
