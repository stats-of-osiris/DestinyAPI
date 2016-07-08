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
                    game.pull_team_stat('weaponKillsMachineGun', team_name)
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
                    'team_name': team_name,
                    'allegiance': allegiance
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
