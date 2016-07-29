# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:02:11 2016

@author: johnofmars
"""

import time
import pandas as pd
from datetime import datetime
import numpy as np
import re
import destiny
import math

titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009215820974)

game_report = pd.DataFrame(titan_report.report_games())

team_report = pd.DataFrame(titan_report.report_teams())


teammate_report = pd.DataFrame(
    titan_report.report_my_team()
).set_index('user_name')

teammate_report['contribution'] = teammate_report.score / sum(teammate_report.score)*100

#file_name = datetime.strptime(game_report.iloc[0]['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') + re.sub('[^A-Za-z0-9]+', '', game_report.iloc[0]['map_name']) + 'ReptCard.md'
file_name = 'report_card.txt'

#---------------HEADER----------------------

header = """---
layout: post
title: Passage Report Card for {Title}
excerpt: "{Excerpt}"
modified: {Date}
categories: articles
tags: [pvp,trials,data,report_card]
image:
  feature: header.png
comments: true
share: true
---
"""

header_context = {
 "Title":game_report.iloc[0]['map_name'],
 "Excerpt":"First Python-generated Report Card",
# "Date": now.strftime("%Y-%m-%d")
 "Date": datetime.now().date()
 } 
 
with  open(file_name,'w') as myfile:
    myfile.write(header.format(**header_context))

#---------------TEAM SUMMARY-----------

summary = """

### Team Summary

1. **{Player1}** - The "Player1_class"
2. **{Player2}** - The "Player2_class"
3. **{Player3}** - The "Player3_class"

"""

summary_context = {
 "Map":         game_report.iloc[0]['map_name'],
 "Player1":teammate_report.index.values[0],
# "Player1_class":teammate_report.iloc[0]['pclass'],
 "Player2":teammate_report.index.values[1],
# "Player2_class":teammate_report.iloc[1]['pclass'],
 "Player3":teammate_report.index.values[2],
# "Player3_class":teammate_report.iloc[2]['pclass'],
 } 
 
with  open(file_name,'a') as myfile:
    myfile.write(summary.format(**summary_context))
    
#---------------TEAM PERFORMANCE-----------

teamperf = """
### Overall Team Performance

