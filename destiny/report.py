# -*- coding: utf-8 -*-

"""
stats_osiris.report
~~~~~~~~~~~~~~~~

    This is the primary module of stats_osiris. It returns several
    various dictionaries of game stats to enable further analysis of a player's
    Trials of Osiris performance.

"""

from . import constants
from .player import Guardian
from .game import Game
from tzlocal import get_localzone


class Report(object):
    def __init__(self, console, name, guardian_id=None,
                 games=9, last_game_id=None, **kwargs):
        """
        Cylcle through creating a Guardian and then calling
        `games_from_guardian` in order to pull raw data to create reports
        :param console: 'xbox' or 'psn'; needed to accurately locate player
        :param player_name: Screen name of the player
        :param guardian_id: Id of specific guardian to find.
                            If None, defaults to last played guardian.
        :param games: number of games to pull (defaults to 10; 25 is the max
            for a single API call
        :param last_game_id: final game_id in the series to be pulled
        """
        self.guardian = Guardian(
            console, name, guardian_id=guardian_id, **kwargs
        )
        self.data = Game.games_from_guardian(
            self.guardian, n=games, last_game_id=last_game_id, **kwargs
        )

    def report_games(self):
        """
        Aggregate self.data to a game level, filtered to stats defined in
        `constants`.
        :return: List of dicts
        """
        # Initialize list of desired game data
        report_list = []

        # Set timezone info
        tz = get_localzone()

        # Get game level metrics for each game
        for game in self.data:

            # Determine score and round count
            if game.result == 'Victory':
                us_score = 5.0
            else:
                us_score = game.us[0]['values']['teamScore']['basic']['value']
            them_score = game.them[0]['values']['teamScore']['basic']['value']
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

    def report_teams(self):
        """
        Aggregate self.data to a team per game level.
        :return: List of dicts
        """
        report_list = []

        for game in self.data:
            for t in game.team_data:
                team_name = t['teamName']

                # Compute the derived metrics
                kills_primary = sum(
                    [sum(
                        game.pull_team_stat(v[0], team_name)
                    ) for v in constants.PRIMARY_WEAPON_STATS.values()]
                )
                kills_prec_primary = sum(
                    [sum(
                        game.pull_team_stat(v[1], team_name)
                    ) for v in constants.PRIMARY_WEAPON_STATS.values()]
                )

                kills_special = sum(
                    [sum(
                        game.pull_team_stat(v[0], team_name)
                    ) for v in constants.SPECIAL_WEAPON_STATS.values()]
                )
                kills_prec_special = sum(
                    [sum(
                        game.pull_team_stat(v[1], team_name)
                    ) for v in constants.SPECIAL_WEAPON_STATS.values()]
                )

                kills_sniper = sum(
                    [sum(game.pull_team_stat(constants.SPECIAL_WEAPON_STATS['kills_sniper'][0], team_name))]
                )

                kills_prec_sniper = sum(
                    [sum(game.pull_team_stat(constants.SPECIAL_WEAPON_STATS['kills_sniper'][1], team_name))]
                )

                kills_shotgun = sum(
                    [sum(game.pull_team_stat(constants.SPECIAL_WEAPON_STATS['kills_shotgun'][0], team_name))]
                )

                kills_prec_shotgun = sum(
                    [sum(game.pull_team_stat(constants.SPECIAL_WEAPON_STATS['kills_shotgun'][1], team_name))]
                )

                kills_heavy = sum(
                    [sum(
                        game.pull_team_stat(v[0], team_name)
                    ) for v in constants.HEAVY_WEAPON_STATS.values()]
                )
                kills_prec_heavy = sum(
                    [sum(
                        game.pull_team_stat(v[1], team_name)
                    ) for v in constants.HEAVY_WEAPON_STATS.values()]
                )

                kills = sum(game.pull_team_stat(
                    constants.KEY_STATS['kills_total'], team_name))
                deaths = sum(game.pull_team_stat(
                    constants.KEY_STATS['deaths'], team_name))

                try:
                    kd_ratio = kills / deaths
                except ZeroDivisionError:
                    kd_ratio = kills

                if game.user_team == team_name:
                    allegiance = 'us'
                else:
                    allegiance = 'them'

                try:
                    avg_kill_distance = sum(
                        game.pull_team_stat('averageKillDistance', team_name)
                    ) / kills
                except ZeroDivisionError:
                    avg_kill_distance = 0

                try:
                    avg_life = sum(
                        game.pull_team_stat(
                            'activityDurationSeconds', team_name, False)
                    ) / deaths
                except ZeroDivisionError:
                    avg_life = sum(
                        game.pull_team_stat(
                            'activityDurationSeconds', team_name, False)
                    ) / len(game.pull_team_stat('kills', team_name))

                # Combine into team-level dict
                team_level_stats = {
                    'activity_id': game.activity_id,
                    'team_name': team_name,
                    'allegiance': allegiance,
                    'kd_ratio': kd_ratio,
                    'kills_primary': kills_primary,
                    'kills_prec_primary': kills_prec_primary,

                    'kills_special': kills_special,
                    'kills_prec_special': kills_prec_special,
                    'kills_sniper': kills_sniper,
                    'kills_prec_sniper': kills_prec_sniper,
                    'kills_shotgun': kills_shotgun,
                    'kills_prec_shotgun': kills_prec_shotgun,

                    'kills_heavy': kills_heavy,
                    'kills_prec_heavy': kills_prec_heavy,
                    'avg_life': avg_life,
                    'avg_kill_distance': avg_kill_distance
                }
                for k, v in constants.KEY_STATS.items():
                    if k in ['longest_life', 'longest_kill_spree']:
                        try:
                            team_level_stats[k] = max(
                                game.pull_team_stat(v, team_name)
                            )
                        except ValueError:
                            team_level_stats[k] = 0
                    elif k == 'assists':
                        team_level_stats[k] = sum(
                            game.pull_team_stat(v, team_name, False)
                        )
                    else:
                        team_level_stats[k] = sum(
                            game.pull_team_stat(v, team_name)
                        )

                team_level_stats['score'] = team_level_stats['kills_total'] * 100 + team_level_stats['deaths'] * -100 + team_level_stats[
                                                                                                    'assists'] * 30 + \
                                    team_level_stats['rez_count'] * 25 + team_level_stats['rezzed_count'] * 12.5

                report_list.append(team_level_stats)
        return report_list

    def report_my_team(self):
        """
        Aggregate self.data to a fireteam level, across all games.
        :return: List of dicts
        """
        report_list = []

        for g in self.data[0].us:
            user_name = g['player']['destinyUserInfo']['displayName']

            # Compute the derived metrics
            kills_primary = sum(
                    [sum(
                        self._get_player_stat(v[0], user_name)
                    ) for v in constants.PRIMARY_WEAPON_STATS.values()]
                )
            kills_prec_primary = sum(
                    [sum(
                        self._get_player_stat(v[1], user_name)
                    ) for v in constants.PRIMARY_WEAPON_STATS.values()]
                )
            kills_special = sum(
                    [sum(
                        self._get_player_stat(v[0], user_name)
                    ) for v in constants.SPECIAL_WEAPON_STATS.values()]
                )
            kills_prec_special = sum(
                    [sum(
                        self._get_player_stat(v[1], user_name)
                    ) for v in constants.SPECIAL_WEAPON_STATS.values()]
                )

            kills_sniper = sum(
                [sum(self._get_player_stat(constants.SPECIAL_WEAPON_STATS['kills_sniper'][0], user_name))]
            )

            kills_prec_sniper = sum(
                [sum(self._get_player_stat(constants.SPECIAL_WEAPON_STATS['kills_sniper'][1], user_name))]
            )

            kills_shotgun = sum(
                [sum(self._get_player_stat(constants.SPECIAL_WEAPON_STATS['kills_shotgun'][0], user_name))]
            )

            kills_prec_shotgun = sum(
                [sum(self._get_player_stat(constants.SPECIAL_WEAPON_STATS['kills_shotgun'][1], user_name))]
            )

            kills_heavy = sum(
                    [sum(
                        self._get_player_stat(v[0], user_name)
                    ) for v in constants.HEAVY_WEAPON_STATS.values()]
                )
            kills_prec_heavy = sum(
                    [sum(
                        self._get_player_stat(v[1], user_name)
                    ) for v in constants.HEAVY_WEAPON_STATS.values()]
                )

            kills = sum(self._get_player_stat('kills', user_name))
            deaths = sum(self._get_player_stat('deaths', user_name))

            try:
                kd_ratio = kills / deaths
            except ZeroDivisionError:
                kd_ratio = kills

            try:
                avg_kill_distance = sum(
                    self._get_player_stat('averageKillDistance', user_name)
                ) / kills
            except ZeroDivisionError:
                avg_kill_distance = 0

            try:
                avg_life = sum(
                    self._get_player_stat(
                        'activityDurationSeconds', user_name, False)
                ) / deaths
            except ZeroDivisionError:
                avg_life = sum(
                    self._get_player_stat(
                        'activityDurationSeconds', user_name, False)
                )

            us_stats = {
                'user_name': user_name,
                'kd_ratio': kd_ratio,
                'kills_primary': kills_primary,
                'kills_prec_primary': kills_prec_primary,

                'kills_special': kills_special,
                'kills_prec_special': kills_prec_special,
                'kills_sniper': kills_sniper,
                'kills_prec_sniper': kills_prec_sniper,
                'kills_shotgun': kills_shotgun,
                'kills_prec_shotgun': kills_prec_shotgun,

                'kills_heavy': kills_heavy,
                'kills_prec_heavy': kills_prec_heavy,
                'avg_life': avg_life,
                'avg_kill_distance': avg_kill_distance
            }
            for k, v in constants.KEY_STATS.items():
                if k in ['longest_life', 'longest_kill_spree']:
                    try:
                        us_stats[k] = max(
                            self._get_player_stat(v, user_name)
                        )
                    except ValueError:
                        us_stats[k] = 0
                elif k == 'assists':
                    us_stats[k] = sum(
                        self._get_player_stat(v, user_name, False)
                    )
                else:
                    us_stats[k] = sum(
                        self._get_player_stat(v, user_name)
                    )

            us_stats['score'] = us_stats['kills_total']*100+us_stats['deaths']*-100+us_stats['assists']*30+us_stats['rez_count']*25+us_stats['rezzed_count']*12.5
            report_list.append(us_stats)

        return report_list

    def _get_player_stat(self, stat, player, extended=True, display=False):
        """
        Function to find stats for a given player across all Games present
        in self.data.
        :param stat: Name of stat to pull. Must be in constants.
        :param player: Display_name of player
        :param extended: If True, searches down the `extended` tree of values
                         If False, searches down the base `values` tree.
                         Defaults to True.
        :param display: Determines which value type to retun.
                        If True, returns `displayValue` from the API.
                        If False, returns `value` from the API.
                        Defaults to False.
        :return: A list of values for the stat and player specified.
        """
        if display:
            value = 'displayValue'
        else:
            value = 'value'
        if extended:
            if stat == 'averageKillDistance':
                return [
                    g['extended']['values'][stat]['basic'][value] *
                    g['extended']['values']['kills']['basic'][value]
                    for game in self.data
                    for g in game.us
                    if
                    g['player']['destinyUserInfo']['displayName'] == player and
                    stat in g['extended']['values'].keys()
                ]
            else:
                return [
                    g['extended']['values'][stat]['basic'][value]
                    for game in self.data
                    for g in game.us
                    if
                    g['player']['destinyUserInfo']['displayName'] == player and
                    stat in g['extended']['values'].keys()
                ]
        else:
            return [
                g['values'][stat]['basic'][value]
                for game in self.data
                for g in game.us
                if g['player']['destinyUserInfo']['displayName'] == player and
                stat in g['values'].keys()
            ]
