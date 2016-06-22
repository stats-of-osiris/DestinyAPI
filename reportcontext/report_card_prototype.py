# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:02:11 2016

@author: johnofmars
"""

import time
import pandas as pd

dfStats = pd.read_csv('DestinyStats.csv')

dfTeams = pd.read_csv('dfTeams.csv')
dfGames = pd.read_csv('dfGames.csv')
dfIndiv = pd.read_csv('dfIndiv.csv')

#dfTeams.set_index('alleg', inplace=True)

#---------------HEADER----------------------

header = """---
layout: post
title: {Title}
excerpt: "{Excerpt}"
modified: {Date}
categories: articles
tags: [pvp,trials,data]
image:
  feature: header.png
comments: true
share: true
---
"""

header_context = {
 "Title":'Report Card', 
 "Excerpt":"Test",
 "Date":time.strftime("%Y-%m-%d")
 } 
 
with  open('report_card.txt','w') as myfile:
    myfile.write(header.format(**header_context))

#---------------TEAM SUMMARY-----------

summary = """
##Trials Report Card

###Team Summary

1. {Player1} - The {Player1_weapon}-wielding {Player1_class}
2. {Player2} - The {Player2_weapon}-wielding {Player2_class}
3. {Player3} - The {Player3_weapon}-wielding {Player3_class}

"""

summary_context = {
 "Player1":dfIndiv.iloc[0]['player'], 
 "Player1_weapon":dfIndiv.iloc[0]['best_weap'],
 "Player1_class":dfIndiv.iloc[0]['pclass'],
 "Player2":dfIndiv.iloc[1]['player'], 
 "Player2_weapon":dfIndiv.iloc[1]['best_weap'],
 "Player2_class":dfIndiv.iloc[1]['pclass'],
 "Player3":dfIndiv.iloc[2]['player'], 
 "Player3_weapon":dfIndiv.iloc[2]['best_weap'],
 "Player3_class":dfIndiv.iloc[2]['pclass'],
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(summary.format(**summary_context))
    
#---------------TEAM PERFORMANCE-----------

teamperf = """
### Overall Team Performance

![]({map_path})

Playing on {Map} for {Time} minutes

Spawn Side: % Alpha, % Bravo

Graph of Kill Method Distribtuion:
![](http://johnofmars.github.io/images/{killm_graph_path})
	
Round Scores by Game
![](http://johnofmars.github.io/images/{game_graph_path})

- Team K/D of {teamkd}
- {N_1stk} out of {N_games} matches we had First Blood	
- {N_aces} Aces vs {N_aced} times Aced
- {N_annil} Annihilations vs {N_annild} times Annihilated
- {N_rez} Resurrections vs {N_enemy_rez} Enemy Resurrections Allowed
- {N_morbs} Orbs Missed out of {N_orbs} generated

"""

teamperf_context = {
 "map_path":"https://www.bungie.net/img/theme/destiny/bgs/pgcrs/crucible_exodus_blue.jpg",
 "Map":"Map",
 "Time":"%.1f" % (dfIndiv.iloc[0]['play_time']/60),
 "killm_graph_path":"headers/trials2.jpg",
 "game_graph_path":"headers/trials2.jpg",
 "teamkd": "%.2f" % dfTeams.iloc[0]['k_d'],
 "N_1stk": int(dfTeams.iloc[0]['first_blood']),
 "N_games":len(dfGames),
 "N_aces":int(dfTeams.iloc[0]['ace']),
 "N_aced":int(dfTeams.iloc[1]['ace']),
 "N_annil":int(dfTeams.iloc[0]['annil']),
 "N_annild":int(dfTeams.iloc[1]['annil']),
 "N_rez":int(dfTeams.iloc[0]['rezzes']),
 "N_enemy_rez":int(dfTeams.iloc[1]['rezzes']),
 "N_morbs":int(dfTeams.iloc[0]['orbs_gen']-dfTeams.iloc[0]['orbs_gath']),
 "N_orbs":int(dfTeams.iloc[0]['orbs_gen']),
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(teamperf.format(**teamperf_context))
#
#---------------INDIV PERFORMANCE-----------

indiv = """

### Detailed Individual Performance

| General Summary            | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| Kills                      |           |           |           |
| Assists                    |           |           |           |
| Deaths                     |           |           |           |
| K/D                        |           |           |           |
| Sweaty K/D                 |           |           |           |
| % Contribution             |           |           |           |
| Last Guardian Actions*     |           |           |           |
| Wrecking Balls             |           |           |           |
| Longest Kill Streak        |           |           |           |
| Longest Life               |           |           |           |
| Close Calls                |           |           |           |

Last Guardian Actions are:

'Never Say Die' = Kill an enemy as the last guardian standing
'From the Brink' = Revive a teammate as the last guardian standing

| Kill Method Breakdown      | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| % Primary vs Secondary     |           |           |           |
| Sniper Headshots / Kills   |           |           |           |
| Shotgun Kills              |           |           |           |
| Other Special Weapon Kills |           |           |           |
| Heavy Weapon Kills         |           |           |           |
| Grenade Kills              |           |           |           |
| Melee Kills                |           |           |           |
| Super Kills                |           |           |           |

| Resurrections & Orbs       | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| Resurrections Performed    |           |           |           |
| Resurrection Received      |           |           |           |
| Deaths Un-Rezzed           |           |           |           |
| Orbs Generated             |           |           |           |
| Orbs Missed                |           |           |           |
"""

indiv_context = {
 "Player1":'Player 1', 
 "Player2":'Player 2', 
 "Player3":'Player 3'
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(indiv.format(**indiv_context))