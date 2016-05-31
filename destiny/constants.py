# API endpoints
API_PATHS = {
    # used in Player.set_id()
    'get_membership_id_by_display_name': '{self.console_id}/Stats/'
                                         'GetMembershipIdByDisplayName/'
                                         '{self.name}/',
    # used in Player.__init__()
    'get_destiny_account_summary': '{self.console_id}/Account/'
                                   '{self.id}/Summary',
    # used in Game.__init__()
    'get_post_game_carnage_report': 'Stats/PostGameCarnageReport/'
                                    '{self.id}',
    # used in Game.games_from_guardian()
    'get_activity_history': 'Stats/ActivityHistory/{guardian.console_id}/'
                            '{guardian.player_id}/{guardian.id}'
}

# Platform decode
PLATFORMS = {
    'xbox': '1',
    'psn':  '2'
}

# Guardian class decode from hash
GUARDIAN_TYPE = {
    3655393761: 'Titan',
    2271682572: 'Warlock',
    671679327:  'Hunter'
}

# Guardian race decode from hash
GUARDIAN_RACE = {
    2803282938: 'Awoken',
    898834093:  'Exo',
    3887404748: 'Human'
}

# Guardian gender decode from hash
GUARDIAN_GENDER = {
    3111576190: 'Male',
    2204441813: 'Female'
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

# List of key stats targeted for report
KEY_STATS = [
    # Player & Game Info
    {'path':        'player.destinyUserInfo.displayName',
     'column_name': 'Player',
     'team':        'both'},
    {'path':        'values.team.basic.displayValue',
     'column_name': 'Team',
     'team':        'both'},
    {'path':        'values.team.basic.displayValue',
     'column_name': 'Team Score',
     'team':        'both'},
    {'path':        'standing.displayValue',
     'column_name': 'Standing',
     'team':        'both'},
    {'path':        'values.activityDurationSeconds.basic.displayValue',
     'column_name': 'Team',
     'team':        'both'},
    # Player Performance
    {'path':        'extended.values.kills.basic.value',
     'column_name': 'Kills',
     'team':        'both'},
    {'path':        'extended.values.deaths.basic.value',
     'column_name': 'Deaths',
     'team':        'both'},
    {'path':        'extended.values.assists.basic.value',
     'column_name': 'Assists',
     'team':        'both'},
    {'path':        'extended.values.resurrectionsPerformed.basic.value',
     'column_name': 'Resurrections Performed',
     'team':        'both'},
    {'path':        'extended.values.resurrectionsReceived.basic.value',
     'column_name': 'Resurrections Received',
     'team':        'us'},
    {'path':        'extended.values.orbsGenerated.basic.value',
     'column_name': 'Orbs Generated',
     'team':        'us'},
    {'path':        'extended.values.orbsGathered.basic.value',
     'column_name': 'Orbs Gathered',
     'team':        'us'},
    {'path':        'extended.values.Lifespan.basic.value',
     'column_name': 'Longest Life',
     'team':        'us'},
    {'path':        'extended.values.longestKillSpree.basic.value',
     'column_name': 'Longest Kill Spree',
     'team':        'us'},
    # Weapon Use & Medals
    {'path':        'extended.values.weaponBestType.basic.displayValue',
     'column_name': 'Best Weapon Type',
     'team':        'us'},
    {'path':        'extended.values.medalsEliminationLastStandKill.basic.value',
     'column_name': 'Never Say Die',
     'team':        'us'},
    {'path':        'extended.values.medalsEliminationLastStandRevive.basic.value',
     'column_name': 'From The Brink',
     'team':        'us'},
    {'path':        'extended.values.medalsEliminationWipeQuick.basic.value',
     'column_name': 'Wrecking Ball',
     'team':        'us'},
    {'path':        'extended.values.medalsCloseCallTalent.basic.value',
     'column_name': 'Close Call',
     'team':        'us'},
    # Primaries
    {'path':        'extended.values.weaponKillsAutoRifle.basic.value',
     'column_name': 'Auto Rifle Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponPrecisionKillsAutoRifle.basic.value',
     'column_name': 'Auto Rifle Prec Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsHandCannon.basic.value',
     'column_name': 'Hand Cannon Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponPrecisionKillsHandCannon.basic.value',
     'column_name': 'Hand Cannon Prec Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsPulseRifle.basic.value',
     'column_name': 'Pulse Rifle Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponPrecisionKillsPulseRifle.basic.value',
     'column_name': 'Pulse Rifle Prec Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsScoutRifle.basic.value',
     'column_name': 'Scout Rifle Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponPrecisionKillsScoutRifle.basic.value',
     'column_name': 'Scout Rifle Prec Kills',
     'team':        'us'},
    # Secondaries
    {'path':        'extended.values.weaponKillsSniper.basic.value',
     'column_name': 'Sniper Rifle Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponPrecisionKillsSniper.basic.value',
     'column_name': 'Sniper Rifle Prec Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsShotgun.basic.value',
     'column_name': 'Shotgun Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsFusionRifle.basic.value', # doesn't appear to be working
     'column_name': 'Fusion Rifle Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsSideArm.basic.value', # doesn't appear to be working
     'column_name': 'Sidearm Kills',
     'team':        'us'},
    # Heavy Weapons, Melees, Grenades, Supers
    {'path':        'extended.values.weaponKillsRocketLauncher.basic.value',
     'column_name': 'Rocket Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsMachineGun.basic.value', #doesn't appear to be working
     'column_name': 'HMG Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsMelee.basic.value',
     'column_name': 'Melee Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsGrenade.basic.value',
     'column_name': 'Grenade Kills',
     'team':        'us'},
    {'path':        'extended.values.weaponKillsSuper.basic.value',
     'column_name': 'Super Kills',
     'team': 'us'}
]
