import pandas as pd
import numpy as np
import destiny

# titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009215820974, games=10)
titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009244596520, games=7)

game_report = pd.DataFrame(titan_report.report_games())

team_report = pd.DataFrame(titan_report.report_teams())

teammate_report = pd.DataFrame(
    titan_report.report_my_team()
).set_index('user_name')

game_report.to_csv('game_report.csv', header=True, index=True)
team_report.to_csv('team_report.csv', header=True, index=True)
teammate_report.to_csv('teammate_report.csv', header=True, index=True)

print(team_report[team_report['allegiance'] == 'us']['kd_ratio'].mean())

#Simple Examples

# wins = game_report[(game_report.standing == 'Victory')].standing.count()
#
# win_rate = wins / len(game_report.index)
#
# print(
#     'Win Rate: {0:.0f}%'.format(win_rate * 100)
# )
#
# kill_cols = [col for col in team_report.columns if 'kills_' in col]
#
# kills_by_allegiance = team_report.groupby('allegiance')[kill_cols]
#
# print(
#     kills_by_allegiance.aggregate(np.sum)
# )


# print(
#     teammate_report.score / sum(teammate_report.score)*100
# )
