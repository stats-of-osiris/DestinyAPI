
from __future__ import print_function
import requests


# perform the request and turn it into a dict tree
def get_json(path, api_key):
    base = 'https://www.bungie.net/Platform/Destiny/'
    url = base + path
    headers = {'X-API-Key': api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


# crawl dict tree via period-delimited string
def crawl_data(destiny_object, data_path):
    path = data_path.split('.')
    # start at top of path
    loc = destiny_object.data
    for p in path:
        if p in loc.keys():
            # continue navigating
            loc = loc[p]
        else:
            keys = loc.keys()
            print("{destiny_object.type}: Using {path}, couldn't find {p}. "
                  "Possible values at this level:\n{keys}".format(**locals()))
            print(loc[p])
    return loc
