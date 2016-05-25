# DestinyAPI
Project to pull stats from Destiny's API to support a team-based performance analysis for a Trials of Osiris passage.

- [Bungie API Wiki](http://bungienetplatform.wikia.com/wiki/Special:WikiActivity)
- [Bungie API Support Forum](https://www.bungie.net/en/Clan/Forum/39966)
- [TRON: Legacy Soundtrack](https://www.youtube.com/watch?v=COWrh0eFFWk)

## Report Template
[Template located here.](https://github.com/yergi/DestinyAPI/blob/master/Results_Template.md) Sections for Team Identification, Team Performance & Card Total Individual Performance.

## Architecture
`example.py` is main script & imports the `destiny` subfolder

- `___init___.py` imports game & player
- `constants.py` 
	- list of key stats to collect from API response, based on ['stats_blob.txt`](https://github.com/yergi/DestinyAPI/blob/master/destiny/stats_blob.txt)
- `game.py`
	- calls `__init__.py` & uses `utils` to find player games.
- `player.py`
	- isolates player data
- `utils.py` 
	- `get_json`: API call, dict transform & returns the response. 
	- `craw_data`: Response crawl to look for stats & return possible values for stats not found.
