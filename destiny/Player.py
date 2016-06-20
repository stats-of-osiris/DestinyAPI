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
        self.id = utils.get_json(
            constants.API_PATHS['get_membership_id_by_display_name'].format(
                **locals()), **kwargs)['Response']
        self.data = utils.get_json(constants.API_PATHS[
            'get_destiny_account_summary'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        # separate Player and Guardian data via .pop()
        self.guardians = Guardian.guardians_from_data(
            self.data.pop('characters'))
        self.last_guardian = self.set_last_guardian()

    def set_last_guardian(self):
        # Grabs the dateLastPlayed for each Guardian in the account and finds
        # the Guardian dict of the one most recently played
        compare_date = '2010-01-01T00:00:00Z'
        for g in self.guardians.values():
            if utils.compare_dates(g.last_played,
                                   compare_date) == g.last_played:
                last_guardian = g
                compare_date = g.last_played
        return last_guardian

    def get(self, data_path):
        return utils.crawl_data(self, data_path)
