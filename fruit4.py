# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:07:32 2016

@author: montgomeryj
"""

import pandas as pd
from scipy.stats import mode


#gameID = ['5051903760']
dfStats = pd.DataFrame(columns=())
dfTeams = pd.DataFrame(columns=())
dfIndiv = pd.DataFrame(columns=())

dfStats = pd.read_csv('5051903760DestinyStats.csv')


# Generate Team List (need a function for this)
teammates = ['JohnOfMars','XpLiCiTOnE','igordennis']

# Assign Allegiences
dfStats['alleg'] = '?'

dfTeamFull = dfStats[dfStats['player'].isin(teammates)]

dfTeamFull.loc[:, 'alleg'] = 'us'

dfStats.set_index('Unnamed: 0', inplace=True)
dfTeamFull.set_index('Unnamed: 0', inplace=True)

dfStats.update(dfTeamFull)

dfStats = dfStats.replace('?','them')

#add rows
# sweaty k
# sweaty d

dfStats['n_primary'] = (dfStats.ar_kills + dfStats.hc_kills + dfStats.pr_kills + dfStats.scout_kills) #/ dfStats.kills
dfStats['n_special'] = (dfStats.sniper_kills + dfStats.shotg_kills + dfStats.fr_kills + dfStats.side_kills)
dfStats['n_heavy'] = (dfStats.rocket_kills + dfStats.hmg_kills)
dfStats['n_abil'] = (dfStats.melees + dfStats.grenades)
dfStats['n_supers'] = (dfStats.supers)

dfStats['points'] = dfStats.kills*100 + dfStats.deaths*-100 + dfStats.assists*33 + dfStats.rezzes*25 + dfStats.rezzed*12

# generate games list
game_stats = ['game_N','activity_id',' play_time','team','standing','score']

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

# Team Calcs---------------------------------------------------------------

teams_list = ['us','them']

for teams in teams_list:

    dfTeamFull = dfStats[dfStats['alleg'].isin([teams])]
      
    dfTeamFocus = dfTeamFull.sum(axis=0)
    
    dfTeamFocus['k_d'] = dfTeamFocus['kills']/dfTeamFocus['deaths']
    dfTeamFocus['alleg'] = mode(dfTeamFull.alleg)[0][0]
    # annil / 3 round up
    
    team_drop_rows = [
        'activity_id',
        'game_N',
        'standing',
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
    
    dfFocus['long_life'] = max(dfFocusFull.long_life)
    dfFocus['max_k_spree'] = max(dfFocusFull.max_k_spree)

    #'avg_life' : average
    #'avg_k_dist' : average
    
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
# % kill method