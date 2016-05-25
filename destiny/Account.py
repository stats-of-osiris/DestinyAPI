# -*- coding: utf-8 -*-

"""
destiny.Account
~~~~~~~~~~~~~~~~

This class provides access to the `GetDestinyAccountSummary` endpoint of the
Destiny API.

"""
from . import utils
from . import constants
from .Guardian import Guardian

API_PATH = '{self.membership_type}/Account/{self.membership_id}/Summary'

class Account(object):
    """
    Create Account object using JSON data from the
    `GetDestinyAccountSummary` endpoint.
    :param membership_type: 'xbox' or 'psn'; needed to accurately locate player
    :param display_name: Screen name of the player
    """
    def __init__(self, membership_type, display_name, **kwargs):
        self.membership_type = constants.PLATFORMS[str(membership_type).lower()]
        self.display_name = str(display_name)
        # self.membership_id = self.get_membership_id(**kwargs)
        self.set_membership_id(**kwargs)
        data = utils.get_json(API_PATH.format(**locals()), **kwargs)
        guardian_data = data['Response']['data'].pop('characters')
        self.guardians = Guardian.guardians_from_data(guardian_data)
        self.data = data['Response']['data']

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from underlying JSON object
        """
        return utils.crawl_data(self, data_path)

    def set_membership_id(self, **kwargs):
        """
        Helper method to get the membership id for the account
        """
        path = '{self.membership_type}/Stats/GetMembershipIdByDisplayName/{self.display_name}/'
        self.membership_id = utils.get_json(path.format(**locals()), **kwargs)['Response']
