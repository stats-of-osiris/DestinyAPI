# -*- coding: utf-8 -*-

"""
stats_osiris.report
~~~~~~~~~~~~~~~~

    This is the primary module of stats_osiris. It returns several
    various dictionaries of game stats to enable further analysis of a player's
    Trials of Osiris performance.

"""

from . import utils
from .player import Guardian
from .game import Game
from tzlocal import get_localzone


class Report(object):
    def __init__(self, console, name, guardian_id=None,
                 games=10, last_game_id=None):
        # Collect data from API
        with utils.build_session() as s:
            self.guardian = Guardian(console, name, guardian_id=guardian_id,
                                     session=s)
            self.game_data = Game.games_from_guardian(
                self.guardian, games, last_game_id, session=s)
        self.game_report = self.create_game_report()
        self.team_report = self.create_team_report()

    def create_game_report(self):
        # Initialize list of desired game data
        report_list = []

        # Set timezone info
        tz = get_localzone()

        # Get game level metrics for each game
        for game in self.game_data:

            # Determine score and round count
            us_score = game.us['score']['basic']['value']
            them_score = game.them['score']['basic']['value']
            rounds = us_score + them_score

            # Calculate length of the game
            play_time = (
                game.user_data[
                    'values']['activityDurationSeconds']['basic']['value'] +
                game.user_data[
                    'values']['leaveRemainingSeconds']['basic']['value']
            )

            # Combine into game-level dict
            game_level_stats = {
                'activity_id': game.activity_id,
                'date': game.time.astimezone(tz),
                'map_name': game.map['activityName'],
                'map_image': game.map['pgcrImage'],
                'team': game.user_team,
                'standing': game.result,
                'score': us_score,
                'enemy_score': them_score,
                'sweaty?': game.sweaty,
                'play_time': play_time,
                'avg_round_time': play_time / rounds
            }
            report_list.append(game_level_stats)
        return report_list

    def create_team_report(self):
        report_list = []

        for game in self.game_data:
            for t in game.team_data:

                # Grab common metrics
                team_name = t['teamName']
                kills = sum(game.pull_team_stat('kills', team_name))
                deaths = sum(game.pull_team_stat('deaths', team_name))
                assists = sum(game.pull_team_stat('assists', team_name, False))
                if game.user_team == team_name:
                    allegiance = 'us'
                else:
                    allegiance = 'them'

                # Combine into team-level dict
                team_level_stats = {
                    'activity_id': game.activity_id,
                    'team': team_name,
                    'allegiance': allegiance,
                    'kills': kills,
                    'deaths': deaths,
                    'assists': assists,
                    'kd_ratio': kills / deaths,
                    'rezzed_count': sum(game.pull_team_stat(
                        'resurrectionsReceived', team_name)),
                    'rez_count': sum(game.pull_team_stat(
                        'resurrectionsPerformed', team_name)),
                    'orbs_gathered': sum(game.pull_team_stat(
                        'orbsGathered', team_name))
                }
                report_list.append(team_level_stats)
        return report_list
