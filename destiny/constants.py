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

# API Timestamp format
TS = '%Y-%m-%dT%H:%M:%SZ'

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
    'kills_total': 'kills',
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
                   'weaponPrecisionKillsAutoRifle'],
    'kills_hcannon': ['weaponKillsHandCannon',
                      'weaponPrecisionKillsHandCannon'],
    'kills_scout': ['weaponKillsScoutRifle',
                    'weaponPrecisionKillsScoutRifle'],
    'kills_pulse': ['weaponKillsPulseRifle',
                    'weaponPrecisionKillsPulseRifle']
}

SPECIAL_WEAPON_STATS = {
    'kills_sniper': ['weaponKillsSniper',
                     'weaponPrecisionKillsSniper'],
    'kills_shotgun': ['weaponKillsShotgun',
                      'weaponPrecisionKillsShotgun'],
    'kills_fusion': ['weaponKillsFusionRifle',
                     'weaponPrecisionKillsFusionRifle'],
    'kills_sidearm': ['weaponKillsSidearm',
                      'weaponPrecisionKillsSidearm']
}

HEAVY_WEAPON_STATS = {
    'kills_rocket': ['weaponKillsRocketLauncher',
                     'weaponPrecisionKillsRocketLauncher'],
    'kills_hmg': ['weaponKillsMachineGun',
                  'weaponPrecisionKillsMachineGun'],
    'kills_sword': ['weaponKillsSword',
                    'weaponPrecisionKillsSword']
}

