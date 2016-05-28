# -*- coding: utf-8 -*-

"""
destiny.Guardian
~~~~~~~~~~~~~~~~

    This class provides access to the
        `GetDestinyAccountSummary`
    endpoint of the Destiny API.

"""
from . import utils, constants


class Guardian(object):
    """
    Create a Guardian from JSON data
    :param data: JSON blob specific to this guardian
    """
    def __init__(self, data):
        self.data = data
        if self.usingPlayerData():
            self.last_played = self.get('characterBase.dateLastPlayed')
            self.id = self.get('characterBase.characterId')
            self.player_id = self.get('characterBase.membershipId')
            self.player_name = None
            self.console_id = self.get('characterBase.membershipType')
            self.light_level = self.get('characterBase.powerLevel')
            self.guardian_level = self.get('characterLevel')
            self.g_class = constants.GUARDIAN_TYPE[self.get('characterBase.classHash')]
            # self.gender = constants.GUARDIAN_GENDER[self.get('characterBase.genderHash')]
            # self.race = constants.GUARDIAN_RACE[self.get('characterBase.raceHash')]
        else:
            self.last_played = None
            self.id = self.get('characterId')
            self.player_id = self.get('player.destinyUserInfo.membershipId')
            self.player_name = self.get('player.destinyUserInfo.displayName')
            self.console_id = self.get('player.destinyUserInfo.membershipType')
            self.g_class = self.get('player.characterClass')
            self.light_level = self.get('player.lightLevel')
            self.guardian_level = self.get('player.characterLevel')
            # self.gender = None
            # self.race = None

    @classmethod
    def guardians_from_data(cls, data, player_name=None):
        """
        Create Guardian object using JSON data.
        :param guardian_data: JSON blob for all guardians
        """
        guardians = {}
        for d in data:
            guardian = cls(d)
            if player_name:
                guardian.player_name = player_name
            guardians[guardian.id] = guardian
        return guardians

    def usingPlayerData(self):
        return self.get('characterBase', False)

    def get(self, data_path, throw_error=True):
        return utils.crawl_data(self, data_path, throw_error)
