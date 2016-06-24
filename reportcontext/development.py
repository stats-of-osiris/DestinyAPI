# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:28:09 2016

@author: montgomeryj
"""

import pandas as pd

#dfSample = dfStats.loc[(dfStats['Team Name'] == 'Alpha') & (dfStats['Player Name'] == 'JohnOfMars'), 'Player Name']

dfWeaps = pd.read_csv('dfWeaps.csv')

dfJohnWeaps = dfWeaps.loc[(dfWeaps['player'] == 'JohnOfMars')]
                
                