# -*- coding: utf-8 -*-

"""
stats_osiris.report
~~~~~~~~~~~~~~~~

    This is the primary module of stats_osiris. It returns exports several
    DataFrames as CSV files to enable further analysis of a player's
    Trials of Osiris performance.

"""

from . import utils
from .player import Guardian
from .game import Game
from .manifest import get_map
import csv
from datetime import datetime
from tzlocal import get_localzone
import pytz


def get_report(console, name, guardian_id=None,
               games=10, last_game_id=None):

    # Collect data from API
    with utils.build_session() as s:
        guardian = Guardian(console, name, guardian_id=guardian_id, session=s)
        game_data = Game.games_from_guardian(
            guardian, games, last_game_id=last_game_id, session=s)

    # Initialize list of desired game data
    csv_games = []
    csv_teams = []

    # Set timezone info
    tz = get_localzone()

    # Get game level metrics for each game
    for game in game_data:

        # Convert period to datetime
        period = pytz.utc.localize(datetime.strptime(
                game.get('period'), '%Y-%m-%dT%H:%M:%SZ'))

        # Set which guardian entry is the user
        user_data = [g for g in game.guardian_data
                     if int(g['characterId']) == guardian.guardian_id][0]
        user_team = user_data['values']['team']['basic']['displayValue']

        # Set which team is 'us' and which is 'them'
        us = [team for team in game.team_data
              if team['teamName'] == user_team][0]
        them = [team for team in game.team_data
                if team['teamName'] != user_team][0]

        us_score = us['score']['basic']['value']
        them_score = them['score']['basic']['value']
        sweaty = them_score >= 3
        rounds = us_score + them_score

        # Calculate length of the game
        play_time = (
            user_data['values']['activityDurationSeconds']['basic']['value'] +
            user_data['values']['leaveRemainingSeconds']['basic']['value']
        )

        # Pull map info from manifest
        pvp_map = get_map(game.get('activityDetails.referenceId'))

        # Combine into game-level dict
        game_level_stats = {
            'activity_id': game.activity_id,
            'date': period.astimezone(tz),
            'map_name': pvp_map['activityName'],
            'map_image': pvp_map['pgcrImage'],
            'team': us['teamName'],
            'standing': us['standing']['basic']['displayValue'],
            'score': us_score,
            'enemy_score': them_score,
            'sweaty?': sweaty,
            'play_time': play_time,
            'avg_round_time': play_time / rounds
        }
        csv_games.append(game_level_stats)

        # Combine into team-level dict
        for t in game.team_data:
            team_name = t['teamName']
            team_level_stats = {
                'activity_id': game.activity_id,
                'team': team_name,
                'kills': sum(game.pull_team_stat('kills', team_name)),
                'deaths': sum(game.pull_team_stat('deaths', team_name)),
                'assists': sum(game.pull_team_stat('assists', team_name)),
                'rezzed_count': sum(game.pull_team_stat(
                    'resurrectionsReceived', team_name, True)),
                'rez_count': sum(game.pull_team_stat(
                    'resurrectionsPerformed', team_name, True)),
                'orbs_gathered': sum(game.pull_team_stat(
                    'orbsGathered', team_name, True))
            }
            csv_teams.append(team_level_stats)

    # Write game data to csv file
    with open('game_stats.csv', 'w') as csv_file:
        headers = ['activity_id', 'date', 'map_name', 'map_image', 'team',
                   'standing', 'score', 'enemy_score', 'sweaty?',
                   'play_time', 'avg_round_time']
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_games)
    print('Game CSV created!')

    # Write team data to csv file
    with open('team_stats.csv', 'w') as csv_file:
        headers = team_level_stats.keys()
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(csv_teams)
    print('Team CSV created!')



