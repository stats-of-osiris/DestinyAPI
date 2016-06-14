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

### API Scripts in `destiny` folder

- `utils.py` 
	- `get_json`: API call, dict transform & returns the response. 
	- `validate_json`: reports errors 
	- `crawl_data`: Response crawl to look for stats & return possible values for stats not found.
- `Account.py`
	- Create Account object using JSON data from the `GetDestinyAccountSummary` endpoint.
- `Guardian.py`
	- Create Guardian object using JSON data from the `GetDestinyAccountSummary` endpoint.
- `CarnageReport.py`
	- This class provides access to the `PostGameCarnageReport` endpoint of the Destiny API, which includes:
	- `class` for `CarnageReport`
		- `classmethod` for `reports_from_ids`
		- `classmethod` for `reports_from_guardians`
	- `class` for `CarnagePlayers`
		- `classmethod` for `players_from_data`

### Support Scripts in `destiny` folder

- `constants.py` 
	- Central location for `API_PATHS` to improve readability in other scripts.
	- Playstation or Xbox `PLATFORMS`
	- Hashes for `GUARDIAN_TYPE`, `GUARDIAN_RACE`, `GUARDIAN_GENDER`
	- Codes for `ACTIVITY_MODES`.
	- list of `KEY_STATS` to collect from API response, currently based on needs of a Trials Report.

## Trials Report Template
[Template located here.](https://github.com/yergi/DestinyAPI/blob/master/report_card.md) Sections for Team Summary, Overall Team Performance & Detailed Individual Performance.
