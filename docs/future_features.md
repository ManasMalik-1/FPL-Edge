# Future Features

## Goalkeeper Rotation / Combo Recommendations

Analyse pairs of goalkeepers rather than only individual goalkeepers.

The system should identify goalkeeper combinations where their fixtures complement each other.

Example:

GW1 → GK A has easy fixture → Start GK A
GW2 → GK A has difficult fixture, GK B has easy fixture → Start GK B
GW3 → GK A has easy fixture → Start GK A

The recommendation should consider:

- Fixture difficulty
- Team defensive strength
- Expected points
- Upcoming fixtures
- Combined price

Goal: recommend the best two-goalkeeper combinations and indicate which goalkeeper to start each gameweek.

Best £9.0m Goalkeeper Combination
--------------------------------
GK A + GK B

Best starter selected for each upcoming fixture
based on:
- fixture difficulty
- team defensive strength
- expected points


-------------------------------------------------------------------------
Dynamic Fixture Horizon

Currently, the fixture table shows the next 5 gameweeks.

In the final FPL Edge app, users should be able to choose how many upcoming gameweeks they want to analyze.

Possible options:
- 1 Gameweek
- 3 Gameweeks
- 5 Gameweeks
- 7 Gameweeks
- Custom number of Gameweeks

The fixture table should dynamically update based on the user's selection.

Example:
If the user selects 1 GW:
Team | GW1 | Avg Difficulty

If the user selects 3 GWs:
Team | GW1 | GW2 | GW3 | Avg Difficulty

If the user selects 7 GWs:
Team | GW1 | GW2 | GW3 | GW4 | GW5 | GW6 | GW7 | Avg Difficulty

The average fixture difficulty should be recalculated based only on the selected number of upcoming gameweeks.

Goal:
Allow users to analyze fixtures differently depending on their FPL strategy, such as a 1-week punt, a 3-gameweek transfer, or a longer-term 7+ gameweek investment.