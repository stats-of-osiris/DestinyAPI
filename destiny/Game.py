# -*- coding: utf-8 -*-

"""
destipy.Game
~~~~~~~~~~~~~~~~

    This class provides access to the
        `PostGameCarnageReport`
    endpoint of the Destiny API.

"""
from . import utils, constants
from .manifest import get_map
import pytz
from datetime import datetime


class Game(object):
    """
    :param activity_id: The ID of the activity whose PGCR is requested.
    :param guardian: guardian_id to determine teams and outcome
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    """

    def __init__(self, activity_id, guardian_id, **kwargs):
        self.activity_id = activity_id
        self.data = utils.get_json(constants.API_PATHS[
            'get_post_game_carnage_report'
        ].format(**locals()), **kwargs)
        self.data = self.get('Response.data')
        self.time = pytz.utc.localize(datetime.strptime(
                    self.get('period'), '%Y-%m-%dT%H:%M:%SZ'))
        self.map = get_map(self.get('activityDetails.referenceId'))
        # separate player data and game data via dict.pop()
        self.guardian_data = self.data.pop('entries')
        self.team_data = self.data.pop('teams')
        self.user_guardian = [g for g in self.guardian_data
                              if int(g['characterId']) == int(guardian_id)][0]
        self.user_team = self.user_guardian[
            'values']['team']['basic']['displayValue']
        self.us = [team for team in self.team_data
                  if team['teamName'] == self.user_team][0]
        self.them = them = [team for team in self.team_data
                    if team['teamName'] != self.user_team][0]
        self.sweaty = self.determine_sweaty()
        self.result = self.us['standing']['basic']['displayValue']

    @classmethod
    def games_from_ids(cls, game_ids: list, guardian, **kwargs):
        """
        Pass a list of game_ids and return a list of Game objects
        :param game_ids: List of game_ids
        :param guardian: ???
        :return: List of Game objects
        """
        games = []
        for game_id in game_ids:
            games.append(cls(game_id, guardian.guardian_id, **kwargs))
        return games

    @classmethod
    def games_from_guardian(cls, guardian, n=10, game_mode='trials',
                            last_game_id=None, **kwargs):
        """
        Pass Guardian object and return a dict of Game objects
        :param guardian: Guardian object
        :param n: number of games to pull (defaults to 25, which is the max
            for a single API call
        :param game_mode: game mode (defaults to Trials)
        :param last_game_id: final game_id in the series to be pulled
            (optional)
        :return: List of Game objects
        """
        page = 0
        game_ids = []
        while True:
            params = {
                'page': str(page),
                'mode': constants.ACTIVITY_MODES[game_mode]
            }
            data = utils.get_json(constants.API_PATHS[
                'get_activity_history'].format(
                **locals()), params=params, **kwargs)
            if last_game_id is None:
                for a in data['Response']['data']['activities']:
                    game_ids.append(a['activityDetails']['instanceId'])
                    # Stop append once we hit the requested number of games
                    if len(game_ids) > n - 1:
                        break
            else:
                last_game_time = Game(last_game_id).time
                for a in data['Response']['data']['activities']:
                    if utils.compare_dates(a['period'], last_game_time,
                                           newest=False) == a['period']:
                        game_ids.append(a['activityDetails']['instanceId'])
                        # Stop append once we have the # of games requested
                        if len(game_ids) > n - 1:
                            break
            # Ask for next page if we need more games, else break the loop
            if len(game_ids) < n - 1:
                page += 1
            else:
                break
            # TODO: Add error checking for when more games are requested than exist
            # date for activity: a['period']
            # map for activity: a['activityDetails']['referenceId']
        games = cls.games_from_ids(game_ids, guardian, **kwargs)
        return games

    def pull_team_stat(self, stat, team_name,
                       extended=True, display=False):
        if display:
            value = 'displayValue'
        else:
            value = 'value'
        if extended:
            return [
                g['extended']['values'][stat]['basic'][value]
                for g in self.guardian_data
                if g['values']['team']['basic']['displayValue'] == team_name and
                stat in g['extended']['values'].keys()
                ]
        else:
            return [
                g['values'][stat]['basic'][value] for g in self.guardian_data
                if g['values']['team']['basic']['displayValue'] == team_name and
                stat in g['values'].keys()
                ]

    def determine_sweaty(self):
        them_score = self.them['score']['basic']['value']
        if self.get('activityDetails.mode') == 14:
            return them_score >= 3
        return False

    def get(self, data_path):
        return utils.crawl_data(self, data_path)

