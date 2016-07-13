# DestiPy
Project to pull stats from Destiny's API to support a performance analysis for Destiny games.

- [Unofficial API Github](http://destinydevs.github.io/BungieNetPlatform/)
- [List of all API endpoints](http://destinydevs.github.io/BungieNetPlatform/docs/Endpoints)
- [List of all medals](http://destinydevs.github.io/BungieNetPlatform/docs/MedalHistoricalStats)
- [Bungie API Support Forum](https://www.bungie.net/en/Clan/Forum/39966)
- [TRON: Legacy Soundtrack](https://www.youtube.com/watch?v=COWrh0eFFWk)
- [Web-based Activity Viewer](http://destinyactivitydetails.com/)


## Data Set Inputs
The ideal case for when the user builds the data set is for them to give these as required:

* console system
* display name
* game mode
* number of games

And these as optional:

* start date
* end date
* last game id 
* guardian id

And then the result data set becomes an object for people to run the pre-built reports. 
Oh, and potentially a list of columns to return as an optional argument as well. Otherwise it includes all columns.

## Architecture

- `example.py` is a working development script & imports the `destiny` folder
- `trialsreport_write.py` is the script for writing the final report card to a `.md` Markdown file. Not currently connected to the rest of the project for inputs.

### Report Scripts in `destiny` folder

- `player.py`
	- This module defines the Player and Guardian classes, which pull from the `GetDestinyAccountSummary` endpoint of the Destiny API.
	- `Player` class: "Pull summary data of each guardian belonging to the Player."
	- `Guardian` class: 
		- `_filter_guardian`: "Take the full guardian list from Player and filter to single Guardian."
		- `_get_last_guardian`: "Finds the last guardian played.."
- `game.py`
	- This module defines the `Game` class which provides access to the `PostGameCarnageReport` endpoint of the Destiny API. This class is used by the `Report` class to generate the data for analysis.
	- `games_from_ids` classmethod: "Pass a list of game_ids and return a list of Game objects"
	- `games_from_guardian` classmethod: "Pass Guardian object and return a dict of Game objects"
	- `pull team stats` class: "Finds the desired stat for the specified team (Alpha | Bravo) for a given Game."
	- `sweaty status` class: "Determine whether a Trials game was "sweaty". Defined as enemy team scoring 3 or greater."
- `report.py`
	- This is the primary module of stats_osiris. It returns several various dictionaries of game stats to enable further analysis of a player's Trials of Osiris performance.
	- `report_games` class: "Aggregate self.data to a game level, filtered to stats defined in `constants`."
	- `report_teams` class: "Aggregate self.data to a team per game level."
	- `report_my_team` class: "Aggregate self.data to a fireteam level, across all games."
	- `_get_player_stat` class: "Function to find stats for a given player across all Games present in self.data."

### API Scripts in `destiny` folder

- `constants.py` 
	- Central location for `API_PATHS` to improve readability in other scripts.
	- Playstation or Xbox `PLATFORMS`
	- Hashes for `GUARDIAN_TYPE`, `GUARDIAN_RACE`, `GUARDIAN_GENDER`
	- Codes for `ACTIVITY_MODES`.
	- list of `KEY_STATS` to collect from API response, currently based on needs of a Trials Report.
- `utils.py` 
	- `get_json`: API call, dict transform & returns the response. 
	- `validate_json`: reports errors
	- `build_session` : handles the API request header creation
	- `close_session` : clean up after yourself, your mama ain't here.	- 
	- `crawl_data`: Response crawl to look for stats & return possible values for stats not found.
- `manifest.py`
	- Manifest work is divided into two halves, one handling the manifest from Bungie, and one making it easily accessible to other scripts. 
	- Manifest file work:
		- `update_version` : "Update the current version of the locally stored manfiest file and when an update check was last performed"
		- `check_version`  : "When pulling data from the manifest, this will check for an updated version every 30 days, or if the `force_update` flag is flipped"
		- `update_manifest` : "Download the zipped manifest file. Shows a progress bar where '=' == 2%"
		- `unzip_manifest` : "Helper function to unzip manifest file, and delete the zip file"
		- `check_for_update`  : "    When pulling data from the manifest, this will check for an updated version every 30 days, or if the `force_update` flag is flipped"
	- Accessibility functions take hashes and returns the Manifest entries.
		- `get_row`
		- `get_table`
		- `get_bucket`
		- `get_item`
		- `get_items`
		- `get_map`

## Trials Report Template
[Template located here.](http://johnofmars.github.io/articles/FirebaseDelphiReptCard/) Sections for Team Summary, Overall Team Performance & Detailed Individual Performance.
