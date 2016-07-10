# -*- coding: utf-8 -*-

"""
destiny.Player
~~~~~~~~~~~~~~~~

    This class provides access to the
        `GetDestinyAccountSummary`
    endpoint of the Destiny API.

"""
from . import utils, constants
from .manifest import get_row


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
        self.guardians = self._set_guardians()

    def _set_guardians(self):
        """

        :return:
        """
        json = self.data.pop('characters')
        guardians_list = [
            {
                'guardian_id':
                    entry['characterBase']['characterId'],
                'class':
                    constants.CLASS[entry['characterBase']['classHash']],
                'race':
                    constants.RACE[entry['characterBase']['raceHash']],
                'gender':
                    constants.GENDER[entry['characterBase']['genderHash']],
                'light_lvl':
                    entry['characterBase']['stats']['STAT_LIGHT']['value'],
                'emblem':
                    get_row(
                        entry['emblemHash'], 'DestinyInventoryItemDefinition'
                    )['itemName'],
                'minutes_played':
                    int(entry['characterBase']['minutesPlayedTotal']),
                'date_last_played':
                    entry['characterBase']['dateLastPlayed']
            }
            for entry in json
        ]
        return guardians_list

    def get(self, data_path):
        return utils.crawl_data(self, data_path)


class Guardian(Player):
    def __init__(self, console, player_name, guardian_id=None, **kwargs):
        Player.__init__(self, console, player_name, **kwargs)
        if guardian_id:
            self.guardian_id = int(guardian_id)
        else:
            self.guardian_id = self._get_last_guardian()
        self.data = self._filter_guardian()

    def _filter_guardian(self):
        for guardian in self.guardians:
            if guardian['guardian_id'] == self.guardian_id:
                return guardian

    def _get_last_guardian(self):
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
