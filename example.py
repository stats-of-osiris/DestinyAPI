
from __future__ import print_function
import pandas as pd
import destiny

activity_ids = ['4892996696']
dfStats = pd.DataFrame(columns=())

# either pass in API key here or set as an environment variable
# by either pasting following line into terminal or adding to ~/.profile
# export BUNGIE_NET_API_KEY='key'
api_key = None

activities = destiny.ActivityInfo.activities_from_ids(activity_ids, api_key)

for activity_id in activity_ids:
    characters = activities[activity_id].characters
    for character in characters.values():
        dfAppend = pd.DataFrame(
            {
                'Player Name': [character.get('player.destinyUserInfo.displayName')],
                'Team Name': [character.get('values.team.basic.displayValue')]
            })
        dfStats = dfStats.append(dfAppend, ignore_index=True)

print(dfStats)

print(destiny.Player('psn', 'JohnOfMars').id)