![](https://www.bungie.net{map_path})

Playing for **{Time}** minutes on **{Date}**.

Spawn Side: {alpha_count} times **Alpha**, {bravo_count} times **Bravo**


![]({game_graph_path})

- Team K/D of {teamkd}, with a sweaty[^1] K/D of "teamskd"
- Average round time of {round_time} seconds, or "round_stime" seconds when sweaty[^1]
- {N_1stk} out of {N_games} matches we had First Blood
- {N_aces} Aces vs {N_aced} times Aced
- {N_annil} Annihilations vs {N_annild} times Annihilated
- {N_rez} Resurrections vs {N_enemy_rez} Enemy Resurrections Allowed
- {N_morbs} Orbs Missed out of {N_orbs} generated

#### The Team's Kill Methods:
![]({killm_graph_path})

"""

teamperf_context = {
 "map_path":    game_report.iloc[0]['map_image'],
 "Time":        "%.1f" % (game_report['play_time'].sum() / 60),
 "Date":        game_report.iloc[0]['date'],
 "alpha_count":     len(game_report[game_report['team'] == 'Alpha']),
 "bravo_count":     len(game_report[game_report['team'] == 'Bravo']),
 "game_graph_path":     "round_scores.png",
 "killm_graph_path":    "weapon_method.png",
# "teamskd":      "%.2f" % (team_report.iloc[0]['sweaty_k'] / team_report.iloc[0]['sweaty_d']),
 "teamkd":      "%.2f" % team_report[team_report['allegiance'] == 'us']['kd_ratio'].mean(),
 "round_time":         "%.1f" % (np.mean(game_report.avg_round_time)),
# "round_stime":        "%.1f" % (np.mean(game_report.sweaty_round_time)),
 "N_1stk":      int(team_report[team_report['allegiance'] == 'us']['medals_first_blood'].sum()),
 "N_games":     len(game_report),
 "N_aces":      int(math.ceil(team_report[team_report['allegiance'] == 'us']['medals_ace'].sum()/3)),
 "N_aced":      int(math.ceil(team_report[team_report['allegiance'] == 'them']['medals_ace'].sum()/3)),
 "N_annil":     int(math.ceil(team_report[team_report['allegiance'] == 'us']['medals_annihilation'].sum()/3)),
 "N_annild":    int(math.ceil(team_report[team_report['allegiance'] == 'them']['medals_annihilation'].sum()/3)),
 "N_rez":       int(team_report[team_report['allegiance'] == 'us']['rez_count'].sum()),
 "N_enemy_rez": int(team_report[team_report['allegiance'] == 'them']['rez_count'].sum()),
 "N_morbs":     int(team_report[team_report['allegiance'] == 'us']['orbs_dropped'].sum()-team_report[team_report['allegiance'] == 'us']['orbs_gathered'].sum()),
 "N_orbs":      int(team_report[team_report['allegiance'] == 'us']['orbs_dropped'].sum()),
 }

with  open(file_name,'a') as myfile:
    myfile.write(teamperf.format(**teamperf_context))

#---------------INDIV PERFORMANCE-----------

indiv = """

### Detailed Individual Performance

| #                      	| {Player1} 	| {Player2} 	| {Player3} 	|
|:--------|--------:|--------:|--------:|
| Kills                  	| {p1k}     	| {p2k}     	| {p3k}     	|
| Assists                	| {p1a}     	| {p2a}     	| {p3a}     	|
| Deaths                 	| {p1d}     	| {p2d}     	| {p3d}     	|
| K/D                    	| {p1kd}    	| {p2kd}    	| {p3kd}    	|
| Sweaty K/D[^1]             	| p1skd   	| p2skd   	| p3skd    	|
| Percent Contribution[^2]  	| {p1cont} %  	| {p2cont} %    	| {p3cont} %    	|
| Last Guardian Actions[^3]   | {p1lga}   	| {p2lga}   	| {p3lga}   	|
| Wrecking Balls         	| {p1wb}    	| {p2wb}    	| {p3wb}    	|
| Longest Kill Streak    	| {p1mks}   	| {p2mks}   	| {p3mks}   	|
| Longest Life           	| {p1ll}    	| {p2ll}    	| {p3ll}    	|
| Close Calls            	| {p1cc}    	| {p2cc}    	| {p3cc}    	|
{format_code}

"""

indiv_context = {
    "Player1":teammate_report.index.values[0],

    "p1k":	"%.0f" % 	(teammate_report.iloc[0]['kills_total']),
    "p1a":	"%.0f" % 	(teammate_report.iloc[0]['assists']),
    "p1d":	"%.0f" % 	(teammate_report.iloc[0]['deaths']),
    "p1kd":	"%.2f" % 	(teammate_report.iloc[0]['kd_ratio']),
#    "p1skd":	"%.2f" % 	(teammate_report.iloc[0]['sweaty_k'] / teammate_report.iloc[0]['sweaty_d']),
    "p1cont":	"%.1f" % 	(teammate_report.iloc[0]['contribution']),
    "p1lga":	"%.0f" % 	(teammate_report.iloc[0]['medals_from_the_brink'] + teammate_report.iloc[0]['medals_never_say_die']),
    "p1wb":	"%.0f" % 	(teammate_report.iloc[0]['medals_wrecking_ball']),
    "p1mks":	"%.0f" % 	(teammate_report.iloc[0]['longest_kill_spree']),
    "p1ll":	"%.0f" % 	(teammate_report.iloc[0]['longest_life']),
    "p1cc":	"%.0f" % 	(teammate_report.iloc[0]['medals_close_call']),

    "Player2":teammate_report.index.values[1],

    "p2k":	"%.0f" % 	(teammate_report.iloc[1]['kills_total']),
    "p2a":	"%.0f" % 	(teammate_report.iloc[1]['assists']),
    "p2d":	"%.0f" % 	(teammate_report.iloc[1]['deaths']),
    "p2kd":	"%.2f" % 	(teammate_report.iloc[1]['kd_ratio']),
#    "p2skd":	"%.2f" % 	(teammate_report.iloc[1]['sweaty_k'] / teammate_report.iloc[1]['sweaty_d']),
    "p2cont":	"%.1f" % 	(teammate_report.iloc[1]['contribution']),
    "p2lga":	"%.0f" % 	(teammate_report.iloc[1]['medals_from_the_brink'] + teammate_report.iloc[1]['medals_never_say_die']),
    "p2wb":	"%.0f" % 	(teammate_report.iloc[1]['medals_wrecking_ball']),
    "p2mks":	"%.0f" % 	(teammate_report.iloc[1]['longest_kill_spree']),
    "p2ll":	"%.0f" % 	(teammate_report.iloc[1]['longest_life']),
    "p2cc":	"%.0f" % 	(teammate_report.iloc[1]['medals_close_call']),

    "Player3":teammate_report.index.values[2],

    "p3k":	"%.0f" % 	(teammate_report.iloc[2]['kills_total']),
    "p3a":	"%.0f" % 	(teammate_report.iloc[2]['assists']),
    "p3d":	"%.0f" % 	(teammate_report.iloc[2]['deaths']),
    "p3kd":	"%.2f" % 	(teammate_report.iloc[2]['kd_ratio']),
#    "p3skd":	"%.2f" % 	(teammate_report.iloc[2]['sweaty_k'] / teammate_report.iloc[2]['sweaty_d']),
    "p3cont":	"%.1f" % 	(teammate_report.iloc[2]['contribution']),
    "p3lga":	"%.0f" % 	(teammate_report.iloc[2]['medals_from_the_brink'] + teammate_report.iloc[2]['medals_never_say_die']),
    "p3wb":	"%.0f" % 	(teammate_report.iloc[2]['medals_wrecking_ball']),
    "p3mks":	"%.0f" % 	(teammate_report.iloc[2]['longest_kill_spree']),
    "p3ll":	"%.0f" % 	(teammate_report.iloc[2]['longest_life']),
    "p3cc":	"%.0f" % 	(teammate_report.iloc[2]['medals_close_call']),

    "format_code": "{: .table)"
 }

with  open(file_name,'a') as myfile:
    myfile.write(indiv.format(**indiv_context))


indiv2 = """

| Kill Method Breakdown        	| {Player1}      	| {Player2}      	| {Player3}      	|
|:--------|--------:|--------:|--------:|
| % Primary vs Secondary     	| {p1pvs} %      	| {p2pvs} %      	| {p3pvs} %      	|
| Sniper Headshots / Kills   	| {p1shs}/{p1sk} 	| {p2shs}/{p2sk} 	| {p3shs}/{p3sk} 	|
| Shotgun Kills              	| {p1sg}         	| {p2sg}         	| {p3sg}         	|
| Other Special Weapon Kills 	| {p1os}         	| {p2os}         	| {p3os}         	|
| Heavy Weapon Kills         	| {p1hk}         	| {p2hk}         	| {p3hk}         	|
| Grenade Kills              	| {p1g}          	| {p2g}          	| {p3g}          	|
| Melee Kills                	| {p1m}          	| {p2m}          	| {p3m}          	|
| Super Kills                	| {p1s}          	| {p2s}          	| {p3s}          	|
{format_code}


| Resurrections & Orbs      	| {Player1}      	| {Player2}      	| {Player3}      	|
|:--------|--------:|--------:|--------:|
| Resurrections Performed    	| {p1rez}        	| {p2rez}        	| {p3rez}        	|
| Resurrections Received        	| {p1rezd}       	| {p2rezd}       	| {p3rezd}       	|
| Deaths Un-rezzed           	| {p1fail}       	| {p2fail}       	| {p3fail}       	|
| Orbs Generated             	| {p1ogen}       	| {p2ogen}       	| {p3ogen}       	|
| Orbs Gathered                	| {p1ogath}      	| {p2ogath}      	| {p3ogath}      	|
{format_code}

###### Definitions

[^1]:**Sweaty** stats are based on matches where the enemy team wins at least 3 rounds.

[^2]:
    **Percent contribution** is a metric for determining how much you helped or hindered your team. I started with the points that Destiny awards natively and tweaked them for Trials.

    - +100 for kills, -100 for deaths,

    - +33 for assists, +25 for rezzes, +12 for being rezzed.

    Scores are tabulated across all games for individuals and the team. And then a player's contribution is shown as percent of the team's total score.

[^3]:
    **Last Guardian Actions** are:

    - *'Never Say Die'* = Kill an enemy as the last guardian standing.

    - *'From the Brink'* = Revive a teammate as the last guardian standing.
"""

indiv_context2 = {
    "Player1":teammate_report.index.values[0],

    "p1pvs":	"%.1f" % 	(teammate_report.iloc[0]['kills_primary'] / (teammate_report.iloc[0]['kills_primary'] + teammate_report.iloc[0]['kills_special']) * 100),
    "p1shs":	"%.0f" % 	(teammate_report.iloc[0]['kills_prec_sniper']),
    "p1sk":	"%.0f" % 	(teammate_report.iloc[0]['kills_sniper']),
    "p1sg":	"%.0f" % 	(teammate_report.iloc[0]['kills_shotgun']),
    "p1os":	"%.0f" % 	(teammate_report.iloc[0]['kills_special'] - teammate_report.iloc[0]['kills_shotgun']-teammate_report.iloc[0]['kills_shotgun']),
    "p1hk":	"%.0f" % 	(teammate_report.iloc[0]['kills_heavy']),
    "p1g":	"%.0f" % 	(teammate_report.iloc[0]['kills_melee']),
    "p1m":	"%.0f" % 	(teammate_report.iloc[0]['kills_grenade']),
    "p1s":	"%.0f" % 	(teammate_report.iloc[0]['kills_super']),
    "p1rez":	"%.0f" % 	(teammate_report.iloc[0]['rez_count']),
    "p1rezd":	"%.0f" % 	(teammate_report.iloc[0]['rezzed_count']),
    "p1fail":	"%.0f" % 	(teammate_report.iloc[0]['deaths'] - teammate_report.iloc[0]['rezzed_count']),
    "p1ogen":	"%.0f" % 	(teammate_report.iloc[0]['orbs_dropped']),
    "p1ogath":	"%.0f" % 	(teammate_report.iloc[0]['orbs_gathered']),

    "Player2":teammate_report.index.values[1],

    "p2pvs":	"%.1f" % 	(teammate_report.iloc[1]['kills_primary'] / (teammate_report.iloc[1]['kills_primary'] + teammate_report.iloc[1]['kills_special']) * 100),
    "p2shs":	"%.0f" % 	(teammate_report.iloc[1]['kills_prec_sniper']),
    "p2sk": 	"%.0f" % 	(teammate_report.iloc[1]['kills_sniper']),
    "p2sg": 	"%.0f" % 	(teammate_report.iloc[1]['kills_shotgun']),
    "p2os": 	"%.0f" % 	(teammate_report.iloc[1]['kills_special'] - teammate_report.iloc[1]['kills_shotgun']-teammate_report.iloc[1]['kills_shotgun']),
    "p2hk": 	"%.0f" % 	(teammate_report.iloc[1]['kills_heavy']),
    "p2g":	      "%.0f" % 	(teammate_report.iloc[1]['kills_melee']),
    "p2m":	"%.0f" % 	(teammate_report.iloc[1]['kills_grenade']),
    "p2s":	"%.0f" % 	(teammate_report.iloc[1]['kills_super']),
    "p2rez":	"%.0f" % 	(teammate_report.iloc[1]['rez_count']),
    "p2rezd":	"%.0f" % 	(teammate_report.iloc[1]['rezzed_count']),
    "p2fail":	"%.0f" % 	(teammate_report.iloc[1]['deaths'] - teammate_report.iloc[1]['rezzed_count']),
    "p2ogen":	"%.0f" % 	(teammate_report.iloc[1]['orbs_dropped']),
    "p2ogath":	"%.0f" % 	(teammate_report.iloc[1]['orbs_gathered']),

    "Player3":teammate_report.index.values[2],

    "p3pvs":	"%.1f" % 	(teammate_report.iloc[2]['kills_primary'] / (teammate_report.iloc[2]['kills_primary'] + teammate_report.iloc[2]['kills_special']) * 100),
    "p3shs":	"%.0f" % 	(teammate_report.iloc[2]['kills_prec_sniper']),
    "p3sk":	"%.0f" % 	(teammate_report.iloc[2]['kills_sniper']),
    "p3sg":	"%.0f" % 	(teammate_report.iloc[2]['kills_shotgun']),
    "p3os":	"%.0f" % 	(teammate_report.iloc[2]['kills_special'] - teammate_report.iloc[2]['kills_shotgun']-teammate_report.iloc[2]['kills_shotgun']),
    "p3hk":	"%.0f" % 	(teammate_report.iloc[2]['kills_heavy']),
    "p3g":	"%.0f" % 	(teammate_report.iloc[2]['kills_melee']),
    "p3m":	"%.0f" % 	(teammate_report.iloc[2]['kills_grenade']),
    "p3s":	"%.0f" % 	(teammate_report.iloc[2]['kills_super']),
    "p3rez":	"%.0f" % 	(teammate_report.iloc[2]['rez_count']),
    "p3rezd":	"%.0f" % 	(teammate_report.iloc[2]['rezzed_count']),
    "p3fail":	"%.0f" % 	(teammate_report.iloc[2]['deaths'] - teammate_report.iloc[2]['rezzed_count']),
    "p3ogen":	"%.0f" % 	(teammate_report.iloc[2]['orbs_dropped']),
    "p3ogath":	"%.0f" % 	(teammate_report.iloc[2]['orbs_gathered']),

    "format_code": "{: .table)"
 }

with  open(file_name,'a') as myfile:
    myfile.write(indiv2.format(**indiv_context2))