# -*- coding: utf-8 -*-

"""
stats_osiris.report
~~~~~~~~~~~~~~~~

    This is the primary module of stats_osiris. It returns several
    various dictionaries of game stats to enable further analysis of a player's
    Trials of Osiris performance.

"""

from. import constants
from .player import Guardian
from .game import Game
from tzlocal import get_localzone
from numpy import mean


class Report(object):
    def __init__(self, console, name, guardian_id=None,
                 games=10, last_game_id=None):
        self.guardian = Guardian(console, name, guardian_id=guardian_id)
        self.game_data = Game.games_from_guardian(
            self.guardian, n=games, last_game_id=last_game_id)
        self.game_report = self.__create_game_report()
        self.team_report = self.__create_team_report()

    def __create_game_report(self):
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
                game.user_guardian[
                    'values']['activityDurationSeconds']['basic']['value'] +
                game.user_guardian[
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

    def __create_team_report(self):
        report_list = []

        for game in self.game_data:
            for t in game.team_data:

                # Grab some initial metrics
                team_name = t['teamName']
                kill_primary = sum(
                    [sum(
                        game.pull_team_stat(v, team_name)
                    ) for v in constants.PRIMARY_WEAPON_STATS.values()]
                )
                kills_special = sum(
                    [sum(
                        game.pull_team_stat(v, team_name)
                    ) for v in constants.SPECIAL_WEAPON_STATS.values()]
                )
                kills_heavy = sum(
                    [sum(
                        game.pull_team_stat(v, team_name)
                    ) for v in constants.HEAVY_WEAPON_STATS.values()]
                )
                if game.user_team == team_name:
                    allegiance = 'us'
                else:
                    allegiance = 'them'

                # Combine into team-level dict
                team_level_stats = {
                    'activity_id': game.activity_id,
                    'team_name': team_name,
                    'allegiance': allegiance,
                    'kd_ratio': sum(game.pull_team_stat(
                        constants.KEY_STATS['kills'], team_name
                    )) / sum(game.pull_team_stat(
                        constants.KEY_STATS['deaths'], team_name
                    )),
                    'kills_primary': kill_primary,
                    'kills_special': kills_special,
                    'kills_heavy': kills_heavy
                }
                for k, v in constants.KEY_STATS.items():
                    if k in ['longest_life', 'longest_kill_spree']:
                        team_level_stats[k] = max(
                            game.pull_team_stat(v, team_name)
                        )
                    elif k in ['avg_life', 'avg_kill_distance']:
                        team_level_stats[k] = mean(
                            game.pull_team_stat(v, team_name)
                        )
                    elif k == 'assists':
                        team_level_stats[k] = sum(
                            game.pull_team_stat(v, team_name, False)
                        )
                    else:
                        team_level_stats[k] = sum(
                            game.pull_team_stat(v, team_name)
                        )
                report_list.append(team_level_stats)
        return report_list
