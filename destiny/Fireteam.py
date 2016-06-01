# -*- coding: utf-8 -*-

"""
destiny.Fireteam
~~~~~~~~~~~~~~~~

    This class links Guardians together across games.

"""


class Fireteam(object):
    """
    Create a Fireteam from Guardian objects
    :param guardian:
    """
    def __init__(self, guardian):
        self.guardians = {}
        # TODO: this needs to be a dataframe
        self.stats = None
        self.add_guardian(guardian)

    @classmethod
    def fireteam_from_guardians(cls, guardians):
        fireteam = cls()
        fireteam.add_guardians(guardians)

    def add_guardian(self, guardian):
        # TODO: update self.stats here
        self.guardians[guardian.id] = guardian

    def add_guardians(self, guardians):
        for g in guardians:
            fireteam = self.add_guardian(g)
