# -*- coding: utf-8 -*-

"""
destipy.Game
~~~~~~~~~~~~~~~~

    This class provides access to the
        `PostGameCarnageReport`
    endpoint of the Destiny API.

"""
from . import utils, constants
from .Guardian import Guardian


class Game(object):
    """
    :param activity_id: The ID of the activity whose PGCR is requested.
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    """

    def __init__(self, activity_id, guardian=None, **kwargs):
        self.id = str(activity_id)
        self.data = utils.get_json(constants.API_PATHS[
            'get_post_game_carnage_report'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        self.mode = self.get('activityDetails.mode')
        # separate player data and game data via dict.pop()
        self.guardians = Guardian.guardians_from_data(self.data.pop('entries'))
        self.outcome = None
        if guardian:
            self.outcome = self.guardians[guardian.id].get('values.standing.basic.displayValue')

    @classmethod
    def games_from_ids(cls, game_ids, guardian=None, **kwargs):
        """
        Pass a list of game_ids and return a list of CarnageReport objects
        :param game_ids: List of game_ids
        :return: List of CarnageReport objects
        """
        games = {}
        for game_id in game_ids:
            games[game_id] = cls(game_id, guardian, **kwargs)
        return games

    @classmethod
    def games_from_guardian(cls, guardian, n='10', game_mode='trials',
                              last_activity_id=None, **kwargs):
        """
        Pass Guardian object and return a dict of Game objects
        :param guardian: Guardian object
        :param n: number of games to pull (optional)
        :param game_mode: game mode (optional, defaults to Trials)
        :param last_game_id: final game_id in the series to be pulled
            (optional)
        :return: List of Game objects
        """
        params = {
            'count': n,
            'mode': constants.ACTIVITY_MODES[game_mode]
        }
        game_ids = []
        data = utils.get_json(constants.API_PATHS[
            'get_activity_history'
        ].format(**locals()), params=params, **kwargs)
        for a in data['Response']['data']['activities']:
            # date for activity: a['period']
            # map for activity: a['activityDetails']['referenceId']
            game_ids.append(a['activityDetails']['instanceId'])
        games = cls.games_from_ids(game_ids, guardian, **kwargs)
        return games

    def get(self, data_path):
        return utils.crawl_data(self, data_path)

