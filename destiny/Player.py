# -*- coding: utf-8 -*-

"""
destiny.Player
~~~~~~~~~~~~~~~~

    This class provides access to the
        `GetDestinyAccountSummary`
    endpoint of the Destiny API.

"""
from . import utils, constants
from .manifest import get_class, get_gender, get_race, get_items, get_row


class Player(object):
    """
    :param console: 'xbox' or 'psn'; needed to accurately locate player
    :param player_name: Screen name of the player
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    """
    def __init__(self, console, player_name, **kwargs):
        if isinstance(console, int):
            self.console_id = console
        else:
            self.console_id = constants.PLATFORMS[str(console).lower()]
        self.player_name = str(player_name)
        self.player_id = utils.get_json(
            constants.API_PATHS['get_membership_id_by_display_name'].format(
                **locals()), **kwargs)['Response']
        self.data = utils.get_json(constants.API_PATHS[
            'get_destiny_account_summary'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        self.guardians = self.pull_guardians()

    def pull_guardians(self):
        json = self.data.pop('characters')
        guardians = []
        for entry in json:
            guardians.append(
                {'guardian_id': entry['characterBase']['characterId'],
                 'class': get_class(entry['characterBase']['classHash']),
                 'race': get_race(entry['characterBase']['raceHash']),
                 'gender': get_gender(entry['characterBase']['genderHash']),
                 'light_lvl':
                     entry['characterBase']['stats']['STAT_LIGHT']['value'],
                 'emblem':
                    get_row(
                        entry['emblemHash'],
                        'DestinyInventoryItemDefinition'
                    )['itemName'],
                 'minutes_played':
                    int(entry['characterBase']['minutesPlayedTotal']),
                 'date_last_played': entry['characterBase']['dateLastPlayed']
                 }
            )
        return guardians

    def get(self, data_path):
        return utils.crawl_data(self, data_path)


class Guardian(Player):
    def __init__(self, console, player_name, guardian_id=None, **kwargs):
        Player.__init__(self, console, player_name, **kwargs)
        if guardian_id:
            self.guardian_id = int(guardian_id)
        else:
            self.guardian_id = self.get_last_guardian()
        self.data = self.filter_guardian()

    def filter_guardian(self):
        for guardian in self.guardians:
            if guardian['guardian_id'] == self.guardian_id:
                return guardian

    def get_last_guardian(self):
        """
        Finds the last guardian played.
        :return: Guardian Id as string
        """
        compare_date = '2010-01-01T00:00:00Z'
        for guardian in self.guardians:
            last_played = guardian['date_last_played']
            if utils.compare_dates(
                    last_played, compare_date) == last_played:
                last_guardian = guardian['guardian_id']
                compare_date = last_played
        return last_guardian

