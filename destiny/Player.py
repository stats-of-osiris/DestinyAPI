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
import pandas as pd


class Player(object):
    """
    :param console: 'xbox' or 'psn'; needed to accurately locate player
    :param player_name: Screen name of the player
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    """
    def __init__(self, console, player_name, **kwargs):
        self.console_name = console
        self.console_id = constants.PLATFORMS[
            str(console).lower()
        ]
        self.player_name = str(player_name)
        self.player_id = utils.get_json(
            constants.API_PATHS['get_membership_id_by_display_name'].format(
                **locals()), **kwargs)['Response']
        self.data = utils.get_json(constants.API_PATHS[
            'get_destiny_account_summary'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        self.grimoire = self.get('grimoireScore')
        # separate Player and Guardian data via .pop()
        # self.guardians = self.data.pop('characters')
        self.guardians = self.pull_guardians()

    def pull_guardians(self):
        json = self.data.pop('characters')
        guardians = []
        for entry in json:
            summary = pd.DataFrame(
                {
                    'class':
                        get_class(entry['characterBase']['classHash']),
                    'race':
                        get_race(entry['characterBase']['raceHash']),
                    'gender':
                        get_gender(entry['characterBase']['genderHash']),
                    'light_lvl':
                        entry['characterBase']['stats']['STAT_LIGHT']['value'],
                    'emblem':
                        get_row(
                            entry['emblemHash'],
                            'DestinyInventoryItemDefinition'
                        )['itemName'],
                    'minutes_played':
                        int(entry['characterBase']['minutesPlayedTotal'])
                },
                index=[entry['characterBase']['characterId']]
            ).rename_axis('guardian_id')
            guardians.append(summary)
        return pd.concat(guardians)

    def get(self, data_path):
        return utils.crawl_data(self, data_path)


class Guardian(Player):
    def __init__(self, console, player_name, guardian_id=None, **kwargs):
        Player.__init__(self, console, player_name, **kwargs)
        if guardian_id:
            self.guardian_id = guardian_id
        else:
            self.guardian_id = self.get_last_guardian()
        self.data = utils.get_json(
            constants.API_PATHS['get_character'].format(
                **locals()), **kwargs)['Response']['data']
        self.g_class = get_class(self.get('characterBase.classHash'))
        self.race = get_race(self.get('characterBase.raceHash'))
        self.gender = get_gender(self.get('characterBase.genderHash'))
        self.equipment = self.get_equipment()
        self.summary = self.create_summary()

    def get_last_guardian(self):
        """
        Finds the last guardian played.
        :return: Guardian Id as string
        """
        compare_date = '2010-01-01T00:00:00Z'
        for g in self.guardians:
            last_played = g['characterBase']['dateLastPlayed']
            if utils.compare_dates(last_played,
                                   compare_date) == last_played:
                last_guardian = g['characterBase']['characterId']
                compare_date = last_played
        return last_guardian

    def get_equipment(self):
        equipment = self.get('characterBase.peerView.equipment')
        stuff = []
        for e in equipment:
            stuff.append(e.get('itemHash'))
        return get_items(stuff)

    def create_summary(self):
        summary = pd.DataFrame(
            {
                'class': get_class(self.get('characterBase.classHash')),
                'race': get_race(self.get('characterBase.raceHash')),
                'gender': get_gender(self.get('characterBase.genderHash')),
                'light_lvl': self.get('characterBase.stats.STAT_LIGHT.value'),
                'emblem': get_row(
                    self.get('emblemHash'),
                    'DestinyInventoryItemDefinition'
                )['itemName']
            },
            index=[self.guardian_id]
        ).rename_axis('guardian_id')
        return summary
