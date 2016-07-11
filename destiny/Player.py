# -*- coding: utf-8 -*-

"""
stats_osiris.Player
~~~~~~~~~~~~~~~~

    This module defines the Player and Guardian classes, which pull from the
    `GetDestinyAccountSummary` endpoint of the Destiny API.

"""
from . import utils, constants
from .manifest import get_row
from datetime import datetime


class Player(object):
    def __init__(self, console, player_name, **kwargs):
        """
        :param console: 'xbox' or 'psn'; needed to accurately locate player
        :param player_name: Screen name of the player
        :kwarg api_key: API key to authorize access to Destiny API
        :kwarg params: Query parameters to pass to the `requests.get()` call
        """
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
        Pull summary data of each guardian belonging to the Player.
        :return: List of dicts
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
        """
        :param console: 'xbox' or 'psn'; needed to accurately locate player
        :param player_name: Screen name of the player
        :param guardian_id: Id of specific guardian to find.
                            If None, defaults to last played guardian.
        :kwarg api_key: API key to authorize access to Destiny API
        :kwarg params: Query parameters to pass to the `requests.get()` call
        """
        Player.__init__(self, console, player_name, **kwargs)
        if guardian_id:
            self.guardian_id = int(guardian_id)
        else:
            self.guardian_id = self._get_last_guardian()
        self.data = self._filter_guardian()

    def _filter_guardian(self):
        """
        Take the full guardian list from Player and filter to single Guardian.
        :return: Dict
        """
        for guardian in self.guardians:
            if guardian['guardian_id'] == self.guardian_id:
                return guardian

    def _get_last_guardian(self):
        """
        Finds the last guardian played.
        :return: String
        """
        dates_played = {
            datetime.strptime(g['date_last_played'],
                              constants.TS): g['guardian_id']
            for g in self.guardians
        }
        last_played = dates_played[max(dates_played.keys())]
        return last_played
