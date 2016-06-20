
from __future__ import print_function
import pandas as pd
import destiny

game_ids = ['4892996696']
dfStats = pd.DataFrame(columns=())

# either pass in API key here or set as an environment variable
# by either pasting following line into terminal or adding to ~/.profile
# export BUNGIE_NET_API_KEY='key'
api_key = None

games = destiny.Game.games_from_ids(game_ids, api_key=api_key)

for game_id in game_ids:
    guardians = games[game_id].guardians
    for guardian in guardians.values():
        dfAppend = pd.DataFrame(
            {
                'Player Name':
                    [guardian.player_name],
                'Team Name':
                    [guardian.get('values.team.basic.displayValue')]
            })
        dfStats = dfStats.append(dfAppend, ignore_index=True)

print(dfStats, '\n')

john = destiny.Player('psn', 'JohnOfMars')

# Player.guardians dict needs a better index
titan = john.guardians['2305843009215820974']
print(titan.id, 'Light level {0} {1} {2} {3}'.format(
    titan.light_level, titan.g_class, titan.gender, titan.race), '\n')

last_10_trials = destiny.Game.games_from_guardian(titan, n=10)
print('TRIALS, SON')
for game in last_10_trials.values():
    print(game.id, game.mode, game.outcome)

items = destiny.Manifest().items
hash_code = 1274330687
ghorn = items[hash_code]
print('Name: {}'.format(ghorn['itemName']))
print('Type: {}'.format(ghorn['itemTypeName']))
print('Tier: {}'.format(ghorn['tierTypeName']))
print(ghorn['itemDescription'])
