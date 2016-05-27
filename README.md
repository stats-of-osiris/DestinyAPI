# DestiPy
Project to pull stats from Destiny's API to support a team-based performance analysis for a Trials of Osiris passage.

- [Bungie API Wiki](http://bungienetplatform.wikia.com/wiki/Bungienetplatform_Wikia)
- [List of all API endpoints](http://bungienetplatform.wikia.com/wiki/Endpoints)
- [Bungie API Support Forum](https://www.bungie.net/en/Clan/Forum/39966)
- [TRON: Legacy Soundtrack](https://www.youtube.com/watch?v=COWrh0eFFWk)

## Report Template
[Template located here.](https://github.com/yergi/DestinyAPI/blob/master/report_card.md) Sections for Team Summary, Overall Team Performance & Detailed Individual Performance.

## Architecture

- `example.py` is a working development script & imports the `destiny` folder
- `template_write.py` is the script for writing the final report card to a `.md` Markdown file. Not currently connected to the rest of the project for inputs.

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
	- list of key stats to collect from API response, based on ['stats_blob.txt`](https://github.com/yergi/DestinyAPI/blob/master/destiny/stats_blob.txt)