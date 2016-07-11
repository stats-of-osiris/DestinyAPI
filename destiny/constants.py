# -*- coding: utf-8 -*-

"""
stats_osiris.constants

Collection of various constants that are used to access the Bungie.net API,
the Destiny Manifest, etc.
"""

# API endpoints
API_PATHS = {
    # used in Player.set_id()
    'get_membership_id_by_display_name': '{self.console_id}/Stats/'
                                         'GetMembershipIdByDisplayName/'
                                         '{self.player_name}/',
    # used in Player.__init__()
    'get_destiny_account_summary': '{self.console_id}/Account/'
                                   '{self.player_id}/Summary',
    # used in Game.__init__()
    'get_post_game_carnage_report': 'Stats/PostGameCarnageReport/'
                                    '{self.activity_id}',
    # used in Game.games_from_guardian()
    'get_activity_history': 'Stats/ActivityHistory/{guardian.console_id}/'
                            '{guardian.player_id}/{guardian.guardian_id}',
    'get_manifest': 'Manifest/',
    'get_character': '{self.console_id}/Account/{self.player_id}/'
                     'Character/{self.guardian_id}/'
}

# Platform decode
PLATFORMS = {
    'xbox': 1,
    'psn':  2
}

# File paths to Manifest files
MAN_DIR = 'manifest'

MANIFEST = {
    'version_file': '{}/man_version.json'.format(MAN_DIR),
    'db': '{}/manifest.content'.format(MAN_DIR),
    'zip': '{}/man_zip'.format(MAN_DIR)
}

# Quick hash lookups
GENDER = {
    2204441813: 'Female',
    3111576190: 'Male'
}

CLASS = {
    671679327: 'Hunter',
    3655393761: 'Titan',
    2271682572: 'Warlock'
}

RACE = {
    2803282938: 'Awoken',
    898834093: 'Exo',
    3887404748: 'Human'
}

# List of possible activity modes
ACTIVITY_MODES = {
    'none':             '0',
    'story':            '2',
    'strike':           '3',
    'raid':             '4',
    'all_pvp':          '5',
    'patrol':           '6',
    'all_pve':          '7',
    'pvp_intro':        '8',
    '3_vs_3':           '9',
    'control':          '10',
    'lockdown':         '11',
    'team':             '12',
    'free_for_all':     '13',
    'ffa':              '13',
    'trials':           '14',
    'trials_of_osiris': '14',
    'doubles':          '15',
    'nightfall':        '16',
    'heroic':           '17',
    'all_strikes':      '18',
    'iron_banner':      '19',
    'ib':               '19',
    'all_arena':        '20',
    'arena':            '21',
    'arena_challenge':  '22',
    'elimination':      '23',
    'rift':             '24'
}

# List of throttling errors
RATE_LIMIT_ERRORS = [31, 35, 36, 37]

# List of stats to pull for reports where 'k: v' is 'column name: API name'
KEY_STATS = {
    'kills': 'kills',
    'deaths': 'deaths',
    'assists': 'assists',
    'rez_count': 'resurrectionsPerformed',
    'rezzed_count': 'resurrectionsReceived',
    'orbs_gathered': 'orbsGathered',
    'orbs_dropped': 'orbsDropped',
    'longest_life': 'longestSingleLife',
    'longest_kill_spree': 'longestKillSpree',
    'kills_precision': 'precisionKills',
    'kills_melee': 'weaponKillsMelee',
    'kills_grenade': 'weaponKillsGrenade',
    'kills_super': 'weaponKillsSuper',
    'medals_first_blood': 'medalsFirstBlood',
    'medals_never_say_die': 'medalsEliminationLastStandKill',
    'medals_from_the_brink': 'medalsEliminationLastStandRevive',
    'medals_back_in_action': 'medalsComebackKill',
    'medals_wrecking_ball': 'medalsEliminationWipeSolo',
    'medals_ace': 'medalsEliminationWipeQuick',
    'medals_close_call': 'medalsCloseCallTalent',
    'medals_annihilation': 'medalsActivityCompleteVictoryEliminationShutout'
}

RATIOS = {
    'avg_life': 'averageLifespan',
    'avg_kill_distance': 'averageKillDistance',
    'kd_ratio': 'killsDeathsRatio'
}

PRIMARY_WEAPON_STATS = {
    'kills_auto': ['weaponKillsAutoRifle',
                   'weaponKillsPrecisionKillsAutoRifle'],
    'kills_hcannon': ['weaponKillsHandCannon',
                      'weaponKillsPrecisionKillsHandCannon'],
    'kills_scout': ['weaponKillsScoutRifle',
                    'weaponKillsPrecisionKillsScoutRifle'],
    'kills_pulse': ['weaponKillsPulseRifle',
                    'weaponKillsPrecisionKillsPulseRifle']
}

SPECIAL_WEAPON_STATS = {
    'kills_sniper': ['weaponKillsSniper',
                     'weaponKillsPrecisionKillsSniper'],
    'kills_shotgun': ['weaponKillsShotgun',
                      'weaponKillsPrecisionKillsShotgun'],
    'kills_fusion': ['weaponKillsFusionRifle',
                     'weaponKillsPrecisionKillsFusionRifle'],
    'kills_sidearm': ['weaponKillsSidearm',
                      'weaponKillsPrecisionKillsSidearm']
}

HEAVY_WEAPON_STATS = {
    'kills_rocket': ['weaponKillsRocketLauncher',
                     'weaponKillsPrecisionKillsRocketLauncher'],
    'kills_hmg': ['weaponKillsMachineGun',
                  'weaponKillsPrecisionKillsMachineGun'],
    'kills_sword': ['weaponKillsSword',
                    'weaponKillsPrecisionKillsSword']
}

