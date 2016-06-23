# Report Context


## `apicall_scrape_csvwrite.py`

This script is totally redundant with work done in the main `DestiPy` folder, but I can't make heads or tails of that, so I took an already working solution and used that so I could do report context work instead.

This is based on James' first `fruit2.py` script for doing a simple API call and writing stats to a csv. I have modified to include all of the KEY_STATS listed in `constants.py` as well as a few others as I have been working.

TO DO: 

- Deprecate this script in favor of main `DestiPy` functions.
- Update `KEY_STATS` in `constants.py`
- Update naming convention in `KEY_STATS` to use lowercase snakecase naming convention rather than normal speech (e.g. `ar_kills` instead of `Auto Rifle Kills`).


## `data_crunch.py`

This script imports the `.csv` into a single dataframe (`dfStats`) with all data. And from that it generates 3 results dataframes:

- Teams Summary across all games (`dfTeams`)
	- us
	- them
- Games Summary based on allegiance to queried player (`dfGames`)
- Individual Performance Summary across all games  (`dfIndiv`)
	- player
	- teammate(s)

TO DO:

- Need function to find teammates
- Need to incorporate `manifest` for
	- finding Map name & photo
	- finding player loadouts
- Plot games graph


## `report_card_prototype.py`

Based on `report_card.py` in main folder. Almost done working on it. Right now it needs implementation of the graphs and hashes. But the `data_crunch.py` needs to be updated for that next.

# TODO:

## Display Map
Collect Map Hash
Convert Map Hash to Map Name
Format Map Name
Locate map image path

## Plotting
Plot Round Scores by Game
Plot Kill Method Distrubution

##Calculate Sweaty K/D
dfGames filter by enemy score
Assign sweaty status
update dfStats before dfTeams/dfIndiv creation
Assign sweaty kills
Assign sweaty deaths
Calculate sweaty K/D or N/A for no sweaty matches
Display sweaty K/D

##Display Best Weapon
Collect weapon hashes & kill counts 
Find max kill weapon for each class
Convert weapon hashes to names
Cross-reference best weapon class with weapon name

## General Report Fixes
Updated description:
"Scores are tabulated across all games for individuals and the team. And then a player's contribution is shown as their percent of the team's total score."
Format Time better to include seconds
