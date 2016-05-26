# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:02:11 2016

@author: johnofmars
"""

import time

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
 "Player1":'Player 1', 
 "Player1_weapon":"Weapon",
 "Player1_class":"Character Class",
 "Player2":'Player 2', 
 "Player2_weapon":"Weapon",
 "Player2_class":"Character Class",
 "Player3":'Player 3', 
 "Player3_weapon":"Weapon",
 "Player3_class":"Character Class",
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(summary.format(**summary_context))
    
#---------------TEAM PERFORMANCE-----------

teamperf = """
###Overall Team Performance

Playing on {Map} for {Time}
	
Round Scores by Game
![](http://johnofmars.github.io/images/{graph_path})
	
- {N_aces} Aces
- {N_annil} Annilations
- {N_rez} Rezzes Allowed
- {N_orbs} Orbs Missed

"""

teamperf_context = {
 "Map":"Map",
 "Time":"Time",
 "graph_path":"headers/trials2.jpg",
 "N_aces":"N",
 "N_annil":"N",
 "N_rez":"N",
 "N_orbs":"N",
 } 
 
with  open('report_card.txt','a') as myfile:
    myfile.write(teamperf.format(**teamperf_context))

#---------------INDIV PERFORMANCE-----------

indiv = """

###Individual Detailed Performance

| Stat                       | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| Kills                      |           |           |           |
| Assists                    |           |           |           |
| Deaths                     |           |           |           |
| K/D                        |           |           |           |
| % Contribution             |           |           |           |
| Score Contribution         |           |           |           |


| Stat                       | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| % Primary vs Secondary     |           |           |           |
| # of Last Guardian Actions |           |           |           |
| # of Wrecking Balls        |           |           |           |
| Longest Kill Streak        |           |           |           |
| Longest Life               |           |           |           |

| Stat                       | {Player1} | {Player2} | {Player3} |
|----------------------------|-----------|-----------|-----------|
| Rezzes                     |           |           |           |
| Rezzed                     |           |           |           |
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