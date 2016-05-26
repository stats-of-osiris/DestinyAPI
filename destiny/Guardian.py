# -*- coding: utf-8 -*-

"""
destiny.Guardian
~~~~~~~~~~~~~~~~

This class provides access to the `GetDestinyAccountSummary` endpoint of the
Destiny API.

"""
from . import utils, constants


class Guardian(object):
    """
    Create Guardian object using JSON data from the
    `GetDestinyAccountSummary` endpoint.
    :param data: JSON blob specific to this guardian
    """
    def __init__(self, data):
        self.data = data
        self.guardian_id = self.get('characterBase.characterId')
        self.account_id = self.get('characterBase.membershipId')
        self.account_type = self.get('characterBase.membershipType')
        self.type = constants.GUARDIAN_TYPE[
            self.get('characterBase.classHash')
        ]
        self.gender = constants.GUARDIAN_GENDER[
            self.get('characterBase.genderHash')
        ]
        self.race = constants.GUARDIAN_RACE[
            self.get('characterBase.raceHash')
        ]

    @classmethod
    def guardians_from_data(cls, guardian_data):
        guardians = {}
        for gd in guardian_data:
            guardian = cls(gd)
            guardians[guardian.guardian_id] = guardian
        return guardians

    def get(self, data_path):
        """
        Get the value from a dict entry by specifying a period-delimited string
        :param data_path: period-delimited string defining path to wanted value
        :return: value of specified key from underlying JSON object
        """
        return utils.crawl_data(self, data_path)

