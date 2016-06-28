from __future__ import print_function
import json
import pandas as pd

# items = pd.read_sql('items', 'sqlite:///manifest/destipy.content')
# print(items.head())

uri = 'sqlite:///manifest/manifest.content'
items = pd.read_sql('DestinyInventoryItemDefinition', uri)
print(items.head())
