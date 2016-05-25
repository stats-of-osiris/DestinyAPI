# -*- coding: utf-8 -*-

"""
destiny.CarnageReport
~~~~~~~~~~~~~~~~

This module provides access to the `PostGameCarnageReport` endpoint of the
Destiny API.

"""
from . import utils
import os
import time


class CarnageReport(object):
    """
    :param activity_id: The ID of the activity whose PGCR is requested.
    :param api_key: API key to authorize access to Destiny API

    Usage::

        >>> import destiny
        >>> pgcr = destiny.CarnageReport('4892996696', 'api_key').data
        >>> pgcr.get('mode')
        '14'

    """

    def __init__(self, activity_id, api_key=None):
        if not api_key:
            api_key = os.environ['BUNGIE_NET_API_KEY']
        self.type = 'Post Game Carnage Report'
        self.activity_id = str(activity_id)
        path = 'Stats/PostGameCarnageReport/' + str(activity_id)
        data = utils.get_json(path, api_key)
        self.api_wait = data['ThrottleSeconds']
        # separate player data and game data
        player_data = data['Response']['data'].pop('entries')
        self.data = data['Response']['data']
        self.player_data = player_data
        self.players = CarnagePlayers.players_from_data(player_data)

    @classmethod
    def activities_from_ids(cls, activity_ids, api_key=None):
        """
        Pass a list of activity_ids and receive back a list of JSON responses
        :param activity_ids: List of activity_ids
        :param api_key: API key to authorize access to Destiny API
        :return: List of dicts
        """
        activities = {}
        for activity_id in activity_ids:
            activities[activity_id] = CarnageReport(activity_id, api_key)
            if activities[activity_id].api_wait > 0:
                print("Pausing for {wait} seconds "
                      "for rate limiting".format(**locals()))
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
        self.name = data['player']['destinyUserInfo']['displayName']

    @classmethod
    def players_from_data(cls, player_data, api_key=None):
        players = {}
        for pd in player_data:
            newplayer = CarnagePlayers(pd)
            players[newplayer.name] = newplayer
        return players

    def get(self, datapath):
        return utils.crawl_data(self, datapath)