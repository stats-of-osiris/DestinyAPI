# -*- coding: utf-8 -*-

"""
destiny.Manifest

This module handles the creation and updating of the Destiny Manifest
SQLite database and pulling values from said database.
"""

from . import utils, constants
import zipfile, sqlite3, json, os, pickle, sys


class Manifest(object):
    """
    Access the data contained in Destiny's Manifest database. This is used
    to interpret the hashes that are present in many API calls.
    """
    def __init__(self, **kwargs):
        self.data = pull_manifest(**kwargs)
        self.items = self.data['DestinyInventoryItemDefinition']
        self.activities = self.data['DestinyActivityDefinition']
        self.classes = self.data['DestinyClassDefinition']
        self.race = self.data['DestinyRaceDefinition']
        self.gender = self.data['DestinyGenderDefinition']
        self.stats = self.data['DestinyStatDefinition']
        self.stat_group = self.data['DestinyStatGroupDefinition']


def pull_manifest(**kwargs):
    """
    This function checks with the Destiny API for updates, and if one is
    detected downloads, unzips, and prepares the database for consumption.
    :param kwargs: Used in case a session is passed through.
    :return: The entire Manifest database in dict form.
    """
    # Find url of the manifest zip file
    api_call = utils.get_json(constants.API_PATHS
                              ['get_manifest'].format(**locals()),
                              **kwargs)
    db_url = 'http://www.bungie.net{}'.format(
        api_call['Response']['mobileWorldContentPaths']['en'])
    db_version = api_call['Response']['version']
    # Store version # of db as pickle for later reference
    if not os.path.exists('manifest'):
        os.mkdir('manifest')
    version_file = 'manifest/man_version.pickle'
    if not os.path.exists(version_file):
        with open(version_file, 'wb+') as version:
            pickle.dump(db_version, version)
    with open(version_file, 'rb') as version:
        current_version = pickle.load(version)
    # Download new manifest if new version detected or it doesn't exist
    if db_version != current_version\
            or not os.path.exists('manifest/manifest.content'):
        print('Update to Manifest Found')
        with open(version_file, 'wb') as version:
            pickle.dump(db_version, version)
        print('Stored version updated')
        print('Retrieving database, this might take a while...')
        with open('manifest/MAN_ZIP', 'wb') as zip_file:
            session = utils.build_session(**kwargs)
            response = session.get(db_url, stream=True)
            total_length = response.headers.get('content-length')
            if total_length == 0:  # no content length header
                utils.close_session(session, **kwargs)
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
                utils.close_session(session, **kwargs)
        with zipfile.ZipFile('manifest/MAN_ZIP') as zip_file:
            name = zip_file.namelist()
            zip_file.extractall()
        os.rename(name[0], 'manifest/manifest.content')
        os.remove('manifest/MAN_ZIP')
        print('Database unzipped')
        # Connect to the manifest
        conn = sqlite3.connect('manifest/manifest.content')
        # Create the cursor object
        cursor = conn.cursor()
        # Initialize master dict where all db tables will be stored
        man_data = {}
        # Iterate through each table in the db and pull out the JSON
        for table in constants.MAN_HASH.keys():
            cursor.execute('SELECT json FROM {}'.format(table))
            # The result retrieved below is a list of tuples
            rows = cursor.fetchall()
            # Parse out the tuples into the actual JSON values
            row_values = [json.loads(row[0]) for row in rows]
            # Create a dict of the db table with the hashes as the keys
            #  and the JSON as the values
            value_dict = {}
            hash_key = constants.MAN_HASH[table]
            for value in row_values:
                value_dict[value[hash_key]] = value
            # Add the table dict to our master dict,
            # with the table name as the key
            man_data[table] = value_dict
            with open('manifest/manifest.pickle', 'wb') as data:
                pickle.dump(man_data, data)
    with open('manifest/manifest.pickle', 'rb') as data:
        man_data = pickle.load(data)
    return man_data
