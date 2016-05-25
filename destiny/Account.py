# -*- coding: utf-8 -*-

"""
destiny.Account
~~~~~~~~~~~~~~~~

This module provides access to the `GetDestinyAccountSummary` endpoint of the
Destiny API.

"""
from . import utils
from . import Player
import os

class Account(object):
    """
    Return JSON object from `SearchDestinyPlayer` endpoint.
    :param membership_type: 'xbox' or 'psn'; needed to accurately locate player
    :param display_name: Screen name of the player
    """
    def __init__(self, membership_type, display_name, api_key=None):
        if not api_key:
            api_key = os.environ['BUNGIE_NET_API_KEY']
        if membership_type == 'xbox':
            self.membership_type = 'TigerXbox'
        elif membership_type == 'psn':
            self.membership_type = 'TigerPsn'
        self.display_name = str(display_name)
        self.membership_id = Player(membership_type, display_name).player_id
        path = '{0}/Account/{1}/Summary'.format(
            self.membership_type, self.membership_id
        )
        data = utils.get_json(path, api_key)
        self.data = data['Response']['data']