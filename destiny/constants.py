# platform decode
PLATFORMS = {
            'xbox'      : '1',
            'psn'       : '2'
}

# Character class decode from hash
CLASS = {
    3655393761: 'Titan',
    2271682572: 'Warlock',
    671679327: 'Hunter'
}

# Character race decode from hash
RACE = {
    2803282938: 'Awoken',
    898834093: 'Exo',
    3887404748: 'Human'
}

# Character gender decode from hash
GENDER = {
    3111576190: 'Male',
    2204441813: 'Female'
}

# List of key stats targeted for report
KEY_STATS = [
        #Player & Game Info
            {'path'         : 'player.destinyUserInfo.displayName',
             'column_name'  : 'Player',
             'team'         : 'both'},
            {'path'         : 'values.team.basic.displayValue',
             'column_name'  : 'Team',
             'team'         : 'both'},
            {'path'         : 'values.team.basic.displayValue',
             'column_name'  : 'Team Score',
             'team'         : 'both'},
            {'path'         : 'standing.displayValue', 
             'column_name'  : 'Standing',
             'team'         : 'both'},
            {'path'         : 'values.activityDurationSeconds.basic.displayValue',
             'column_name'  : 'Team',
             'team'         : 'both'},

        #Player Performance
            {'path'         : 'extended.values.kills.basic.value',
             'column_name'  : 'Kills',
             'team'         : 'both'},
            {'path'         : 'extended.values.deaths.basic.value',
             'column_name'  : 'Deaths',
             'team'         : 'both'},
            {'path'         : 'extended.values.assists.basic.value',
             'column_name'  : 'Assists',
             'team'         : 'both'},
            {'path'         : 'extended.values.resurrectionsPerformed.basic.value',
             'column_name'  : 'Resurrections Performed',
             'team'         : 'both'},
            {'path'         : 'extended.values.resurrectionsReceived.basic.value',
             'column_name'  : 'Resurrections Received',
             'team'         : 'us'},
            {'path'         : 'extended.values.orbsGenerated.basic.value',
             'column_name'  : 'Orbs Generated',
             'team'         : 'us'},
            {'path'         : 'extended.values.orbsGathered.basic.value',
             'column_name'  : 'Orbs Gathered',
             'team'         : 'us'},

        #Weapon Use & Medals
            {'path'         : 'extended.values.weaponBestType.basic.displayValue',
             'column_name'  : 'Best Weapon Type',
             'team'         : 'us'},

            {'path'         : 'extended.values.medalsEliminationLastStandKill.basic.value',
             'column_name'  : 'Never Say Die',
             'team'         : 'us'},
            {'path'         : 'extended.values.medalsEliminationLastStandRevive.basic.value',
             'column_name'  : 'From The Brink',
             'team'         : 'us'},
            {'path'         : 'extended.values.medalsEliminationWipeQuick.basic.value',
             'column_name'  : 'Wrecking Ball',
             'team'         : 'us'},
            {'path'         : 'extended.values.medalsCloseCallTalent.basic.value',
             'column_name'  : 'Wrecking Ball',
             'team'         : 'us'},

        #Primaries
            {'path'         : 'extended.values.weaponKillsAutoRifle.basic.value',
             'column_name'  : 'Auto Rifle Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponPrecisionKillsAutoRifle.basic.value',
             'column_name'  : 'Auto Rifle Prec Kills',
             'team'         : 'us'},

            {'path'         : 'extended.values.weaponKillsHandCannon.basic.value',
             'column_name'  : 'Hand Cannon Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponPrecisionKillsHandCannon.basic.value',
             'column_name'  : 'Hand Cannon Prec Kills',
             'team'         : 'us'},

            {'path'         : 'extended.values.weaponKillsPulseRifle.basic.value',
             'column_name'  : 'Pulse Rifle Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponPrecisionKillsPulseRifle.basic.value',
             'column_name'  : 'Pulse Rifle Prec Kills',
             'team'         : 'us'},

            {'path'         : 'extended.values.weaponKillsScoutRifle.basic.value',
             'column_name'  : 'Scout Rifle Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponPrecisionKillsScoutRifle.basic.value',
             'column_name'  : 'Scout Rifle Prec Kills',
             'team'         : 'us'},

        #Secondaries
            {'path'         : 'extended.values.weaponKillsSniper.basic.value',
             'column_name'  : 'Sniper Rifle Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponPrecisionKillsSniper.basic.value',
             'column_name'  : 'Sniper Rifle Prec Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsShotgun.basic.value',
             'column_name'  : 'Shotgun Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsFusionRifle.basic.value', #doesn't appear to be working
             'column_name'  : 'Fusion Rifle Kills',
             'team'         : 'us'},

        # Heavy Weapons, Melees, Grenades, Supers
            {'path'         : 'extended.values.weaponKillsRocketLauncher.basic.value',
             'column_name'  : 'Rocket Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsMachineGun.basic.value', #doesn't appear to be working
             'column_name'  : 'HMG Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsMelee.basic.value',
             'column_name'  : 'Melee Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsGrenade.basic.value', 
             'column_name'  : 'Grenade Kills',
             'team'         : 'us'},
            {'path'         : 'extended.values.weaponKillsSuper.basic.value', 
             'column_name'  : 'Super Kills',
             'team'         : 'us'}
]
