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
        self.meta = utils.get_json(constants.API_PATHS
                                   ['get_manifest'].format(**locals()),
                                   **kwargs)
        self.meta_url = 'http://www.bungie.net{}'.format(
            self.meta['Response']['mobileWorldContentPaths']['en'])
        self.meta_version = self.meta['Response']['version']
        self.data = self.get_data()
        self.items = self.data['DestinyInventoryItemDefinition']
        self.activities = self.data['DestinyActivityDefinition']
        self.classes = self.data['DestinyClassDefinition']
        self.race = self.data['DestinyRaceDefinition']
        self.gender = self.data['DestinyGenderDefinition']
        self.stats = self.data['DestinyStatDefinition']
        self.stat_group = self.data['DestinyStatGroupDefinition']

    MAN_DIR = 'manifest'
    VERSION_PICKLE = '{}/man_version.pickle'.format(MAN_DIR)
    MANIFEST_FILE = '{}/manifest.content'.format(MAN_DIR)
    MANIFEST_PICKLE = '{}/manifest.pickle'.format(MAN_DIR)

    def update_version(self, db_version, version_file=VERSION_PICKLE,
                       directory=MAN_DIR):
        if not os.path.exists(directory):
            os.mkdir(directory)
        with open(version_file, 'wb') as version:
            pickle.dump(db_version, version)

    def check_version(self, version_file=VERSION_PICKLE):
        with open(version_file, 'rb') as version:
            current_version = pickle.load(version)
        return current_version

    def update_manifest(self, directory=MAN_DIR,
                        file_name=MANIFEST_FILE, **kwargs):
        zip_file = '{}/MAN_ZIP'.format(directory)
        with open(zip_file, 'wb') as zip_file:
            session = utils.build_session(**kwargs)
            response = session.get(self.meta_url, stream=True)
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
        with zipfile.ZipFile(zip_file) as zip_file:
            name = zip_file.namelist()
            zip_file.extractall()
        os.rename(name[0], file_name)
        os.remove(zip_file)
        print('Database downloaded')

    def crawl_manifest(self, manifest_file=MANIFEST_FILE,
                       manifest_pickle=MANIFEST_PICKLE):

        # Ensure that a manifest file exists
        if not os.path.exists(manifest_pickle):
            self.check_for_update()
        # Connect to the manifest
        conn = sqlite3.connect(manifest_file)
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
            # and the JSON as the values
            value_dict = {}
            hash_key = constants.MAN_HASH[table]
            for value in row_values:
                value_dict[value[hash_key]] = value
            # Add the table dict to our master dict,
            # with the table name as the key
            man_data[table] = value_dict
            with open(manifest_pickle, 'wb') as data:
                pickle.dump(man_data, data)

    def check_for_update(self, version_file=VERSION_PICKLE,
                         manifest_file=MANIFEST_FILE, **kwargs):
        # Create version file if it doesn't yet exist
        if not os.path.exists(version_file):
            self.update_version(self.meta_version)
        current_version = self.check_version()
        cond1 = self.meta_version != current_version
        cond2 = os.path.exists(manifest_file)
        if cond1 or not cond2:
            print('Update to Manifest Found')
            self.update_version(self.meta_version)
            print('Stored Version Updated')
            self.update_manifest(**kwargs)
            self.crawl_manifest()

    def get_data(self, manifest_pickle=MANIFEST_PICKLE,
                 update=False, directory=MAN_DIR, **kwargs):
        if update or not os.path.exists(directory):
            self.check_for_update(**kwargs)
        with open(manifest_pickle, 'rb') as data:
            man_data = pickle.load(data)
        return man_data
