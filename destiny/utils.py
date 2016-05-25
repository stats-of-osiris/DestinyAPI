# -*- coding: utf-8 -*-

"""
destiny.utils
~~~~~~~~~~~~~~

This file provides utility functions that are used within destiny
that are also useful for external consumption.

"""

from __future__ import print_function
import requests
import os


def get_json(path, **kwargs):
    """
    Construct the appropriate syntax for a `requests.get()` call.
    :param path: uri path to append to base API path
    :param api_key: API key to authorize access to Destiny API (optional, keyword)
    :return: JSON object
    """
    # check kwargs to see if the api_key was passed in,
    # use environment variable if not
    kwargs = {} if kwargs is None else kwargs
    api_key = kwargs.get('api_key', os.environ['BUNGIE_NET_API_KEY'])
    base = 'https://www.bungie.net/Platform/Destiny/'
    url = base + path
    headers = {'X-API-Key': api_key}
    # Can't get this to attach to response correctly
    params = kwargs.get('params', None)
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def crawl_data(destiny_object, data_path):
    """
    Crawl dict tree via period-delimited string
    :param destiny_object: module object with a data variable containing the JSON response to crawl
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
