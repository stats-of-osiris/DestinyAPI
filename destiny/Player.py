
from __future__ import print_function
import os
import time
from .utils import get_json
from .utils import crawl_data


class Player(object):
    def __init__(self, membership_type, display_name, api_key=None):
        if not api_key:
            api_key = os.environ['BUNGIE_NET_API_KEY']
        if membership_type == 'xbox':
            self.membership_type = 'TigerXbox'
        elif membership_type == 'psn':
            self.membership_type = 'TigerPsn'
        self.display_name = str(display_name)
        path = 'SearchDestinyPlayer/' + self.membership_type + '/' + self.display_name
        data = get_json(path, api_key)
        self.data = data['Response'][0]
        self.api_wait = data['ThrottleSeconds']
        self.id = data['Response'][0]['membershipId']

    @classmethod
    def player_from_name(cls, membership_type, display_name, api_key=None):
        player = Player(membership_type, display_name, api_key)
        if player.api_wait > 0:
            print("Pausing for {wait} seconds for rate limiting".format(**locals()))
            time.sleep(player.api_wait + 1)
        return player

    def get(self, data_path):
        return crawl_data(self, data_path)
