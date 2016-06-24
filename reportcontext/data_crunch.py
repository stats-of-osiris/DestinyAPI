# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:07:32 2016

@author: montgomeryj
"""

import pandas as pd
from scipy.stats import mode
import math
import numpy as np
import matplotlib.pyplot as plt
import collections


dfStats = pd.DataFrame(columns=())
dfTeams = pd.DataFrame(columns=())
dfIndiv = pd.DataFrame(columns=())

dfStats = pd.read_csv('DestinyStats.csv')


# Generate Team List (need a function for this)
teammates = ['JohnOfMars','DirtyAquaticApe','igordennis']
#teammates = ['JohnOfMars','XpLiCiTOnE','igordennis']

# Assign Allegiences
dfStats['alleg'] = '?'

dfTeamFull = dfStats[dfStats['player'].isin(teammates)]

dfTeamFull.loc[:, 'alleg'] = 'us'

dfStats.set_index('Unnamed: 0', inplace=True)
dfTeamFull.set_index('Unnamed: 0', inplace=True)

dfStats.update(dfTeamFull)

dfStats = dfStats.replace('?','them')

dfStats['n_primary'] = (dfStats.ar_kills + dfStats.hc_kills + dfStats.pr_kills + dfStats.scout_kills) #/ dfStats.kills
dfStats['n_special'] = (dfStats.sniper_kills + dfStats.shotg_kills + dfStats.fr_kills + dfStats.side_kills)
dfStats['n_heavy'] = (dfStats.rocket_kills + dfStats.hmg_kills)
dfStats['n_abil'] = (dfStats.melees + dfStats.grenades)
dfStats['n_supers'] = (dfStats.supers)

dfStats['points'] = dfStats.kills*100 + dfStats.deaths*-100 + dfStats.assists*33 + dfStats.rezzes*25 + dfStats.rezzed*12

# generate games list -------------------------------------------
game_stats = ['game_N','activity_id','date','play_time','team','standing','score', 'map_name', 'map_path']

dfGames = dfStats.loc[(dfStats['player'] == 'JohnOfMars'), game_stats]
dfGames.set_index('game_N', inplace=True)

# set score to 5 for victories
for x in dfGames.index:
    if dfGames.loc[x,'standing'] == 'Victory':
        dfGames.loc[x,'score'] = 5

# Find Enemy Scores for these games
dfSample = dfStats.loc[dfStats['alleg'] == 'them', game_stats]
dfSample.set_index('game_N', inplace=True)
dfSample = dfSample.iloc[range(0,len(dfSample),3)]

dfGames['enemy_score']=dfSample['score']

dfGames['sweaty'] = 'no'

for x in dfGames.index:
    dfGames.loc[x,'round_time'] =  dfGames.loc[x,'play_time']/(dfGames.loc[x,'score']+dfGames.loc[x,'enemy_score'])
    
    if dfGames.loc[x,'enemy_score'] >= 3:
        dfGames.loc[x,'sweaty'] = 'yes'
        dfGames.loc[x,'sweaty_round_time'] =  dfGames.loc[x,'play_time']/(dfGames.loc[x,'score']+dfGames.loc[x,'enemy_score'])

#dfStats['sweaty_k'] = 'NaN'

for x in dfGames.index:
    for y in dfStats.index:
        if dfGames.ix[x,'activity_id'] == dfStats.ix[y,'activity_id']:
      
            if dfGames.ix[x]['sweaty'] == 'yes':
             
                dfStats.ix[y,'sweaty_k']  = dfStats.ix[y,'kills']
                dfStats.ix[y,'sweaty_d']  = dfStats.ix[y,'deaths']

# Team Calcs---------------------------------------------------------------

teams_list = ['us','them']

for teams in teams_list:

    dfTeamFull = dfStats[dfStats['alleg'].isin([teams])]
      
    dfTeamFocus = dfTeamFull.sum(axis=0)
    
    dfTeamFocus['k_d'] = dfTeamFocus['kills']/dfTeamFocus['deaths']
    dfTeamFocus['alleg'] = mode(dfTeamFull.alleg)[0][0]
    dfTeamFocus['annil'] = math.ceil(dfTeamFocus.annil/3)
    # aces / 3 round up
    
    team_drop_rows = [
        'activity_id',
        'game_N',
        'standing',
        'best_weap',
        'team',
        'player',
        'score',
        'pclass',
        'ar_kills',
        'ar_hshots',
        'hc_kills',
        'hc_hshots',
        'pr_kills',
        'pr_hshots',
        'scout_kills',
        'scout_hshots',
        'sniper_kills',
        'sniper_hshots',
        'shotg_kills',
        'shotg_hshots',
        'fr_kills',
        'side_kills',
        'rocket_kills',
        'hmg_kills',
        'melees',
        'grenades',
        'supers']
    
    dfTeamFocus = dfTeamFocus.drop(team_drop_rows)
    dfTeamFocus = dfTeamFocus.to_frame()
    dfTeamFocus = dfTeamFocus.T
    
    dfTeams = dfTeams.append(dfTeamFocus)

# Individual Calcs------------------------------------------------------------
for player in teammates:
    dfFocusFull = dfStats[dfStats['player'].isin([player])]
    
    dfFocus = dfFocusFull.sum(axis=0)

    dfFocus['k_d'] = dfFocus.kills/dfFocus.deaths
    
    dfFocus['p_cont'] = (dfFocus.points/dfTeams.iloc[0]['points'])*100
    
    dfFocus['pclass'] = mode(dfFocusFull.pclass)[0][0]
    dfFocus['player'] = player
    dfFocus['best_weap'] = mode(dfFocusFull.best_weap)[0][0]
    dfFocus['alleg'] = mode(dfFocusFull.alleg)[0][0]
    dfFocus['date'] = mode(dfFocusFull.date)[0][0]
    dfFocus['map_name'] = mode(dfFocusFull.map_name)[0][0]
    
    dfFocus['map_common'] =  mode(dfGames.team)[1][0]   

    dfFocus['alpha'] = collections.Counter(a)['Alpha']
    dfFocus['bravo'] = collections.Counter(a)['Bravo']

    dfFocus['long_life'] = max(dfFocusFull.long_life)
    dfFocus['max_k_spree'] = max(dfFocusFull.max_k_spree)

    #'avg_life' : average
    #'avg_k_dist' : average
    # best weapon change from numeric to weapon class to loadout
   
    # add bravo spawn count
    # add alpha spawn count   
   
    indiv_drop_rows = [
        'activity_id',
        'game_N',
        'standing',
        'team', 
        'score']
    
    dfFocus = dfFocus.drop(indiv_drop_rows)
   
    dfFocus = dfFocus.to_frame()
    dfFocus = dfFocus.T
 
    dfIndiv = dfIndiv.append(dfFocus)
    

# Plotting here--------------------------------------------

# score by game

N = len(dfGames)
our_scores = dfGames['score']
their_scores = -1*dfGames['enemy_score']

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots(figsize=(10, 5))
rects1 = ax.bar(ind, our_scores, width, color='#3F73CE')
rects2 = ax.bar(ind, their_scores, width, color='#CE3F3F')

ax.set_title('Round Scores by Game')

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

#plt.savefig('round_scores.png', transparent=True)

# % kill method

prim = dfTeams.iloc[0]['n_primary']
spec = dfTeams.iloc[0]['n_special']
heavy = dfTeams.iloc[0]['n_heavy']
abil = dfTeams.iloc[0]['n_abil']
supers = dfTeams.iloc[0]['n_supers']

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

# Export to csv -------------------------------------------------------------
dfStats.to_csv('dfStats.csv', header=True, index=True)
dfTeams.to_csv('dfTeams.csv', header=True, index=True)
dfGames.to_csv('dfGames.csv', header=True, index=True)
dfIndiv.to_csv('dfIndiv.csv', header=True, index=True)