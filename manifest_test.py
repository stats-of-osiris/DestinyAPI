import os
import requests


URL_BASE = 'https://www.bungie.net/Platform/Destiny/'
PATH = 'Stats/PostGameCarnageReport/{0}'


def build_session(**kwargs):
    kwargs.setdefault('api_key', os.environ['BUNGIE_NET_API_KEY'])
    session = kwargs.get('session')
    if session is None:
        api_key = kwargs.get('api_key')
        headers = {'X-API-Key': api_key}
        session = requests.Session()
        session.headers.update(headers)
    return session

print(
    build_session().headers
)


def close_session(session, **kwargs):
    existing_session = kwargs.get('session')
    if existing_session is None:
        session.close()


def request_json(id, **kwargs):
    url = URL_BASE + PATH.format(id)
    params = kwargs.get('params')
    session = build_session(**kwargs)
    api_wait = 1
    while api_wait > 0:
        if params is None:
            response = session.get(url)
        else:
            response = session.get(url, params=params)
        response.raise_for_status()
        response = response.json()
        api_wait = response['ThrottleSeconds']

    close_session(session, **kwargs)
    return response

print(
    request_json('4892996696')
)

