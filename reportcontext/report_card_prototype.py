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

Round Scores by Game
![](http://johnofmars.github.io/images/{game_graph_path})

- Team K/D of {teamkd}
- {N_1stk} out of {N_games} matches we had First Blood	
- {N_aces} Aces vs {N_aced} times Aced
- {N_annil} Annihilations vs {N_annild} times Annihilated
- {N_rez} Resurrections vs {N_enemy_rez} Enemy Resurrections Allowed
- {N_morbs} Orbs Missed out of {N_orbs} generated

Graph of Kill Method Distribtuion:
![](http://johnofmars.github.io/images/{killm_graph_path})

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

| #                      	| {Player1} 	| {Player2} 	| {Player3} 	|
|------------------------	|-----------	|-----------	|-----------	|
| Kills                  	| {p1k}     	| {p2k}     	| {p3k}     	|
| Assists                	| {p1a}     	| {p2a}     	| {p3a}     	|
| Deaths                 	| {p1d}     	| {p2d}     	| {p3d}     	|
| K/D                    	| {p1kd}    	| {p2kd}    	| {p3kd}    	|
| Sweaty K/D*             	| {p1skd}   	| {p2skd}   	| {p3kd}    	|
| Percent Contribution**  	| {p1cont}   	| {p2cont}   	| {p3cont}   	|
| Last Guardian Actions*** | {p1lga}   	| {p2lga}   	| {p3lga}   	|
| Wrecking Balls         	| {p1wb}    	| {p2wb}    	| {p3wb}    	|
| Longest Kill Streak    	| {p1mks}   	| {p2mks}   	| {p3mks}   	|
| Longest Life           	| {p1ll}    	| {p2ll}    	| {p3ll}    	|
| Close Calls            	| {p1cc}    	| {p2cc}    	| {p3cc}    	|


* Sweaty K/D is K/D on matches where the enemy team wins at least 3 rounds.

** Percent contribution is a metric for determining how much you helped or hindered your team.

+100 for kills
-100 for deaths
+33 for assists
+25 for rezzes
+12 for being rezzed

Scores are tabulated across all games for individuals and the team. And then a player's score is shown as percent of the team's total score.

***Last Guardian Actions are:

'Never Say Die' = Kill an enemy as the last guardian standing.
'From the Brink' = Revive a teammate as the last guardian standing.

"""

indiv_context = {
    "Player1":dfIndiv.iloc[0]['player'], 
     
    "p1k":	"%.0f" % 	(dfIndiv.iloc[0]['kills']),
    "p1a":	"%.0f" % 	(dfIndiv.iloc[0]['assists']),
    "p1d":	"%.0f" % 	(dfIndiv.iloc[0]['deaths']),
    "p1kd":	"%.2f" % 	(dfIndiv.iloc[0]['k_d']),
    "p1skd":	"%.2f" % 	(dfIndiv.iloc[0]['k_d']),
    "p1cont":	"%.1f" % 	(dfIndiv.iloc[0]['p_cont']),
    "p1lga":	"%.0f" % 	(dfIndiv.iloc[0]['from_the_brink']+dfIndiv.iloc[0]['never_say_die']),
    "p1wb":	"%.0f" % 	(dfIndiv.iloc[0]['wrecking_ball']),
    "p1mks":	"%.0f" % 	(dfIndiv.iloc[0]['max_k_spree']),
    "p1ll":	"%.0f" % 	(dfIndiv.iloc[0]['long_life']),
    "p1cc":	"%.0f" % 	(dfIndiv.iloc[0]['close_call']),
 
    "Player2":dfIndiv.iloc[1]['player'], 
    
    "p2k":	"%.0f" % 	(dfIndiv.iloc[1]['kills']),
    "p2a":	"%.0f" % 	(dfIndiv.iloc[1]['assists']),
    "p2d":	"%.0f" % 	(dfIndiv.iloc[1]['deaths']),
    "p2kd":	"%.2f" % 	(dfIndiv.iloc[1]['k_d']),
    "p2skd":	"%.2f" % 	(dfIndiv.iloc[1]['k_d']),
    "p2cont":	"%.1f" % 	(dfIndiv.iloc[1]['p_cont']),
    "p2lga":	"%.0f" % 	(dfIndiv.iloc[1]['from_the_brink']+dfIndiv.iloc[1]['never_say_die']),
    "p2wb":	"%.0f" % 	(dfIndiv.iloc[1]['wrecking_ball']),
    "p2mks":	"%.0f" % 	(dfIndiv.iloc[1]['max_k_spree']),
    "p2ll":	"%.0f" % 	(dfIndiv.iloc[1]['long_life']),
    "p2cc":	"%.0f" % 	(dfIndiv.iloc[1]['close_call']),

    "Player3":dfIndiv.iloc[2]['player'],
    
    "p3k":	"%.0f" % 	(dfIndiv.iloc[2]['kills']),
    "p3a":	"%.0f" % 	(dfIndiv.iloc[2]['assists']),
    "p3d":	"%.0f" % 	(dfIndiv.iloc[2]['deaths']),
    "p3kd":	"%.2f" % 	(dfIndiv.iloc[2]['k_d']),
    "p3skd":	"%.2f" % 	(dfIndiv.iloc[2]['k_d']),
    "p3cont":	"%.1f" % 	(dfIndiv.iloc[2]['p_cont']),
    "p3lga":	"%.0f" % 	(dfIndiv.iloc[2]['from_the_brink']+dfIndiv.iloc[2]['never_say_die']),
    "p3wb":	"%.0f" % 	(dfIndiv.iloc[2]['wrecking_ball']),
    "p3mks":	"%.0f" % 	(dfIndiv.iloc[2]['max_k_spree']),
    "p3ll":	"%.0f" % 	(dfIndiv.iloc[2]['long_life']),
    "p3cc":	"%.0f" % 	(dfIndiv.iloc[2]['close_call'])
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(indiv.format(**indiv_context))
    
indiv2 = """

| Kill Method Breakdown        	| {Player1}      	| {Player2}      	| {Player3}      	|
|----------------------------	|----------------	|----------------	|----------------	|
| % Primary vs Secondary     	| {p1pvs} %      	| {p2pvs} %      	| {p3pvs} %      	|
| Sniper Headshots / Kills   	| {p1shs}/{p1sk} 	| {p2shs}/{p2sk} 	| {p3shs}/{p3sk} 	|
| Shotgun Kills              	| {p1sg}         	| {p2sg}         	| {p3sg}         	|
| Other Special Weapon Kills 	| {p1os}         	| {p2os}         	| {p3os}         	|
| Heavy Weapon Kills         	| {p1hk}         	| {p2hk}         	| {p3hk}         	|
| Grenade Kills              	| {p1g}          	| {p2g}          	| {p3g}          	|
| Melee Kills                	| {p1m}          	| {p2m}          	| {p3m}          	|
| Super Kills                	| {p1s}          	| {p2s}          	| {p3s}          	|

| Resurrections & Orbs      	| {Player1}      	| {Player2}      	| {Player3}      	|
|----------------------------	|----------------	|----------------	|----------------	|
| Resurrections Performed    	| {p1rez}        	| {p2rez}        	| {p3rez}        	|
| Deaths Un-rezzed           	| {p1fail}       	| {p2fail}       	| {p3fail}       	|
| Orbs Generated             	| {p1ogen}       	| {p2ogen}       	| {p3ogen}       	|
| Orbs Missed                	| {p1ogath}      	| {p2ogath}      	| {p3ogath}      	|
"""

indiv_context2 = {
    "Player1":dfIndiv.iloc[0]['player'], 

    "p1pvs":	"%.0f" % 	(dfIndiv.iloc[0]['n_primary']/(dfIndiv.iloc[0]['n_primary']+dfIndiv.iloc[0]['n_special'])*100),
    "p1shs":	"%.0f" % 	(dfIndiv.iloc[0]['sniper_hshots']),
    "p1sk":	"%.0f" % 	(dfIndiv.iloc[0]['sniper_kills']),
    "p1sg":	"%.0f" % 	(dfIndiv.iloc[0]['shotg_kills']),
    "p1os":	"%.0f" % 	(dfIndiv.iloc[0]['fr_kills']+dfIndiv.iloc[0]['side_kills']),
    "p1hk":	"%.0f" % 	(dfIndiv.iloc[0]['rocket_kills']+dfIndiv.iloc[0]['hmg_kills']),
    "p1g":	"%.0f" % 	(dfIndiv.iloc[0]['melees']),
    "p1m":	"%.0f" % 	(dfIndiv.iloc[0]['grenades']),
    "p1s":	"%.0f" % 	(dfIndiv.iloc[0]['supers']),
    "p1rez":	"%.0f" % 	(dfIndiv.iloc[0]['rezzes']),
    "p1fail":	"%.0f" % 	(dfIndiv.iloc[0]['deaths']-dfIndiv.iloc[2]['rezzes']),
    "p1ogen":	"%.0f" % 	(dfIndiv.iloc[0]['orbs_gen']),
    "p1ogath":	"%.0f" % 	(dfIndiv.iloc[0]['orbs_gath']),
 
    "Player2":dfIndiv.iloc[1]['player'], 

    "p2pvs":	"%.0f" % 	(dfIndiv.iloc[1]['n_primary']/(dfIndiv.iloc[1]['n_primary']+dfIndiv.iloc[1]['n_special'])*100),
    "p2shs":	"%.0f" % 	(dfIndiv.iloc[1]['sniper_hshots']),
    "p2sk":	"%.0f" % 	(dfIndiv.iloc[1]['sniper_kills']),
    "p2sg":	"%.0f" % 	(dfIndiv.iloc[1]['shotg_kills']),
    "p2os":	"%.0f" % 	(dfIndiv.iloc[1]['fr_kills']+dfIndiv.iloc[1]['side_kills']),
    "p2hk":	"%.0f" % 	(dfIndiv.iloc[1]['rocket_kills']+dfIndiv.iloc[1]['hmg_kills']),
    "p2g":	"%.0f" % 	(dfIndiv.iloc[1]['melees']),
    "p2m":	"%.0f" % 	(dfIndiv.iloc[1]['grenades']),
    "p2s":	"%.0f" % 	(dfIndiv.iloc[1]['supers']),
    "p2rez":	"%.0f" % 	(dfIndiv.iloc[1]['rezzes']),
    "p2fail":	"%.0f" % 	(dfIndiv.iloc[1]['deaths']-dfIndiv.iloc[2]['rezzes']),
    "p2ogen":	"%.0f" % 	(dfIndiv.iloc[1]['orbs_gen']),
    "p2ogath":	"%.0f" % 	(dfIndiv.iloc[1]['orbs_gath']),

    "Player3":dfIndiv.iloc[2]['player'],

    "p3pvs":	"%.1f" % 	(dfIndiv.iloc[2]['n_primary']/(dfIndiv.iloc[2]['n_primary']+dfIndiv.iloc[2]['n_special'])*100),
    "p3shs":	"%.0f" % 	(dfIndiv.iloc[2]['sniper_hshots']),
    "p3sk":	"%.0f" % 	(dfIndiv.iloc[2]['sniper_kills']),
    "p3sg":	"%.0f" % 	(dfIndiv.iloc[2]['shotg_kills']),
    "p3os":	"%.0f" % 	(dfIndiv.iloc[2]['fr_kills']+dfIndiv.iloc[2]['side_kills']),
    "p3hk":	"%.0f" % 	(dfIndiv.iloc[2]['rocket_kills']+dfIndiv.iloc[2]['hmg_kills']),
    "p3g":	"%.0f" % 	(dfIndiv.iloc[2]['melees']),
    "p3m":	"%.0f" % 	(dfIndiv.iloc[2]['grenades']),
    "p3s":	"%.0f" % 	(dfIndiv.iloc[2]['supers']),
    "p3rez":	"%.0f" % 	(dfIndiv.iloc[2]['rezzes']),
    "p3fail":	"%.0f" % 	(dfIndiv.iloc[2]['deaths']-dfIndiv.iloc[2]['rezzes']),
    "p3ogen":	"%.0f" % 	(dfIndiv.iloc[2]['orbs_gen']),
    "p3ogath":	"%.0f" % 	(dfIndiv.iloc[2]['orbs_gath'])

 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(indiv2.format(**indiv_context2))