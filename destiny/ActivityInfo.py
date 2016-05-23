
from __future__ import print_function
import time
import os
from .utils import get_json
from .utils import crawl_data
from .CarnageReport import CarnageReport


class ActivityInfo(object):
    def __init__(self, activity_id, api_key=None):
        if not api_key:
            api_key = os.environ['BUNGIE_NET_API_KEY']
        self.activity_id = str(activity_id)
        path = 'Stats/PostGameCarnageReport/' + str(activity_id)
        data = get_json(path, api_key)
        self.api_wait = data['ThrottleSeconds']
        # separate player data and game data
        character_data = data['Response']['data'].pop('entries')
        self.data = data['Response']['data']
        self.characters = CarnageReport.characters_from_data(character_data)

    @classmethod
    def activities_from_ids(cls, activity_ids, api_key=None):
        activities = {}
        for activity_id in activity_ids:
            activities[activity_id] = ActivityInfo(activity_id, api_key)
            if activities[activity_id].api_wait > 0:
                print("Pausing for {wait} seconds for rate limiting".format(**locals()))
                time.sleep(activities[activity_id].api_wait + 1)
        return activities

    @classmethod
    def activities_from_characters(cls, character_id, n=1, api_key=None):
        # TODO: return last n activities for character
        return NotImplemented

    def get(self, data_path):
        return crawl_data(self, data_path)
