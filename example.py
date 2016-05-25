
from __future__ import print_function
import pandas as pd
import destiny
import json

activity_ids = ['4892996696']
dfStats = pd.DataFrame(columns=())

# either pass in API key here or set as an environment variable
# by either pasting following line into terminal or adding to ~/.profile
# export BUNGIE_NET_API_KEY='key'
api_key = None

reports = destiny.CarnageReport.reports_from_ids(activity_ids, api_key=api_key)

for activity_id in activity_ids:
    players = reports[activity_id].players
    for player in players.values():
        dfAppend = pd.DataFrame(
            {
                'Player Name':
                    [player.get('player.destinyUserInfo.displayName')],
                'Team Name':
                    [player.get('values.team.basic.displayValue')]
            })
        dfStats = dfStats.append(dfAppend, ignore_index=True)

print(dfStats, '\n')

john = destiny.Account('psn', 'JohnOfMars')
print(john.membership_id, '\n')

print(json.dumps(john.data, indent=4), '\n')

