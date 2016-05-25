# -*- coding: utf-8 -*-

"""
destiny.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within destiny
that are also useful for external consumption.

"""

from __future__ import print_function
import requests


def get_json(path, api_key):
    """
    Construct the appropriate syntax for a `requests.get()` call.
    :param path: uri path to append to base API path
    :param api_key: API key to authorize access to Destiny API
    :return: JSON object
    """
    base = 'https://www.bungie.net/Platform/Destiny/'
    url = base + path
    headers = {'X-API-Key': api_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def crawl_data(destiny_object, data_path):
    """
    Crawl dict tree via period-delimited string
    :param destiny_object: JSON response from Destiny API, or a subset thereof
    :param data_path: period-delimited string that specificies which value to return
    :return: single value, could be a string or int
    """
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
