import numpy as np
import pandas as pd

import destiny

titan_report = destiny.Report('psn',
                              'igordennis',
                              2305843009242964293,
                              games=7,
                              last_game_id=5626785836)

# game_report = pd.DataFrame(titan_report.report_games())
#
# wins = game_report[(game_report.result == 'Victory')].result.count()
#
# win_rate = wins / len(game_report.index)
#
# print(
#     'Win Rate: {0:.0f}%'.format(win_rate * 100)
# )

guardian_report = pd.DataFrame(titan_report.report_guardians())

total_kills = (
    guardian_report[guardian_report['allegiance'] == 'us'].kills.sum() /
    guardian_report.activity_id.nunique()
)

print('Avg. Kills per Game: {}'.format(total_kills))

# team_report = pd.DataFrame(titan_report.report_teams())
#
# kill_cols = [col for col in team_report.columns if 'kills_' in col]
#
# kills_by_allegiance = team_report.groupby('allegiance')[kill_cols]
#
# print(
#     kills_by_allegiance.aggregate(np.sum)
# )
#
# teammate_report = pd.DataFrame(
#     titan_report.report_my_team()
# ).set_index('user_name')
#
# print(
#     teammate_report.kills_total
# )
