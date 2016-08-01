# -*- coding: utf-8 -*-

"""
stats_osiris.game
~~~~~~~~~~~~~~~~

    This module defines the `Game` class which receives data from the
    `PostGameCarnageReport` endpoint of the Destiny API, and reshapes it for
    use by the `Report` class to generate the data for analysis.

"""
from . import utils, constants
from .manifest import get_map
import pytz
from datetime import datetime


class Game(object):
    def __init__(self, activity_id, guardian_id, **kwargs):
        """
        This object receives data from Destiny's PGCR endpoint and reshapes
        it in preparation to be consumed by the Report object.
        :param activity_id: The ID of the activity whose PGCR is requested.
        :param guardian_id: guardian_id to determine teams and outcome
        :kwarg api_key: API key to authorize access to Destiny API (optional)
        :kwarg params: Query parameters to pass to the `requests.get()` call
        """
        self.activity_id = activity_id
        self.data = utils.get_json(constants.API_PATHS[
            'get_post_game_carnage_report'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        self.time = pytz.utc.localize(datetime.strptime(
                    self.get('period'), constants.TS))
        self.map = get_map(self.get('activityDetails.referenceId'))

        # separate player data and game data via dict.pop()
        self.guardian_data = self._set_guardian_data()
        self.team_data = self.data.pop('teams')
        self.user_guardian = [g for g in self.guardian_data
                              if int(g['character_id']) == int(guardian_id)][0]
        self.user_team = self.user_guardian['guardian']['team']
        self._set_allegiance()
        self.sweaty = self._set_sweaty()
        self.result = self.user_guardian['guardian']['standing']
        self.duration = self.user_guardian[
            'guardian']['leaveRemainingSeconds'] + self.user_guardian[
            'guardian']['activityDurationSeconds']

    @classmethod
    def games_from_ids(cls, game_ids: list, guardian, **kwargs):
        """
        Pass a list of game_ids and return a list of Game objects
        :param game_ids: List of game_ids
        :param guardian: Guardian object to pass through to Game
        :return: List of Game objects
        """
        games = []
        for game_id in game_ids:
            games.append(cls(game_id, guardian.guardian_id, **kwargs))
        return games

    @classmethod
    def games_from_guardian(cls, guardian, n=10, game_mode='trials',
                            last_game_id=None, **kwargs):
        """
        Pass Guardian object and return a list of Game objects
        :param guardian: Guardian object
        :param n: number of games to pull (defaults to 10; 25 is the max
            for a single API call
        :param game_mode: game mode (defaults to Trials)
        :param last_game_id: final game_id in the series to be pulled
        :return: List of Game objects
        """
        page = 0
        game_ids = []
        while True:
            params = {
                'page': str(page),
                'mode': constants.ACTIVITY_MODES[game_mode]
            }
            data = utils.get_json(constants.API_PATHS[
                'get_activity_history'].format(
                **locals()), params=params, **kwargs)
            try:
                data = data['Response']['data']['activities']
            except KeyError:
                print('More games requested than exist. '
                      'Returning {} games instead'.format(len(game_ids)))
                break
            if last_game_id is None:
                game_ids = game_ids + [
                    a['activityDetails']['instanceId'] for a in data
                ]
                # Stop append once we hit the requested number of games
                if len(game_ids) >= n:
                    game_ids = game_ids[:n]
                    break
            else:
                last_game_time = Game(last_game_id, guardian.guardian_id).time
                game_ids = game_ids + [
                    a['activityDetails']['instanceId']
                    for a in data
                    if pytz.utc.localize(
                        datetime.strptime(a['period'], constants.TS)) <=
                    last_game_time
                ]
                # Stop append once we have the # of games requested
                if len(game_ids) >= n:
                    game_ids = game_ids[:n]
                    break
            # Ask for next page if we need more games, else break the loop
            if len(game_ids) < n:
                if len(data) < 25:
                    print('More games requested than exist. '
                          'Returning {} games instead'.format(len(game_ids)))
                    break
                else:
                    page += 1
            else:
                break
        games = cls.games_from_ids(game_ids, guardian, **kwargs)
        return games

    def pull_team_stat(self, stat, team_name,
                       extended=True, display=False):
        """
        Finds the desired stat for the specified team (Alpha | Bravo)
        for a given Game.
        :param stat: Name of stat to pull. Must be in constants.
        :param team_name: Which team to aggregate.
        :param extended: If True, searches down the `extended` tree of values
                         If False, searches down the base `values` tree.
                         Defaults to True.
        :param display: Determines which value type to retun.
                        If True, returns `displayValue` from the API.
                        If False, returns `value` from the API.
                        Defaults to False.
        :return: A list of values for the stat and team specified.
        """
        if display:
            value = 'displayValue'
        else:
            value = 'value'
        if extended:
            # Find Total Kill Distance so average can be aggregated properly.
            if stat == 'averageKillDistance':
                return [
                    g['extended']['values'][stat]['basic'][value] *
                    g['extended']['values']['kills']['basic'][value]
                    for g in self.guardian_data
                    if g['values']['team']['basic']['displayValue'] ==
                    team_name and stat in g['extended']['values'].keys()
                ]
            else:
                return [
                    g['extended']['values'][stat]['basic'][value]
                    for g in self.guardian_data
                    if
                    g['values']['team']['basic']['displayValue'] ==
                    team_name and stat in g['extended']['values'].keys()
            ]
        else:
            return [
                g['values'][stat]['basic'][value] for g in self.guardian_data
                if g['values']['team']['basic']['displayValue'] ==
                team_name and stat in g['values'].keys()
            ]

    def _set_sweaty(self):
        """
        Determine whether a Trials game was "sweaty". Defined as enemy team
        scoring 3 or greater.
        :return: Boolean
        """
        for team in self.team_data:
            cond1 = team['teamName'] != self.user_team
            cond2 = self.get('activityDetails.mode') == 14
            if cond1 and cond2:
                them_score = team['score']['basic']['value']
                return them_score >= 3
        return False

    def _set_guardian_data(self):
        guardian_data = self.data.pop('entries')
        guardian_data = [
            {'character_id': g['characterId'],
             'guardian': {
                 **{
                     'lightLevel': g['player']['lightLevel'],
                     'characterClass': g['player']['characterClass'],
                     'weaponBestType':
                         g['extended']['values']['weaponBestType']['basic']['displayValue']
                     if 'weaponBestType' in g['extended']['values'].keys()
                     else None
                 },
                 **{
                     k: v for k, v in g['player']['destinyUserInfo'].items()
                     if k in ['displayName', 'iconPath']
                 },
                 **{
                     k: v['basic']['value']
                     for k, v in g['values'].items()
                     if k in ['leaveRemainingSeconds',
                              'activityDurationSeconds']
                     },
                 **{
                     k: v['basic']['displayValue']
                     for k, v in g['values'].items()
                     if k in ['standing', 'team']
                     }
             },
             'stats': {
                 **{
                     k: v['basic']['value']
                     for k, v in g['extended']['values'].items()
                     if k in constants.CORE_STATS
                     },
                 **{
                     k: v['basic']['value']
                     for k, v in g['values'].items()
                     if k == 'assists'
                     }
             },
             'medals': {
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'medals' in k
                 },
             'weapon_kills': {
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'weaponKills' in k
                 },
             'player_kills': {
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'OfPlayer' in k
             },
             'weapons:': [
                 {
                     **get_item(w['referenceId']),
                     **{
                         k: v['basic']['value']
                         for k, v in w['values'].items()
                         if k != 'uniqueWeaponKillsPrecisionKills'
                         }
                 } for w in g['extended']['weapons']
                 ] if 'weapons' in g['extended'].keys() else None
             } for g in guardian_data
            ]
        return guardian_data

    def _set_allegiance(self):
        for guardian in self.guardian_data:
            if guardian['guardian']['team'] == self.user_team:
                guardian['guardian']['allegiance'] = 'us'
            else:
                guardian['guardian']['allegiance'] = 'them'

    def get(self, data_path):
        return utils.crawl_data(self, data_path)
