import json
import destiny
import requests
import os

headers = {'X-API-Key': os.environ['BUNGIE_NET_API_KEY']}
r = requests.get('https://www.bungie.net/Platform/Destiny/2/'
                 'Stats//JohnOfMars', headers=headers)
print(json.dumps(r.json(), indent=4))