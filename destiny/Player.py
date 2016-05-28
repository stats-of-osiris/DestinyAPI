# -*- coding: utf-8 -*-

"""
destiny.Player
~~~~~~~~~~~~~~~~

    This class provides access to the
        `GetDestinyAccountSummary`
    endpoint of the Destiny API.

"""
from . import utils, constants
from .Guardian import Guardian


class Player(object):
    """
    :param console: 'xbox' or 'psn'; needed to accurately locate player
    :param screen_name: Screen name of the player
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    """
    def __init__(self, console, player_name, **kwargs):
        self.console_id = constants.PLATFORMS[
            str(console).lower()
        ]
        self.name = str(player_name)
        self.set_id(**kwargs)
        self.data = utils.get_json(constants.API_PATHS[
            'get_destiny_account_summary'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        # separate Player and Guardian data via .pop()
        self.guardians = Guardian.guardians_from_data(
            self.data.pop('characters'))
        self.set_last_guardian

    def set_id(self, **kwargs):
        self.id = utils.get_json(constants.API_PATHS[
            'get_membership_id_by_display_name'
        ].format(**locals()),**kwargs)['Response']

    def set_last_guardian(self):
        # TODO: fix date logic
        date = '2010-01-01 00:00:00 PT'
        for g in self.guardians.values():
            if g.last_played > date:
                self.last_guardian = g
                date = g.last_played

    def get(self, data_path):
        return utils.crawl_data(self, data_path)
