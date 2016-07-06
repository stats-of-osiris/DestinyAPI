# -*- coding: utf-8 -*-

"""
destiny.utils
~~~~~~~~~~~~~~

This file provides utility functions that are used within destiny
that are also useful for external consumption.

"""

import requests, os, sys, time
from datetime import datetime

from . import constants

URL_BASE = 'https://www.bungie.net/Platform/Destiny/'


def get_json(path, **kwargs):
    """
    Construct the appropriate syntax for a `requests.get()` call.
    :param path: uri path to append to base API path
    :kwarg api_key: API key to authorize access to Destiny API (optional)
    :kwarg params: Query parameters to pass to the `requests.get()` call
    :return: JSON object
    """
    url = URL_BASE + path
    params = kwargs.get('params')
    session = kwargs.get('session')
    if session is None:
        session = build_session()
    api_wait = 1
    while api_wait > 0:
        if params is None:
            response = session.get(url)
        else:
            response = session.get(url, params=params)
        response.raise_for_status()
        response = response.json()
        api_wait = response['ThrottleSeconds']
        if api_wait > 0 and response['ErrorCode'] in \
                constants.RATE_LIMIT_ERRORS:
            print("Hit rate limit, pausing for {0} seconds...".
                  format(api_wait))
            time.sleep(api_wait + 1)
    validate_json_response(response, url)
    if session is None:
        close_session(session, **kwargs)
    return response


def validate_json_response(response, url):
    """
    Check the response for error messages.
    :param response: the full JSON response
    :param url: url of the API response
    :return: True if response has no error message, throws error otherwise
    """
    if response['ErrorCode'] != 1:
        api_error = "[{ErrorCode}] {ErrorStatus}: {Message}"
        api_error = api_error.format(**response) + '\n' + url
        sys.exit(api_error)
    return True


def build_session(**kwargs):
    kwargs.setdefault('api_key', os.environ['BUNGIE_NET_API_KEY'])
    session = kwargs.get('session')
    if session is None:
        api_key = kwargs.get('api_key')
        headers = {'X-API-Key': api_key}
        session = requests.Session()
        session.headers.update(headers)
    return session


def close_session(session, **kwargs):
    existing_session = kwargs.get('session')
    if existing_session is None:
        session.close()


def crawl_data(destipy_object, data_path, throw_error=True):
    """
    Crawl dict tree via period-delimited string. Used to more easily
        reference data not explicitly gathered by Destipy.
    :param destipy_object: Destipy object with a data variable
        containing the JSON response to crawl
    :param data_path: period-delimited string that
        specifies which value to return
    :param throw_error: if false, hide message and don't throw error
    :return: single value, could be a string or int
    """
    path = data_path.split('.')
    # start at top of path
    loc = destipy_object.data
    for p in path:
        if p in loc.keys():
            # continue navigating
            loc = loc[p]
        elif throw_error:
            # print helpful message
            keys = loc.keys()
            object_class = destipy_object.__class__.__name__
            print("{object_class}: Using {path}, couldn't find {p}. "
                  "Possible values at this level:\n{keys}".format(**locals()))
            # throw a KeyError
            print(loc[p])
        else:
            return None
    return loc


def compare_dates(date_1, date_2, newest=True):
    """
    Helper function to convert string-formatted dates to datetime objects
    and compare which ones come first
    :param date_1: First date to compare
    :param date_2: Second date to compare
    :param newest: Determines if we return the newest of the two
        dates (if True), or the oldest (if False)
    :return: Newest or oldest date (based on :param newest:) as a string
    """
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    date_1_dt = datetime.strptime(date_1, fmt)
    date_2_dt = datetime.strptime(date_2, fmt)
    if newest is True:
        if date_1_dt >= date_2_dt:
            return date_1
        else:
            return date_2
    else:
        if date_1_dt <= date_2_dt:
            return date_1
        else:
            return date_2
