# -*- coding: utf-8 -*-

"""
destipy.ReportContext
~~~~~~~~~~~~~~~~

    This class wraps several method calls to build everything
    needed for a report.

"""

from .utils import build_session
from .player import Player
from .game import Game
from .fireteam import Fireteam


class ReportContext(object):
    """
    :param console: 'xbox' or 'psn', needed to locate player
    :param name: PSN Online ID or Xbox Gamertag of the player
    :kwarg guardian_id: Guardian ID to pull Games
    :kwarg game_mode: game mode to pull Games
    :kwarg last_n: specify to pull the last n Games
    :kwarg last_game_id: ending point for last n Games
    :kwarg start_datetime: maybe?
    :kwarg end_datetime: maybe?
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    """

    def __init__(self, console, name, **kwargs):
        self.session = build_session(**kwargs)
        self.player = Player(console, name, session=self.session, **kwargs)
        kwargs = {} if not kwargs else kwargs
        guardian_id = kwargs.get('guardian_id')
        game_mode = kwargs.get('game_mode')
        last_n = kwargs.get('last_n')
        last_game_id = kwargs.get('last_game_id')
        start_datetime = kwargs.get('start_datetime')
        end_datetime = kwargs.get('end_datetime')

        if guardian_id in self.player.guardians:
            guardian = self.player.guardians[guardian_id]
        else:
            if guardian_id is not None:
                print("Guardian ID {guardian_id} not found using\
                    Player ID {self.player.id}".format(**locals()))
            guardian = self.player.last_guardian
        
        self.games = Game.games_from_guardian(guardian, last_n=last_n,
                                              last_game_id=last_game_id,
                                              session=self.session, **kwargs)
        
        self.teams = []
        # seed the first Fireteam with this Guardian
        self.teams.append(Fireteam(guardian))
        # TODO: add other Guardians to Fireteams

        # shortcuts
        self.home_team = self.teams[0]
        #self.away_team = self.teams[1]
