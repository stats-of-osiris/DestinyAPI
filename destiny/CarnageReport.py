
from .utils import crawl_data


class CarnageReport(object):
    def __init__(self, data):
        self.type = 'Carnage Report'
        self.data = data
        self.name = data['player']['destinyUserInfo']['displayName']

    @classmethod
    def characters_from_data(cls, player_data, api_key=None):
        characters = {}
        for pd in player_data:
            new_character = CarnageReport(pd)
            characters[new_character.name] = new_character
        return characters

    def get(self, data_path):
        return crawl_data(self, data_path)
