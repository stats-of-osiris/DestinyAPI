# -*- coding: utf-8 -*-

"""
destiny.CarnageReport
~~~~~~~~~~~~~~~~

This class provides access to the `PostGameCarnageReport` endpoint of the
Destiny API.

"""
from . import utils
import os
import time


class CarnageReport(object):
    """
    :param activity_id: The ID of the activity whose PGCR is requested.
    :param api_key: API key to authorize access to Destiny API (optional, keyword)

    Usage::

        >>> import destiny
        >>> pgcr = destiny.CarnageReport('4892996696').data
        >>> pgcr.get('mode')
        '14'
    """

    def __init__(self, activity_id, **kwargs):
        self.type = 'Post Game Carnage Report'
        self.activity_id = str(activity_id)
        path = 'Stats/PostGameCarnageReport/{0}'.format(self.activity_id)
        data = utils.get_json(path, **kwargs)
        self.api_wait = data['ThrottleSeconds']
        # separate player data and game data
        player_data = data['Response']['data'].pop('entries')
        self.data = data['Response']['data']
        self.player_data = player_data
        self.players = CarnagePlayers.players_from_data(player_data)

    @classmethod
    def reports_from_ids(cls, activity_ids, **kwargs):
        """
        Pass a list of activity_ids and return a list of CarnageReport objects
        :param activity_ids: List of activity_ids
        :param api_key: API key to authorize access to Destiny API (optional, keyword)
        :return: List of CarnageReport objects
        """
        activities = {}
        for activity_id in activity_ids:
            activities[activity_id] = CarnageReport(activity_id, **kwargs)
            if activities[activity_id].api_wait > 0:
                print("Pausing for {0} seconds "
                      "for rate limiting".format(activities[activity_id].api_wait))
                time.sleep(activities[activity_id].api_wait + 1)
        return activities

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from CarnageReport JSON object
        """
        return utils.crawl_data(self, data_path)


class CarnagePlayers(object):
    def __init__(self, data):
        self.type = 'player'
        self.data = data
        # not sure if this will work since the object isn't fully created yet
        # self.name = self.get('player.destinyUserInfo.displayName')
        self.name = data['player']['destinyUserInfo']['displayName']

    @classmethod
    def players_from_data(cls, player_data):
        players = {}
        for pd in player_data:
            newplayer = CarnagePlayers(pd)
            players[newplayer.name] = newplayer
        return players

    def get(self, datapath):
        return utils.crawl_data(self, datapath)
