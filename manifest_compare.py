import sqlite3
import json
import pandas as pd

fp = 'manifest/manifest.content'
conn = sqlite3.connect(fp)
table = 'DestinyInventoryItemDefinition'
query = 'SELECT * FROM {0}'.format(table)
items = pd.read_sql(query, conn, index_col='id')
ghorn_hash = 1274330687
hash_id = ghorn_hash & 0xffffffff
ghorn = json.loads(items.loc[hash_id].values[0])

bucket_tbl = 'DestinyInventoryBucketDefinition'
bucket_query = 'SELECT * FROM {0}'.format(bucket_tbl)
bucket_hash = ghorn['bucketTypeHash'] & 0xffffffff
bucket = json.loads(
    pd.read_sql(bucket_query, conn, index_col='id').loc[bucket_hash].values[0])

ghorn_series = pd.Series(
    {'name': ghorn['itemName'],
     'rarity': ghorn['tierTypeName'],
     'type': ghorn['itemTypeName'],
     'icon': ghorn['icon'],
     'category': bucket['bucketName'],
     'description': ghorn['itemDescription']}
)
print(ghorn_series.description)


class Manifest(object):
    def __init__(self):
        self.FILE_PATH = 'manifest/manifest.content'
        self.conn = sqlite3.connect(self.FILE_PATH)
        self.TABLES = {
            'items': 'DestinyInventoryItemDefinition',
            'buckets': 'DestinyInventoryBucketDefinition'
        }

    def get_item(self, hash):
        query = 'SELECT * FROM {0}'.format(
            self.TABLES['items']
        )
        items = pd.read_sql(query, self.conn, index_col='id')