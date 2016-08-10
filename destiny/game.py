# -*- coding: utf-8 -*-

"""
stats_osiris.game
~~~~~~~~~~~~~~~~

    This module defines the `Game` class which receives data from the
    `PostGameCarnageReport` endpoint of the Destiny API, and reshapes it for
    use by the `Report` class to generate the data for analysis.

"""
from . import utils, constants
from .manifest import get_map, get_item
import pytz
from tzlocal import get_localzone
from datetime import datetime


class Game(object):
    def __init__(self, activity_id: int, guardian_id: int, **kwargs):
        """
        This object receives data from Destiny's PGCR endpoint and reshapes
        it in preparation to be consumed by the Report object.
        :param activity_id: The ID of the activity whose PGCR is requested.
        :param guardian_id: guardian_id to determine teams and outcome
        :kwarg api_key: API key to authorize access to Destiny API (optional)
        :kwarg params: Query parameters to pass to the `requests.get()` call
        """
        self.activity_id = activity_id
        self.guardian_id = guardian_id
        self.data = utils.get_json(constants.API_PATHS[
            'get_post_game_carnage_report'
        ].format(**locals()), **kwargs)['Response']['data']

        # Break out data into different levels: activity, team, guardian
        # Also separate out data specific to the user
        self.guardian_data = self._set_guardian_data()
        self.user_guardian = self._set_user_guardian()
        self._set_allegiance() # Update guardian_data now we know user_guardian
        self.team_data = self._set_team_data()
        self.activity_data = self._set_activity_data()

    def _set_guardian_data(self):
        guardian_data = self.data['entries']
        guardian_data = [
            {'activity_id': self.activity_id,
             'guardian_id': g['characterId'],
             # Core Guardian Data
             **{
                 'lightLevel': g['player']['lightLevel'],
                 'characterClass': g['player']['characterClass'],
                 'weaponBestType':
                     g['extended']['values'][
                         'weaponBestType']['basic']['displayValue']
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
             },
             # Core Stats
             **{
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if k in constants.CORE_STATS
             },
             **{
                 k: v['basic']['value']
                 for k, v in g['values'].items()
                 if k == 'assists'
             },
             # Medals
             **{
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'medals' in k
             },
             # Weapon Kill Stats
             **{
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'weaponKills' in k
             },
             **{
                 k: v['basic']['value']
                 for k, v in g['extended']['values'].items()
                 if 'OfPlayer' in k
             }
             } for g in guardian_data
            ]
        return guardian_data

    def _set_user_guardian(self):
        user_guardian = None
        for g in self.guardian_data:
            if int(g['guardian_id']) == int(self.guardian_id):
                user_guardian = g
            else:
                pass
        # Fail safe is guardian_id provided isn't in the game
        if not user_guardian:
            raise Exception('Guardian provided not found in game data.')
        return user_guardian

    def _set_team_data(self):
        team_data = self.data['teams']
        team_data = [
            {
                'team_name': t['teamName'],
                'standing': t['standing']['basic']['displayValue'],
                # Make sure score is 5 if Victory is registered
                'score': 5 if t[
                    'standing']['basic']['displayValue'] == "Victory"
                else t['score']['basic']['value'],
                'allegiance': 'us' if t['teamName'] == self.user_guardian[
                    'team'] else 'them',

            } for t in team_data
        ]
        return team_data

    def _set_activity_data(self):
        # Set up prelim data
        tz = get_localzone()
        time = pytz.utc.localize(datetime.strptime(
            self.get('period'), constants.TS))
        game_map = get_map(self.get('activityDetails.referenceId'))
        scores = {t['allegiance']: t['score'] for t in self.team_data}
        sweaty = True if (scores['them'] >= 3) else False
        play_time = (self.user_guardian['leaveRemainingSeconds'] +
                     self.user_guardian['activityDurationSeconds'])
        rounds = scores['us'] + scores['them']

        activity_data = {
            'activity_id': self.activity_id,
            'date': time.astimezone(tz),
            'map_name': game_map['activityName'],
            'map_image': game_map['pgcrImage'],
            'team_us': self.user_guardian['team'],
            'result': self.user_guardian['standing'],
            'score_us': scores['us'],
            'score_them': scores['them'],
            'sweaty': sweaty,
            'play_time': play_time,
            'rounds': rounds,
            'avg_round_time': play_time / rounds
        }
        return activity_data

    def _pull_team_stat(self, stat, team_name,
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

    def _set_allegiance(self):
        for guardian in self.guardian_data:
            if (guardian['team'] ==
                    self.user_guardian['team']):
                guardian['allegiance'] = 'us'
            else:
                guardian['allegiance'] = 'them'

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
        tz = get_localzone()
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
                last_game_time = Game(
                    last_game_id, guardian.guardian_id
                ).activity_data['time']
                game_ids = game_ids + [
                    a['activityDetails']['instanceId']
                    for a in data
                    if pytz.utc.localize(
                        datetime.strptime(a['period'], constants.TS)
                    ).astimezone(tz) <=
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

    def get(self, data_path):
        return utils.crawl_data(self, data_path)

# To be implemented later:
# 'weapons:': [
#                  {
#                      **get_item(w['referenceId']),
#                      **{
#                          k: v['basic']['value']
#                          for k, v in w['values'].items()
#                          if k != 'uniqueWeaponKillsPrecisionKills'
#                          }
#                  } for w in g['extended']['weapons']
#                  ] if 'weapons' in g['extended'].keys() else None
