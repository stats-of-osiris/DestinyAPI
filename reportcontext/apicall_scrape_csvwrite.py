# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:07:32 2016

@author: montgomeryj
"""

import requests
import json
import pandas as pd
from datetime import datetime

import sys
sys.path.append("..") # Adds higher directory to python modules path.
import destiny

head = {'X-API-Key':'071b767b1d014435b36264bf4f6234fc'}

#First Card
#gameID = ['3212367691','3212434371','3212472566','3212543938','3212576971','3212609456','3212639440','3212686179']

##Scarab Card
#gameID = ["4784376208","4784395782","4784423429","4784444986","4784478654","4784505400","4784538623","4784578379"]

#thwek
#gameID = ["5051903760"]

#Thwek card on Exodus Blue
#gameID = ['5051781495','5051794360','5051827975','5051825913','5051858771','5051885731','5051903760']

##Pantheon
#gameID = ['5100794481','5100843302','5100881734','5100910939','5100940484','5100970909','5101005646','5101033227','5101072353']

##Firebase Delphi
gameID = ['5187547715','5187635260','5187710298','5187514849','5187483457','5187332838','5187588401','5187432330','5187668011','5187466100','5187690866','5187653566','5187383024','5187411339']

dfStats = pd.DataFrame(columns=())
dfWeaps = pd.DataFrame(columns=())
dfAppend2 = pd.DataFrame(columns=('game','player','weap_hash','weap_kills')) 
 
keyStats = [
    # Player Performance
    {'value':        'kills',
     'column_name': 'kills',
     'team':        'both'},
    {'value':        'deaths',
     'column_name': 'deaths',
     'team':        'both'},
    {'value':        'resurrectionsPerformed',
     'column_name': 'rezzes',
     'team':        'both'},
    {'value':        'resurrectionsReceived',
     'column_name': 'rezzed',
     'team':        'us'},
    {'value':        'orbsDropped',
     'column_name': 'orbs_gen',
     'team':        'us'},
    {'value':        'orbsGathered',
     'column_name': 'orbs_gath',
     'team':        'us'},
    {'value':        'longestSingleLife',
     'column_name': 'long_life',
     'team':        'us'},
    {'value':        'averageLifespan',
     'column_name': 'avg_life',
     'team':        'us'},
    {'value':        'longestKillSpree', # broken
     'column_name': 'max_k_spree',
     'team':        'us'},
    # Weapon Use & Medals
    {'value':        'weaponBestType',
     'column_name': 'best_weap',
     'team':        'us'},
    {'value':        'averageKillDistance',
     'column_name': 'avg_k_dist',
     'team':        'us'},
    {'value':        'medalsFirstBlood',
     'column_name': 'first_blood',
     'team':        'us'},
    {'value':        'medalsEliminationLastStandKill',
     'column_name': 'never_say_die',
     'team':        'us'},
    {'value':        'medalsEliminationLastStandRevive',
     'column_name': 'from_the_brink',
     'team':        'us'},
    {'value':        'medalsComebackKill',
     'column_name': 'back_in_action',
     'team':        'us'},
    {'value':        'medalsEliminationWipeSolo',
     'column_name': 'wrecking_ball',
     'team':        'us'}, 
    {'value':        'medalsEliminationWipeQuick',
     'column_name': 'ace',
     'team':        'both'},
    {'value':        'medalsCloseCallTalent',
     'column_name': 'close_call',
     'team':        'us'},
    {'value':        'medalsActivityCompleteVictoryEliminationShutout',
     'column_name': 'annil',
     'team':        'us'},
    # Primaries
    {'value':        'weaponKillsAutoRifle',
     'column_name': 'ar_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsAutoRifle',
     'column_name': 'ar_hshots',
     'team':        'us'},
    {'value':        'weaponKillsHandCannon',
     'column_name': 'hc_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsHandCannon',
     'column_name': 'hc_hshots',
     'team':        'us'},
    {'value':        'weaponKillsPulseRifle',
     'column_name': 'pr_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsPulseRifle',
     'column_name': 'pr_hshots',
     'team':        'us'},
    {'value':        'weaponKillsScoutRifle',
     'column_name': 'scout_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsScoutRifle',
     'column_name': 'scout_hshots',
     'team':        'us'},
    # Secondaries
    {'value':        'weaponKillsSniper',
     'column_name': 'sniper_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsSniper',
     'column_name': 'sniper_hshots',
     'team':        'us'},
    {'value':        'weaponKillsShotgun',
     'column_name': 'shotg_kills',
     'team':        'us'},
    {'value':        'weaponPrecisionKillsShotgun',
     'column_name': 'shotg_hshots',
     'team':        'us'},
    {'value':        'weaponKillsFusionRifle',
     'column_name': 'fr_kills',
     'team':        'us'},
    {'value':        'weaponKillsSideArm', # need representative game
     'column_name': 'side_kills',
     'team':        'us'},
    # Heavy Weapons, Melees, Grenades, Supers
    {'value':        'weaponKillsRocketLauncher',
     'column_name': 'rocket_kills',
     'team':        'us'},
    {'value':        'weaponKillsMachineGun', # need representative game
     'column_name': 'hmg_kills',
     'team':        'us'},
    {'value':        'weaponKillsMelee',
     'column_name': 'melees',
     'team':        'us'},
    {'value':        'weaponKillsGrenade',
     'column_name': 'grenades',
     'team':        'us'},
    {'value':        'weaponKillsSuper',
     'column_name': 'supers',
     'team': 'us'}
]
           
#other key stats evntually
           # strength of the wolf
           # Super medals
           # weapon kill sprees

# add immediately
#   game date & start time
#   hash for map
#   player loadouts


weapon_stats = [
    {'value':        'referenceId',
     'column_name': 'weap_hash',
     'team':        'both'},
    {'value':        'referenceId',
     'column_name': 'weap_kills',
     'team':        'both'},
     ]


items = destiny.Manifest().items
activities = destiny.Manifest().activities 

gameN=0

for game in gameID:
    response = requests.get('https://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/' + game,
                            headers=head)
    
    try:
        response.raise_for_status()
        body = response.json()
        for item in body['Response']['data']['entries']:
            dfAppend = pd.DataFrame(
                {
                    'activity_id': [game],
                    'date': [body['Response']['data']['period']],    ## THIS IS UTC DATE WILL NEED TO FIX  
                    'game_N': [gameN],              
                    'player': [item['player']['destinyUserInfo']['displayName']],
                    'pclass': [item['player']['characterClass']],
                    'team': [item['values']['team']['basic']['displayValue']],
                    'score': [item['values']['score']['basic']['displayValue']],
                    'standing': [item['values']['standing']['basic']['displayValue']],
                    'play_time': [item['values']['activityDurationSeconds']['basic']['value']],
                    'map_hash': [body['Response']['data']['activityDetails']['referenceId']],
                    'map_name': [activities[body['Response']['data']['activityDetails']['referenceId']]['activityName']],
                    'map_path': [activities[body['Response']['data']['activityDetails']['referenceId']]['pgcrImage']],        
                    'k_d': [item['values']['killsDeathsRatio']['basic']['value']],        
                    'assists': [item['values']['assists']['basic']['value']]
                })
            
                
            for stat in keyStats:
                if stat['value'] in item['extended']['values']:
                    dfAppend[stat['column_name']] = pd.Series(
                        [item['extended']['values'][stat['value']]['basic']['value']],
                        index=dfAppend.index)
                else:
                    dfAppend[stat['column_name']] = 0
            
            
            
            
            dfStats = dfStats.append(dfAppend, ignore_index=True)
            
#-----------------------------------------------------------------            
 
            if 'weapons' in item['extended']:
                for x in range(0,len(item['extended']['weapons'])):
                    dfAppend2 = pd.DataFrame(
                        {
                            'game_N': [gameN],              
                            'player': [item['player']['destinyUserInfo']['displayName']],
                            'weap_hash': [item['extended']['weapons'][x]['referenceId']],
                            'weap_kills': [item['extended']['weapons'][x]['values']['uniqueWeaponKills']['basic']['value']],
                            'weap_name':[items[item['extended']['weapons'][x]['referenceId']]['itemName']],
                            'weap_type':[items[item['extended']['weapons'][x]['referenceId']]['itemSubType']]
                        })                  

                    dfWeaps = dfWeaps.append(dfAppend2, ignore_index=True)         

            
    except requests.exceptions.HTTPError as err:
        print("Error: {} {}".format(str(response.status_code), err))
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print("Cannot decode json, got %s" % response.text)

                            
    gameN+=1


dfStats.to_csv('DestinyStats.csv', header=True, index=True)
dfWeaps.to_csv('DestinyWeaps.csv', header=True, index=True, encoding = "ISO-8859-1")