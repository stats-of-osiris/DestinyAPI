# -*- coding: utf-8 -*-

"""
destiny.Player
~~~~~~~~~~~~~~~~

This class provides access to the `GetMembershipIdByDisplayName` endpoint of the
Destiny API.
"""

import os
from . import utils
from . import constants


class Player(object):
    """
    Create Account object using JSON data from the `GetMembershipIdByDisplayName` endpoint.
    :param membership_type: 'xbox' or 'psn'; needed to accurately locate player
    :param display_name: Screen name of the player
    """
    def __init__(self, membership_type, display_name, **kwargs):
        self.membership_type = constants.PLATFORMS[membership_type]
        self.display_name = str(display_name)
        path = '{0}/Stats/GetMembershipIdByDisplayName/{1}/'.format(
            self.membership_type, self.display_name
        )
        data = utils.get_json(path, **kwargs)
        self.player_id = data['Response']
        self.api_wait = data['ThrottleSeconds']

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from SearchDestinyPlayer JSON object
        """
        return utils.crawl_data(self, data_path)
