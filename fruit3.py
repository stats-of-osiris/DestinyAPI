# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:07:32 2016

@author: montgomeryj
"""

import requests
import json
import pandas as pd
head = {'X-API-Key': 'key'}
gameID = ['4874839686']
dfStats = pd.DataFrame(columns=())

keyStats = [{'value': 'kills',
            'displayValue': 'Kills'},
            {'value': 'deaths',
            'displayValue': 'Deaths'},
            {'value': 'assists', #doesn't appear to be working
            'displayValue': 'Assists'},
            {'value': 'resurrectionsPerformed',
            'displayValue': 'Ressurrections Performed'},
            {'value': 'resurrectionsReceived',
            'displayValue': 'Resurrections Received'},
            {'value': 'weaponBestType',
            'displayValue': 'Best Weapon Type'},          
            
            #Primaries
            {'value': 'weaponKillsAutoRifle',
            'displayValue': 'Auto Rifle Kills'},
            {'value': 'weaponPrecisionKillsAutoRifle',
            'displayValue': 'Auto Rifle Prec Kills'},
            
            {'value': 'weaponKillsPulseRifle',
            'displayValue': 'Pulse Rifle Kills'},
            {'value': 'weaponPrecisionKillsPulseRifle',
            'displayValue': 'Pulse Rifle Prec Kills'},
            
            {'value': 'weaponKillsHandCannon',
            'displayValue': 'Hand Cannon Kills'},
            {'value': 'weaponPrecisionKillsHandCannon',
            'displayValue': 'Hand Cannon Prec Kills'},
            
            {'value': 'weaponKillsScoutRifle',
            'displayValue': 'Scout Rifle Kills'},
            {'value': 'weaponPrecisionKillsScoutRifle',
            'displayValue': 'Scout Rifle Prec Kills'},
            
            
            #Secondaries
            {'value': 'weaponKillsSniper',
            'displayValue': 'Sniper Rifle Kills'},
            {'value': 'weaponPrecisionKillsSniper',
            'displayValue': 'Sniper Rifle Prec Kills'},
            {'value': 'weaponKillsShotgun',
            'displayValue': 'Shotgun Kills'},
            {'value': 'weaponKillsFusionRifle', #doesn't appear to be working
            'displayValue': 'Fusion Rifle Kills'},
            
            #Heavy, melee, grenades, Supers
            {'value': 'weaponKillsRocket', #doesn't appear to be working
            'displayValue': 'Rocket Kills'},
            {'value': 'weaponKillsMachineGun', #doesn't appear to be working
            'displayValue': 'Machine Gun Kills'},
            {'value': 'weaponKillsMelee',
            'displayValue': 'Melee Kills'},
            {'value': 'weaponKillsGrenade',
            'displayValue': 'Grenade Kills'},
            {'value': 'weaponKillsSuper',
            'displayValue': 'Super Kills'}]

## Additional Stats for future
# Wrecking Ball
# From the Brink / Never Say Die
# Narrow Escape
            

for game in gameID:
    response = requests.get('https://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/' + game,
                            headers=head)
    try:
        response.raise_for_status()
        body = response.json()
        for item in body['Response']['data']['entries']:
            dfAppend = pd.DataFrame(
                {
                    'Player Name': [item['player']['destinyUserInfo']['displayName']],
                    'Team Name': [item['values']['team']['basic']['displayValue']],
                    'Team Score': [item['values']['score']['basic']['displayValue']],
                    'Play Time': [item['values']['activityDurationSeconds']['basic']['displayValue']]
                })
                
            for stat in keyStats:
                if stat['value'] in item['extended']['values']:
                    dfAppend[stat['displayValue']] = pd.Series(
                        [item['extended']['values'][stat['value']]['basic']['value']],
                        index=dfAppend.index)
                else:
                    dfAppend[stat['displayValue']] = 0
            dfStats = dfStats.append(dfAppend, ignore_index=True)
    except requests.exceptions.HTTPError as err:
        print("Error: {} {}".format(str(response.status_code), err))
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print("Cannot decode json, got %s" % response.text)
    dfStats.to_csv(game + 'DestinyStats.csv', header=True, index=True)
    

#
##Primaries
#{'value': 'weaponKillsAutoRifle',
#displayValue': 'Auto Rifle Kills'},
#{'value': 'weaponPrecisionKillsAutoRifle',
#displayValue': 'Auto Rifle Prec Kills'},
#{'value': 'weaponKillsPulseRifle',
#displayValue': 'Pulse Rifle Kills'},
#{'value': 'weaponPrecisionKillsPulseRifle',
#displayValue': 'Pulse Rifle Prec Kills'},
#{'value': 'weaponKillsPulseRifle',
#displayValue': 'Pulse Rifle Kills'},
#{'value': 'weaponPrecisionKillsPulseRifle',
#displayValue': 'Pulse Rifle Prec Kills'},
#{'value': 'weaponKillsPulseRifle',
#displayValue': 'Pulse Rifle Kills'},
#{'value': 'weaponPrecisionKillsPulseRifle',
#displayValue': 'Pulse Rifle Prec Kills'},
#
#
##Secondaries
#{'value': 'weaponKillsSniper',
#displayValue': 'Sniper Rifle Kills'},
#{'value': 'weaponPrecisionKillsSniper',
#displayValue': 'Sniper Rifle Prec Kills'},
#{'value': 'weaponKillsShotgun',
#displayValue': 'Shotgun Kills'},
#{'value': 'weaponKillsFusionRifle',
#displayValue': 'Fusion Rifle Kills'},
#
##Heavy, melee, grenades, Supers
#
#{'value': 'weaponKillsRockets',
#displayValue': 'Rocket Kills'}
#{'value': 'weaponKillsHMG',
#displayValue': 'Machine Gun Kills'}
#{'value': 'weaponKillsMelee',
#displayValue': 'Melee Kills'}
#{'value': 'weaponKillsGrenade',
#displayValue': 'Grenade Kills'}
#{'value': 'weaponKillsSuper',
#displayValue': 'Super Kills'}]
#
#dfAppend = pd.DataFrame(
#            {
#                'Player Name': [item['player']['destinyUserInfo']['displayName']],
#                'Team Name': [item['values']['team']['basic']['displayValue']]
#                'Team Score': [item['values']['score']['basic']['displayValue']]
#                'Game Tjme': [item['values']['activityDurationSeconds']['basic']['displayValue']]
#
#            })