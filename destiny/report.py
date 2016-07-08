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

                # Grab common metrics
                team_name = t['teamName']
                kills = sum(game.pull_team_stat('kills', team_name))
                kills_prec = sum(game.pull_team_stat(
                    'precisionKills', team_name))
                kills_primary = sum(
                    game.pull_team_stat('weaponKillsAutoRifle', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsHandCannon', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsScoutRifle', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsPulseRifle', team_name)
                )
                kills_special = sum(
                    game.pull_team_stat('weaponKillsSniper', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsShotgun', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsFusionRifle', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKillsSidearm', team_name)
                )
                kills_heavy = sum(
                    game.pull_team_stat('weaponKillsRocketLauncher', team_name)
                ) + sum(
                    game.pull_team_stat('weaponKills')
                )
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
                        'orbsGathered', team_name)),
                    'orbs_dropped': sum(game.pull_team_stat(
                        'orbsDropped', team_name)),
                    'longest_life': max(game.pull_team_stat(
                        'longestSingleLife', team_name)),
                    'avg_life': mean(game.pull_team_stat(
                        'averageLifespan', team_name)),
                    'longest_kill_spree': max(game.pull_team_stat(
                        'longestKillSpree', team_name)),
                    'avg_kill_distance': mean(game.pull_team_stat(
                        'averageKillDistance', team_name)),
                    'kills_precision': kills_prec,
                    'kills_prec_rate': kills_prec / kills,
                    'kills_primary': kills_primary
                }
                report_list.append(team_level_stats)
        return report_list
