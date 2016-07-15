import pandas as pd
import numpy as np
import destiny

titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009215820974)

game_report = pd.DataFrame(titan_report.report_games())

wins = game_report[(game_report.standing == 'Victory')].standing.count()

win_rate = wins / len(game_report.index)

print(
    'Win Rate: {0:.0f}%'.format(win_rate * 100)
)

team_report = pd.DataFrame(titan_report.report_teams())

kill_cols = [col for col in team_report.columns if 'kills_' in col]

kills_by_allegiance = team_report.groupby('allegiance')[kill_cols]

print(
    kills_by_allegiance.aggregate(np.sum)
)

teammate_report = pd.DataFrame(
    titan_report.report_my_team()
).set_index('user_name')

print(
    teammate_report.kills_total
)
