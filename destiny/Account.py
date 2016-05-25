# -*- coding: utf-8 -*-

"""
destiny.Account
~~~~~~~~~~~~~~~~

This class provides access to the `GetAccount` endpoint of the
Destiny API.

"""
from . import utils
from . import constants
from . import Player


class Account(object):
    """
    Create Account object using JSON data from the `GetAccount` endpoint.
    :param membership_type: 'xbox' or 'psn'; needed to accurately locate player
    :param display_name: Screen name of the player
    """
    def __init__(self, membership_type, display_name, **kwargs):
        self.membership_type = constants.PLATFORMS[membership_type]
        self.display_name = str(display_name)
        self.membership_id = Player(membership_type, display_name).player_id
        path = '{0}/Account/{1}/'.format(
            self.membership_type, self.membership_id
        )
        data = utils.get_json(path, **kwargs)
        self.data = data
