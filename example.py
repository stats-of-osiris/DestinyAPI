import pandas as pd
import destiny

titan_report = destiny.Report('psn', 'JohnOfMars', 2305843009215820974)

game_report = pd.DataFrame(titan_report.game_report)

# print(game_report)

team_report = pd.DataFrame(titan_report.team_report)

print(team_report.loc[:, 'kills_primary'])
