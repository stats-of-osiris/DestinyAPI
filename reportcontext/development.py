# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:28:09 2016

@author: montgomeryj
"""

import pandas as pd

#dfSample = dfStats.loc[(dfStats['Team Name'] == 'Alpha') & (dfStats['Player Name'] == 'JohnOfMars'), 'Player Name']

dfStats = pd.read_csv('DestinyStats.csv')
dfGames = pd.read_csv('dfGames.csv')

dfGames['sweaty'] = 'no'
dfGames['sweaty_round_time'] = 'NaN'

for x in dfGames.index:
    dfGames.loc[x,'round_time'] =  dfGames.loc[x,'play_time']/(dfGames.loc[x,'score']+dfGames.loc[x,'enemy_score'])
    
    if dfGames.loc[x,'enemy_score'] >= 3:
        dfGames.loc[x,'sweaty'] = 'yes'
        dfGames.loc[x,'sweaty_round_time'] =  dfGames.loc[x,'play_time']/(dfGames.loc[x,'score']+dfGames.loc[x,'enemy_score'])

dfStats['sweaty_k'] = 0

for x in dfGames.index:
    for y in dfStats.index:
        if dfGames.ix[x]['game_N'] == dfStats.ix[y]['game_N']:
            
#            print dfStats.ix[y]['game_N'], dfGames.ix[x]['sweaty']
            
            if dfGames.ix[x]['sweaty'] == 'yes':
                
                print y, dfStats.ix[y]['kills']
                
                dfStats.ix[y]['sweaty_k'] = dfStats.ix[y]['kills']
                
                print y, dfStats.ix[y]['sweaty_k']
                
                