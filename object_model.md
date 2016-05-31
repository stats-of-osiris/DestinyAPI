
# Destipy Object Model

## Objects

- ReportContext
- Account
- Guardian
- Fireteam
- Game

## Structure

- context (destipy.ReportContext)
    - session (requests.Session)
    - account (destipy.Account)
        - vars
        - guardians (List)
            - guardian (destipy.Guardian)
                - vars
                - stats (pandas.DataFrame)
    - teams (List)
        - team (destipy.Fireteam)
            - stats (pandas.DataFrame)
            - guardians (List)
                - guardian (destipy.Guardian)
    - hometeam (destipy.Fireteam)
    - awayteam (destipy.Fireteam)
    - games (List)
        - game (destipy.Game)
            - vars
            - stats (pandas.DataFrame)
            - guardians (List)
                - guardian (destipy.Guardian)

