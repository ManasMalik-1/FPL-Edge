# FPL Edge Data Dictionary

## Raw Data
### Universal Player Data

- player_id
- player_name
- position
- team_id
- team_name

### Price Data

- season_start_price
- current_price
- price_change

### FPL Activity Data

- ownership_percentage
- transfers_in
- transfers_out

### Availability Data

- injury_status
- suspension_status
- chance_of_playing
- expected_return_date

### Gameweek / Fixture Data

- gameweek
- fixture_id
- opponent
- home_or_away
- fixture_difficulty
- double_gameweek_flag
- blank_gameweek_flag

### Bonus points

- Bonus points earned
- Bonus points per game

#### Position Based Raw Data

### Forward Raw Data

- goals
- assists
- minutes_played
- shots
- big_chances
- big_chances_missed
- non_penalty_xg
- touches_in_opposition_box
- penalty_taker
- central_striker_flag
- main_goal_scorer
- substitution_pattern

### Midfielder Raw Data

- goals
- assists
- minutes_played
- shots
- expected_goals
- expected_assists
- big_chances_created
- touches_in_opposition_box
- penalty_taker
- set_piece_taker
- corner_taker
- defensive_contributions
- position_role
- substitution_pattern

### Defender Raw Data

- goals
- assists
- minutes_played
- goals_conceded
- defensive_contributions
- tackles
- interceptions
- clearances
- blocks
- ball_recoveries
- expected_goals
- expected_assists
- big_chances_created
- touches_in_opposition_box
- position_role
- set_piece_involvement
- set_piece_target
- corner_target
- free_kick_taker
- height
- aerial_actions

### Goalkeeper Raw Data

- minutes_played
- saves
- goals_conceded
- goals_prevented
- clean_sheets
- rotation_risk

## Derived Metrics
Metrics calculated from raw data.

### Universal Derived Metrics

- price_change_since_season_start
- points_per_million
- value_for_money
- recent_form
- last_5_gameweeks_performance
- form_trend
- consistency
- home_vs_away_performance
- expected_output_relative_to_price
- normal_to_per_90_conversion
- bonus_point_potential
- goal_contribution_share

### Forward Derived Metrics

- shots_per_90
- big_chances_per_90
- non_penalty_xg_per_90
- touches_in_opposition_box_per_90
- goals_per_90
- assists_per_90
- goal_contribution_share
- team_dependency
- team_attacking_strength
- team_feed_dependency
- minutes_risk
- rotation_risk_score
- likelihood_of_playing_90_minutes

### Midfielder Derived Metrics

- goals_per_90
- assists_per_90
- expected_goals_per_90
- expected_assists_per_90
- shots_per_90
- big_chances_created_per_90
- touches_in_opposition_box_per_90
- goal_contribution_share
- team_dependency
- minutes_per_start
- minutes_risk

### Defender Derived Metrics

- goals_per_90
- assists_per_90
- goals_conceded_per_90
- expected_goals_per_90
- expected_assists_per_90
- expected_goal_involvement
- big_chances_created_per_90
- touches_in_opposition_box_per_90
- clean_sheet_percentage
- defensive_contributions_per_90
- tackles_per_90
- interceptions_per_90
- clearances_per_90
- blocks_per_90
- ball_recoveries_per_90
- goal_threat
- team_defensive_strength
- aerial_threat

### Goalkeeper Derived Metrics

- saves_per_90
- goals_conceded_per_90
- save_percentage
- clean_sheet_percentage
- team_defensive_strength
- minutes_risk

## Predictions
Metrics predicted by the FPL Edge model.

## Predictions

### Universal Predictions

- expected_points_next_fixture
- expected_points_next_3_fixtures
- expected_points_next_5_fixtures

### Player Availability Predictions

- expected_minutes_next_fixture
- likelihood_of_starting
- likelihood_of_playing_90_minutes

## UI Features
Features that control how information is displayed.

## UI Features

### Player Status Indicators

- injury_icon_on_player_name
- suspension_icon_on_player_name
- player_availability_status
- chance_of_playing_display
- expected_return_date_display

### Stats Display

- normal_stats_view
- per_90_stats_view
- normal_to_per_90_toggle

### Price & Value Display

- price_history_visualization
- price_change_display
- value_for_money_display

### Fixture Display

- fixture_difficulty_display
- home_or_away_indicator
- double_gameweek_indicator
- blank_gameweek_indicator

### Best Players by Price Range

A dedicated page that shows the top 5 recommended players within each FPL price range.

Example price ranges:

- under_5m
- 5m_to_6_5m
- 6_5m_to_8m
- 8m_to_10m
- 10m_plus

For each price range:

- top_5_players
- player_price
- position
- expected_points
- value_for_money
- recent_form
- fixture_context
- key_recommendation_metrics


filter this page by

All Positions
Goalkeeper
Defender
Midfielder
Forward