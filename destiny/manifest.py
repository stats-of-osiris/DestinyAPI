# -*- coding: utf-8 -*-

"""
destiny.Manifest

This module handles the creation and updating of the Destiny Manifest
SQLite database and pulling values from said database.
"""

from . import utils, constants
import sqlite3
import json
import os
import sys
import zipfile
import datetime
import requests

# Meta information about manifest version and location from Destiny API
meta = utils.get_json(constants.API_PATHS['get_manifest'].format(**locals()))
meta_url = 'http://www.bungie.net{}'.format(
    meta['Response']['mobileWorldContentPaths']['en'])
meta_version = meta['Response']['version']


def update_version(db_version):
    """
    Update the current version of the locally stored manfiest file and when
    an update check was last performed
    :param db_version: new db version to store
    :return: None
    """
    payload = {
        'version': db_version,
        'date_checked': datetime.date.today().strftime('%Y-%m-%d')
    }
    if not os.path.exists(constants.MAN_DIR):
        os.mkdir(constants.MAN_DIR)
    with open(constants.MANIFEST['version_file'], 'w') as version:
        json.dump(payload, version)


def check_version():
    """
    Load the version JSON file
    :return: dict object including current version and date when last checked
    """
    try:
        with open(constants.MANIFEST['version_file'], 'r') as version:
            current_version = json.load(version)
    except:
        current_version = None
    return current_version


def update_manifest():
    """
    Download the zipped manifest file. Shows a progress bar where '=' == 2%
    :return: None
    """
    with open(constants.MANIFEST['zip'], 'wb') as zip_file:
        response = requests.get(meta_url, stream=True)
        total_length = response.headers.get('content-length')
        if total_length == 0:  # no content length header
            zip_file.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content():
                dl += len(data)
                zip_file.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write(
                    "\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()
    unzip_manifest()
    print('Database downloaded')


def unzip_manifest():
    """
    Helper function to unzip manifest file, and delete the zip file
    :return: None
    """
    with zipfile.ZipFile(constants.MANIFEST['zip']) as zip_file:
        name = zip_file.namelist()
        zip_file.extractall()
    os.rename(name[0], constants.MANIFEST['db'])
    os.remove(constants.MANIFEST['zip'])


def check_for_update(force_update=False):
    """
    When pulling data from the manifest, this will check for an updated version
    every 30 days, or if the `force_update` flag is flipped
    :param force_update: Defaults to False. If True, will force an API call
    to see if a new manifest version exists
    :return: None
    """
    # Create version file if it doesn't yet exist
    if not os.path.exists(constants.MANIFEST['version_file']):
        update_version(meta_version)

    # Store values from version_file
    current_version = check_version()['version']
    last_checked = datetime.datetime.strptime(
        check_version()['date_checked'], '%Y-%m-%d')

    # Download manifest if it doesn't exist
    if not os.path.exists(constants.MANIFEST['db']):
        print('Manifest not found. Downloading now.')
        update_manifest()
        update_version(meta_version)

    # Check every 30 days or when forced
    gt_30 = (datetime.date.today() - last_checked.date()).days >= 30
    if gt_30 or force_update:
        if meta_version != current_version:
            print('Update to Manifest Found')
            update_manifest()
        update_version(meta_version)


def get_row(hash_key, table, **kwargs):
    """
    Helper function to connect to the manifest sqlite database.
    :param hash_key:
    :param table: Table name to connect to as pulled from constants.TABLES
    :kwargs force_update: Defaults to False. If True, will force an API call
    to see if a new manifest version exists
    :return: Table from manifest as a DataFrame object
    """
    kwargs.setdefault('force_update', False)
    check_for_update(force_update=kwargs.get('force_update'))
    conn = sqlite3.connect(constants.MANIFEST['db'])
    c = conn.cursor()
    try:
        t = (hash(hash_key),)
        c.execute('SELECT json FROM {} WHERE id=?'.format(table), t)
        return json.loads(c.fetchone()[0])
    except TypeError:
        t = (hash_key - 4294967296,)
        c.execute('SELECT json FROM {} WHERE id=?'.format(table), t)
        return json.loads(c.fetchone()[0])


def get_table(table):
    conn = sqlite3.connect(constants.MANIFEST['db'])
    c = conn.cursor()
    c.execute('SELECT json FROM {}'.format(table))
    return c.fetchall()


def get_bucket(hash_key, **kwargs):
    bucket = get_row(hash_key, 'DestinyInventoryBucketDefinition', **kwargs)
    return bucket['bucketName']


def get_item(hash_key, **kwargs):
    item = get_row(hash_key, 'DestinyInventoryItemDefinition', **kwargs)
    bucket_hash = item['bucketTypeHash']
    bucket = get_bucket(bucket_hash)
    try:
        description = item['itemDescription']
    except KeyError:
        description = None
    return {
            'item_id': item['itemHash'],
            'item_name': item['itemName'],
            'item_rarity': item['tierTypeName'],
            'item_type': item['itemTypeName'],
            'icon': item['icon'],
            'item_description': description,
            'item_category': bucket
    }


def get_items(hash_keys: list, **kwargs):
    items = [get_item(key, **kwargs) for key in hash_keys]
    return items


def get_map(hash_key, **kwargs):
    game_map = get_row(hash_key, 'DestinyActivityDefinition', **kwargs)
    return {k: game_map[k] for k in game_map.keys() & {
        'activityName', 'pgcrImage', 'activityDescription', 'activityHash'
    }}


def get_activity_type(hash_key, **kwargs):
    activity_type = get_row(hash_key, 'DestinyActivityTypeDefinition')
    return activity_type['activityTypeName']
