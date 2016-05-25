# -*- coding: utf-8 -*-

"""
destiny.Account
~~~~~~~~~~~~~~~~

This class provides access to the `GetDestinyAccountSummary` endpoint of the
Destiny API.

"""
from . import utils
from . import constants
from . import Player


class Account(object):
    """
    Create Account object using JSON data from the
    `GetDestinyAccountSummary` endpoint.
    :param membership_type: 'xbox' or 'psn'; needed to accurately locate player
    :param display_name: Screen name of the player
    """
    def __init__(self, membership_type, display_name, **kwargs):
        self.membership_type = constants.PLATFORMS[membership_type]
        self.display_name = str(display_name)
        self.membership_id = Player(membership_type, display_name).player_id
        path = '{0}/Account/{1}/Summary'.format(
            self.membership_type, self.membership_id
        )
        data = utils.get_json(path, **kwargs)
        char_data = data['Response']['data'].pop('characters')
        self.char_data = char_data
        self.data = data['Response']['data']

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from CarnageReport JSON object
        """
        return utils.crawl_data(self, data_path)


class AccountChars(object):
    def __init__(self, data):
        self.type = 'character'
        self.data = data
        # not sure if this will work since the object isn't fully created yet
        # self.name = self.get('player.destinyUserInfo.displayName')
        self.char_class = constants.CLASS[
            data['characterBase']['classHash']
        ]
        self.char_gender = constants.GENDER[
            data['characterBase']['genderHash']
        ]
        self.char_race = constants.RACE[
            data['characterBase']['genderHash']
        ]