MEDALS = {
    'medalsAbilityArcLightningKillMulti': {
        'image': '/common/destiny_content/icons/icon_mf4406ecbf05f2e6263a856c900756a6d.png',
        'description': 'Defeat 3 opposing Guardians with a single Stormtrance activation.',
        'name': 'storm_bringer'
    },
    'medalsAbilityGhostGunKillMulti': {
        'image': '/common/destiny_content/icons/icon_m127ecce38e366af72054570a6fdbecd9.png',
        'description': 'Kill 3 enemies with a single Golden Gun charge.',
        'name': 'way_of_gun'
    },
    'medalsAbilityHavocKillMulti': {
        'image': '/common/destiny_content/icons/icon_m3ec59d88f90dc142b29208f5079ebe60.png',
        'description': 'Kill 3 enemies with a single Fist of Havoc.',
        'name': 'cry_havoc'
    },
    'medalsAbilityNovaBombKillMulti': {
        'image': '/common/destiny_content/icons/icon_m24e361d76b433ef6c55848a54256d50c.png',
        'description': 'Kill 3 enemies with a single Nova Bomb.',
        'name': 'space_magic'
    },
    'medalsAbilityRadianceGrenadeKillMulti': {
        'image': '/common/destiny_content/icons/icon_ma5e571c8b02316e43f2b304d04670c35.png',
        'description': 'Kill 3 enemies with grenades while Radiance is active.',
        'name': 'scorched_earth'
    },
    'medalsAbilityShadowStrikeKillMulti': {
        'image': '/common/destiny_content/icons/icon_m5ef54943e06cb079510494981d7908a2.png',
        'description': 'Kill 3 enemies in a single Arc Blade charge.',
        'name': 'gutted'
    },
    'medalsAbilityThermalHammerKillMulti': {
        'image': '/common/destiny_content/icons/icon_m2f168c48897ba93ba070d440f7d2f701.png',
        'description': 'Defeat 3 opposing Guardians with a single Hammer of Sol activation.',
        'name': 'hammer_tongs'
    },
    'medalsAbilityVoidBowKillMulti': {
        'image': '/common/destiny_content/icons/icon_mf3d36ba306e3709cde0c33a241997412.png',
        'description': 'Rapidly defeat 3 opposing Guardians with Shadowshot.',
        'name': 'wild_hunt'
    },
    'medalsAbilityWardDeflect': {
        'image': '/common/destiny_content/icons/icon_m8fee8c2bd6fed4a5154fea2fedf9035d.png',
        'description': 'Block fatal damage within 2 seconds of casting Ward of Dawn.',
        'name': 'blast_shield'
    },
    'medalsActivityCompleteCycle': {
        'image': '/common/destiny_content/icons/icon_mdb8d7a333bf5e55553107cfaa643c77e.png',
        'description': 'Complete a round with at least a Primary, Special, Heavy, Grenade, Melee, and Super kill.',
        'name': 'cycle'
    },
    'medalsActivityCompleteDeathless': {
        'image': '/common/destiny_content/icons/icon_mb092f95c5860abf29bcb6548b9e44056.png',
        'description': 'Complete a match with a minimum of 15 kills without dying or being downed.',
        'name': 'mark_of_unbroken'
    },
    'medalsActivityCompleteHighestScoreLosing': {
        'image': '/common/destiny_content/icons/icon_m6fcd36765e6c7b5b4278dd4996ab7629.png',
        'description': 'Achieve the highest score in a match despite your team\'s loss.',
        'name': 'bright_side'
    },
    'medalsActivityCompleteHighestScoreWinning': {
        'image': '/common/destiny_content/icons/icon_m1ac4982244fdb59cfd334e731503aced.png',
        'description': 'Achieve the highest score in a match while leading your team to victory.',
        'name': 'best_around'
    },
    'medalsActivityCompleteLonewolf': {
        'image': '/common/destiny_content/icons/icon_m4d51c2cb6c2159034432dc7cee6d914c.png',
        'description': 'In a team game, finish first on your team with no assists.',
        'name': 'lone_wolf'
    },
    'medalsActivityCompleteVictoryBlowout': {
        'image': '/common/destiny_content/icons/icon_mcb93d453dae2cc6c6e920f1988086817.png',
        'description': 'In a match that reaches the score limit, double the opposing team\'s score.',
        'name': 'decisive_victory'
    },
    'medalsActivityCompleteVictoryEliminationPerfect': {
        'image': '/common/destiny_content/icons/icon_m7f5451453a58793961439b2c2ba9f3a9.png',
        'description': 'As a team, win an Elimination match where no one on your team dies.',
        'name': 'bulletproof'
    },
    'medalsActivityCompleteVictoryEliminationShutout': {
        'image': '/common/destiny_content/icons/icon_m9ecbbcf34149c6a1c8c845ac0d0b9091.png',
        'description': 'As a team, win an Elimination match without being wiped.',
        'name': 'annihilation'
    },
    'medalsAvenger': {
        'image': '/common/destiny_content/icons/icon_m324a5681ecdd1ff57498932167c794b3.png',
        'description': 'Avenge a defeated teammate.',
        'name': 'avenger'
    },
    'medalsBuddyResurrectionMulti': {
        'image': '/common/destiny_content/icons/icon_m80feb7e68d551509fdcde39af56c2af9.png',
        'description': 'Quickly revive 2 downed allies.',
        'name': 'medic'
    },
    'medalsBuddyResurrectionSpree': {
        'image': '/common/destiny_content/icons/icon_me64c76c9579f691ea1b8868de09d98ae.png',
        'description': 'In a single life, revive 5 downed allies.',
        'name': 'angel_light'
    },
    'medalsCloseCallTalent': {
        'image': '/common/destiny_content/icons/icon_m915391b17f5c469999f22d68a79d9beb.png',
        'description': 'Kill an enemy who nearly killed you.',
        'name': 'narrow_escape'
    },
    'medalsEliminationLastStandKill': {
        'image': '/common/destiny_content/icons/icon_meef309ddbf708b5a5901d9179548713f.png',
        'description': 'Kill an enemy as the last Guardian standing on your team.',
        'name': 'never_say_die'
    },
    'medalsEliminationLastStandRevive': {
        'image': '/common/destiny_content/icons/icon_m2e40fd761d2d76d6be501e8f3f07cb6c.png',
        'description': 'Revive an ally as the last Guardian standing on your team.',
        'name': 'from_the_brink'
    },
    'medalsEliminationWipeQuick': {
        'image': '/common/destiny_content/icons/icon_mc6d31ef5e788b733b1b3326dc23cd250.png',
        'description': 'As a fireteam, defeat the enemy team in the first 30 seconds of a round.',
        'name': 'ace'
    },
    'medalsEliminationWipeSolo': {
        'image': '/common/destiny_content/icons/icon_md8545a9d8956c0ca2a700d75fa7a5f72.png',
        'description': 'Singlehandedly wipe the enemy team.',
        'name': 'wrecking_ball'
    },
    'medalsFirstBlood': {
        'image': '/common/destiny_content/icons/icon_mbacd26f29970ada09f819d6e308285cb.png',
        'description': 'Score the first kill in a match.',
        'name': 'first_blood'
    },
    'medalsGrenadeKillStick': {
        'image': '/common/destiny_content/icons/icon_m521ab81bf41b7dfcbebad5626bb56fb8.png',
        'description': 'Kill an enemy by sticking them with a grenade.',
        'name': 'get_it_off'
    },
    'medalsHazardKill': {
        'image': '/common/destiny_content/icons/icon_m13a859c5047ecb0fc5388156398ed4be.png',
        'description': 'Kill an enemy with an exploding object.',
        'name': 'hazard_pay'
    },
    'medalsHunterKillInvisible': {
        'image': '/common/destiny_content/icons/icon_m0b4e7db175edc2b7b0bfd95b6cfd3f08.png',
        'description': 'Kill an invisible enemy.',
        'name': 'see_you'
    },
    'medalsKillAssistSpree': {
        'image': '/common/destiny_content/icons/icon_m8dbf600866a4d744af7159f425e4178d.png',
        'description': 'In a single life, assist your allies on 3 kills.',
        'name': 'unsung_hero'
    },
    'medalsKillHeadshot': {
        'image': '/common/destiny_content/icons/icon_m0f3d34a0e6cf3aa527172d899a7a97d2.png',
        'description': 'In a single life, kill 3 enemies with headshots.',
        'name': 'bullseye'
    },
    'medalsKillMulti2': {
        'image': '/common/destiny_content/icons/icon_m746baced6bbe4a4c6e7d98aa6345617d.png',
        'description': 'Rapidly kill 2 enemies.',
        'name': 'double_down'
    },
    'medalsKillMulti3': {
        'image': '/common/destiny_content/icons/icon_m1f584310fb18bb5c0fa21e81e295fee5.png',
        'description': 'Rapidly kill 3 enemies.',
        'name': 'triple_down'
    },
    'medalsKillPostmortem': {
        'image': '/common/destiny_content/icons/icon_mdae6855231eb8bf695d6a97a519c9d43.png',
        'description': 'Kill one or more enemies after you have died.',
        'name': 'postmortem'
    },
    'medalsKillSpree1': {
        'image': '/common/destiny_content/icons/icon_me7019dac10f7230fb824c1dc389257a0.png',
        'description': 'In a single life, kill 5 enemies.',
        'name': 'merciless'
    },
    'medalsKillSpree2': {
        'image': '/common/destiny_content/icons/icon_mb313be68b3fcf783cacb5a529e3e0f22.png',
        'description': 'In a single life, kill 10 enemies.',
        'name': 'relentless'
    },
    'medalsKillSpree3': {
        'image': '/common/destiny_content/icons/icon_mc364a999ecb72c893f783e7b5b652f05.png',
        'description': 'In a single life, kill 15 enemies.',
        'name': 'reign_terror'
    },
    'medalsKillSpreeNoDamage': {
        'image': '/common/destiny_content/icons/icon_mab1a465b2c8fc80b5f867f2486db4f81.png',
        'description': 'Defeat 7 opposing Guardians while taking no damage.',
        'name': 'phantom'
    },
    'medalsKilljoy': {
        'image': '/common/destiny_content/icons/icon_m297f0d590aff33be59871d6c4a4673e1.png',
        'description': 'Shut down an enemy\'s kill streak.',
        'name': 'enforcer'
    },
    'medalsKilljoyMega': {
        'image': '/common/destiny_content/icons/icon_mae5e8eebd9f38f37572694b26e970e66.png',
        'description': 'Stop an enemy on a 15+ kill streak.',
        'name': 'end_of_line'
    },
    'medalsMeleeKillHunterThrowingKnifeHeadshot': {
        'image': '/common/destiny_content/icons/icon_mda8430b7c74ea0485026a9f156ffc11f.png',
        'description': 'Fatally headshot an enemy with a Throwing Knife.',
        'name': 'stick_around'
    },
    'medalsPaybackKill': {
        'image': '/common/destiny_content/icons/icon_mbc31aa22e2fd55d1e79a77274f39eb65.png',
        'description': 'Defeat the opposing Guardian who killed you last.',
        'name': 'payback'
    },
    'medalsRadianceShutdown': {
        'image': '/common/destiny_content/icons/icon_m7a1ba4190b056693e497d1ac1e05d6b2.png',
        'description': 'Defeat a Warlock within 3 seconds of their self-reviving with Radiance.',
        'name': 'stay_down'
    },
    'medalsRescue': {
        'image': '/common/destiny_content/icons/icon_mfc8d74051a3ed141a66cbcc99d711158.png',
        'description': 'Defend an ally from enemy fire.',
        'name': 'overwatch'
    },
    'medalsUnknown': {
        'image': None,
        'description': None,
        'name': 'Medal: Unknown'
    },
    'medalsWeaponAutoRifleKillSpree': {
        'image': '/common/destiny_content/icons/icon_m8f1fe9c611ec24e7a1c4f58cb840555d.png',
        'description': 'In a single life, defeat 5 opposing Guardians with an Auto Rifle.',
        'name': 'automatic'
    },
    'medalsWeaponFusionRifleKillSpree': {
        'image': '/common/destiny_content/icons/icon_m2201e64d9f98ea2a8d22ed03ec389bd9.png',
        'description': 'Kill 3 opponents with a Fusion Rifle without switching weapons or reloading.',
        'name': 'master_blaster'
    },
    'medalsWeaponHandCannonHeadshotSpree': {
        'image': '/common/destiny_content/icons/icon_m7b75faac50066f7aed7c9c5c3357a6d0.png',
        'description': 'In a single life, kill 3 opponents with Hand Cannon headshots.',
        'name': 'dead_mans_hand'
    },
    'medalsWeaponMachineGunKillSpree': {
        'image': '/common/destiny_content/icons/icon_md41b3cadbc4c6d3ec0a7d2aaf419fbe7.png',
        'description': 'Kill 3 enemies with a Machine Gun without switching weapons or reloading.',
        'name': 'machine_lord'
    },
    'medalsWeaponPulseRifleKillSpree': {
        'image': '/common/destiny_content/icons/icon_mb1919d9fa1432844e7c0735855e8d5d9.png',
        'description': 'In a single life, defeat 5 opposing Guardians with a Pulse Rifle.',
        'name': 'finger_on_pulse'
    },
    'medalsWeaponRocketLauncherKillSpree': {
        'image': '/common/destiny_content/icons/icon_mde7d77b45e7c96be4b43a70b2370dead.png',
        'description': 'Kill 3 enemies with rockets in less than a second.',
        'name': 'Splash Damage'
    },
    'medalsWeaponScoutRifleKillSpree': {
        'image': '/common/destiny_content/icons/icon_m19f521f962f4aed842251ca89c508196.png',
        'description': 'In a single life, defeat 5 opposing Guardians with a Scout Rifle.',
        'name': 'scouts_honor'
    },
    'medalsWeaponShotgunKillSpree': {
        'image': '/common/destiny_content/icons/icon_m12b0c60086f8ee07b9d92685e299ae4c.png',
        'description': 'Kill 3 enemies with a Shotgun without switching weapons or reloading.',
        'name': 'buckshot_bruiser'
    },
    'medalsWeaponSidearmKillSpree': {
        'image': '/common/destiny_content/icons/icon_me8f0611a5aba8cc115e2eb5485373b7d.png',
        'description': 'In a single life, defeat 3 opposing Guardians with a Sidearm.',
        'name': 'sidekick'
    },
    'medalsWeaponSniperRifleHeadshotSpree': {
        'image': '/common/destiny_content/icons/icon_mbdb0882056e3a6393e4bf6bea4b89061.png',
        'description': 'Kill 2 enemies with Sniper Rifle headshots without switching weapons or reloading.',
        'name': 'marksman'
    },
    'medalsWeaponSwordKillSpree': {
        'image': '/common/destiny_content/icons/icon_m9f8ac92b23f11d46419cb82935682b79.png',
        'description': 'Rapidly defeat 3 enemies with a Heavy Sword.',
        'name': 'sword_gun_fight'
    },
    'medalsWinningScore': {
        'image': '/common/destiny_content/icons/icon_m12dc39d05335f02111561718f0582144.png',
        'description': 'Score the winning points in a match.',
        'name': 'nail_in_coffin'
    }
}

CORE_STATS = ['kills', 'deaths', 'resurrectionsPerformed',
              'resurrectionsReceived', 'orbsGathered', 'orbsDropped',
              'longestSingleLife', 'longestKillSpree', 'precisionKills',
              'totalKillDistance'
              ]
