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


----------------------------------------------------


Future Features — FPL-Edge

Project Vision

FPL-Edge aims to evolve from a data analytics project into an FPL intelligence platform that combines:

Statistical and historical FPL data
Manager insights and press conference signals
Community and pundit opinions
Personal FPL manager analytics

The long-term architecture can be viewed as:

                         FPL-EDGE
                            |
        ---------------------------------------
        |                 |                   |
   Data Analytics    Manager Insights    Community Insights
        |                 |                   |
        |                 |                   |
    FPL Wrapped      Minutes Confidence   Consensus Strategy
        \                 |                /
         \                |               /
          --------------------------------
                         |
                   FPL Decisions
1. FPL Wrapped
Description

FPL Wrapped will provide a season-end summary of a user's Fantasy Premier League performance, similar to Spotify Wrapped.

The feature will transform a manager's historical FPL data into an interactive and potentially shareable set of insights.

Potential Metrics
Season Performance
Total points
Final overall rank
Best gameweek
Worst gameweek
Rank progression throughout the season
Manager Behaviour
Most captained player
Best captain decision
Worst captain decision
Most transferred-in player
Total number of transfers
Points hits taken
Decision Analysis
Bench points wasted
Highest points left on the bench
Captaincy points gained or lost
Most successful transfer
Least successful transfer
Best differential player
Biggest FPL regret
Data Flow
Manager ID
    |
    v
Manager History
    |
    v
Gameweek Picks + Transfers + Captaincy
    |
    v
FPL-Edge Analytics
    |
    v
FPL Wrapped Metrics
    |
    v
Shareable Season Summary
Example Output
YOUR FPL SEASON WRAPPED

Best Gameweek: GW 24
Best Captain: Haaland
Most Trusted Player: Saka
Biggest Bench Regret: 18 Points
Best Transfer: Palmer
Rank Improvement: +1,200,000
Priority

Priority: High

This feature should be implemented first after the core FPL-Edge platform because it primarily uses data already available through the FPL ecosystem.

2. Manager Insights Engine
Description

The Manager Insights Engine will analyze manager press conferences to extract FPL-relevant information.

The goal is not only to identify injuries but to understand signals about:

Player availability
Expected minutes
Rotation risk
Manager trust
Player importance
Tactical role

These qualitative signals can be combined with historical player data to estimate a player's minutes confidence.

Core Pipeline
Press Conference
       |
       v
Transcript / Text
       |
       v
Player Mention Detection
       |
       v
FPL-Relevant Signal Extraction
       |
       v
Structured Manager Signals
       |
       v
Minutes Confidence / FPL Impact
Signal Categories
Availability

Possible signals:

Fit
Injured
Doubtful
Being assessed
Returning from injury
Not ready
Rotation and Minutes

Possible signals:

Expected to start
Rested
Minutes being managed
Rotation expected
Strong competition for position
Manager Trust

Possible signals:

Important player
Key player
Trusted player
Excellent form
Strong training performances
Tactical Role

Possible signals:

Playing in a new position
More advanced role
Deeper role
Set-piece responsibility
Penalty responsibility
Potential Data Model

A future fact table could be:

fct_manager_player_signal
player_id	date	signal_type	sentiment	confidence
Player A	2026-08-20	availability	positive	high
Player A	2026-08-20	manager_trust	positive	medium
Player B	2026-08-20	rotation_risk	negative	high
Minutes Confidence

The final score could combine qualitative and quantitative information.

Manager Signals
       +
Recent Starts
       +
Recent Minutes
       +
Fixture Congestion
       +
Squad Competition
       +
Injury Status
       |
       v
Minutes Confidence Score

Example:

Player: Example Player

Minutes Confidence: 91%

Manager Trust: Strong
Recent Starts: 5/5
Rotation Risk: Low
Fitness Status: Available
Possible Outputs
Dashboard

A dedicated section showing:

High minutes confidence
Medium minutes confidence
Low minutes confidence
Recent manager signals
Changes in player availability
Notifications

The system could eventually send notifications when important manager information changes.

Example:

Manager Update

The player is still being assessed.

Minutes Confidence:
78% -> 52%
Important Principle

Minutes Confidence should be treated as an analytical estimate, not a guarantee that a player will start.

Priority

Priority: High

This is potentially one of FPL-Edge's most unique features because it introduces qualitative manager context that is not available through standard FPL statistics alone.

3. Consensus Strategy
Description

Consensus Strategy will analyze FPL content from multiple trusted pundits and summarize areas of agreement and disagreement.

The purpose is to reduce the time required to consume multiple hours of FPL videos and podcasts.

Instead of manually watching all content, the user could see:

Which players pundits recommend
Where pundits agree
Where they disagree
The main reasoning behind each opinion
Core Pipeline
FPL Videos / Podcasts
          |
          v
Transcripts
          |
          v
Opinion Extraction
          |
          v
Player + Recommendation + Reason
          |
          v
Consensus / Disagreement Analysis
Example Structured Opinion
Pundit: Source A
Player: Saka
Recommendation: Buy
Reason: Strong fixtures
Confidence: High
Potential Data Model
fct_pundit_opinion
pundit	player	recommendation	confidence	reason
A	Saka	Buy	High	Fixtures
B	Saka	Hold	Medium	Minutes
C	Saka	Buy	High	Form
Consensus Output

Example:

SAKA

Consensus:
Most pundits consider Saka a strong medium-term option.

Agreement:
- Good fixtures
- Strong underlying statistics

Disagreement:
- Whether to transfer him in immediately
- Concerns about price

Recommendations:

Buy:  75%
Hold: 20%
Sell:  5%
Potential Future Improvements
Weight pundit opinions based on historical accuracy
Track recommendation performance
Identify changing opinions over time
Compare consensus against actual FPL outcomes
Priority

Priority: Medium/High

This is technically complex and should be implemented after the core data platform and Manager Insights Engine.

Implementation Order

The recommended development sequence is:

Phase 1 — Core FPL-Edge
FPL API
    |
    v
Python Ingestion
    |
    v
PostgreSQL
    |
    v
dbt Transformations
    |
    v
Star Schema
    |
    v
Data Quality Testing
    |
    v
Power BI Analytics
Phase 2 — FPL Wrapped

Build a personal manager analytics and season summary experience using existing FPL data.

Phase 3 — Manager Insights Engine

Develop press conference ingestion, player signal extraction, and Minutes Confidence analytics.

Phase 4 — Consensus Strategy

Develop multi-source content processing, opinion extraction, and consensus analysis.

Long-Term Product Goal

FPL-Edge should eventually provide three types of intelligence:

1. What the statistics say
          +
2. What managers are signalling
          +
3. What FPL experts are discussing
          |
          v
     Better FPL decisions
Important Development Principle

The advanced features should be designed as separate modules that connect to the central FPL-Edge data platform. The initial core pipeline should be completed before implementing these features.

