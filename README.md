# FPL-Edge

End-to-end FPL data pipeline and analytics platform

## Candidate Data Model

Based on the FPL API exploration, the following candidate tables were identified.

### Candidate Dimensions

- `dim_player` – stores player information such as player ID, name, position, and team.
- `dim_team` – stores Premier League team information.
- `dim_gameweek` – stores gameweek information.
- `dim_fixture` – stores fixture information such as home team, away team, kickoff time, and difficulty.

### Candidate Fact Tables

- `fct_player_gameweek` – stores player performance for each gameweek.

## Data Grain

Grain: **One row per player per gameweek.**

Potential metrics include:

- Total points
- Minutes played
- Goals scored
- Assists
- Clean sheets
- Bonus points
- BPS
- Expected goals
- Expected assists
- Historical player value