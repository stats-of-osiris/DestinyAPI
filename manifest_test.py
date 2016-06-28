from pandas.io.json import json_normalize
import sqlite3 as sql
import json

# Connect to manifest
conn = sql.connect('manifest/manifest.content')
cursor = conn.cursor()

# Get items and convert to actual JSON
cursor.execute('SELECT json FROM DestinyInventoryItemDefinition')
rows = cursor.fetchall()
item_values = [json.loads(row[0]) for row in rows]

# Get buckets and convert to actual JSON
cursor.execute('SELECT json FROM DestinyInventoryBucketDefinition')
rows = cursor.fetchall()
bucket_values = [json.loads(row[0]) for row in rows]

# Reshape Items data into usable format
items = json_normalize(item_values)

items = items.loc[:,
                  ['itemHash', 'itemDescription', 'itemTypeName',
                   'tierTypeName', 'itemName', 'icon', 'itemType',
                   'bucketTypeHash']].set_index('itemHash')

items = items.rename(columns={
    'itemDescription': 'Description',
    'itemTypeName': 'Item Type',
    'tierTypeName': 'Rarity',
    'itemName': 'Name',
    'icon': 'Icon',
    'itemType': 'Item Type Id',
    'bucketTypeHash': 'bucketHash'
})

# Reshape Buckets data into usable format
buckets = json_normalize(bucket_values)

buckets = buckets.loc[:, ['bucketHash', 'bucketName']].set_index('bucketHash')

buckets = buckets.rename(columns={
    'bucketName': 'Item Group'
})

# Join Items and Buckets together into a single table
items = items.join(buckets, on='bucketHash')

items = items.drop('bucketHash', axis=1)

# Push back into our own Sqlite DB
new_conn = sql.connect('manifest/destipy.content')
items.to_sql('items', new_conn, if_exists='replace')
