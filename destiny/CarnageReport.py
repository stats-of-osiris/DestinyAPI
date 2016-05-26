# -*- coding: utf-8 -*-

"""
destiny.CarnageReport
~~~~~~~~~~~~~~~~

This class provides access to the `PostGameCarnageReport` endpoint of the
Destiny API.

"""
from . import utils, constants
import time


class CarnageReport(object):
    """
    :param activity_id: The ID of the activity whose PGCR is requested.
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call

    Usage::

        >>> import destiny
        >>> pgcr = destiny.CarnageReport('4892996696')
        >>> pgcr.get('mode')
        '14'
    """

    def __init__(self, activity_id, **kwargs):
        self.type = 'Post Game Carnage Report'
        self.activity_id = str(activity_id)
        data = utils.get_json(constants.API_PATHS[
            'get_post_game_carnage_report'
        ].format(**locals()), **kwargs)
        self.api_wait = data['ThrottleSeconds']
        # separate player data and game data
        player_data = data['Response']['data'].pop('entries')
        self.players = CarnagePlayers.players_from_data(player_data)
        self.data = data['Response']['data']

    @classmethod
    def reports_from_ids(cls, activity_ids, **kwargs):
        """
        Pass a list of activity_ids and return a list of CarnageReport objects
        :param activity_ids: List of activity_ids
        :return: List of CarnageReport objects
        """
        reports = {}
        for activity_id in activity_ids:
            reports[activity_id] = cls(activity_id, **kwargs)
            if reports[activity_id].api_wait > 0:
                print("Pausing for {0} seconds for rate limiting".format(
                    reports[activity_id].api_wait))
                time.sleep(reports[activity_id].api_wait + 1)
        return reports

    @classmethod
    def reports_from_guardian(cls, guardian, n='10', game_mode='trials',
                              last_activity_id=None, **kwargs):
        """
        Pass Account object and return a dict of CarnageReport objects
        :param guardian: Guardian object
        :param n: number of games to pull (optional)
        :param game_mode: game mode (optional, defaults to Trials)
        :param last_activity_id: final activity_id in the series to be pulled
            (optional, ignored for now)
        :return: List of CarnageReport objects
        """
        params = {
            'count': n,
            'mode': constants.ACTIVITY_MODES[game_mode]
        }
        activity_ids = []
        data = utils.get_json(constants.API_PATHS[
            'get_activity_history'
        ].format(**locals()), params=params, **kwargs)
        for a in data['Response']['data']['activities']:
            # date for activity: a['period']
            # activity_id may also be: a['activityDetails']['referenceId']
            activity_ids.append(a['activityDetails']['instanceId'])
        reports = cls.reports_from_ids(activity_ids, **kwargs)
        return reports

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from CarnageReport JSON object
        """
        return utils.crawl_data(self, data_path)


class CarnagePlayers(object):
    """
    :param data: JSON blob specific to this player and report

    Usage::

        >>> import destiny
        >>> pgcr = destiny.CarnageReport('4892996696')
        >>> pgcr.players[0].name
        'JohnOfMars'
    """

    def __init__(self, data):
        self.data = data
        self.name = self.get('player.destinyUserInfo.displayName')

    @classmethod
    def players_from_data(cls, player_data):
        players = {}
        for pd in player_data:
            new_player = cls(pd)
            players[new_player.name] = new_player
        return players

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from underlying JSON object
        """
        return utils.crawl_data(self, data_path)
