import pandas as pd
import destiny

game_ids = ['4892996696']
dfStats = pd.DataFrame(columns=())

# either pass in API key here or set as an environment variable
# by either pasting following line into terminal or adding to ~/.profile
# export BUNGIE_NET_API_KEY='key'
api_key = None

# games = destiny.Game.games_from_ids(
#     game_ids
    # , api_key=api_key
# )

# for game_id in game_ids:
#     guardians = games[game_id].guardians
#     for guardian in guardians.values():
#         dfAppend = pd.DataFrame(
#             {
#                 'Player Name':
#                     [guardian.player_name],
#                 'Team Name':
#                     [guardian.get('values.team.basic.displayValue')]
#             })
#         dfStats = dfStats.append(dfAppend, ignore_index=True)

# print(dfStats, '\n')

john = destiny.Player('psn', 'JohnOfMars')
print('player_id: {}'.format(john.player_id))
print(john.guardians)

titan_id = john.guardians.loc[
    (john.guardians['class'] == 'Titan')].index.values[0]

titan = destiny.Guardian('psn', 'JohnOfMars', titan_id)
print(titan.equipment.head())

# last_10_trials = destiny.Game.games_from_guardian(titan, n=10)
# print('\n', 'TRIALS, SON')
# for game in last_10_trials.values():
#     print(game.activity_id, game.mode, game.outcome)

hash_code = 1274330687
ghorn = destiny.get_item(hash_code)
print('\n', ghorn)
