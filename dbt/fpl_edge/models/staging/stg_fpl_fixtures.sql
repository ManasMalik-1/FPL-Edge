SELECT
    id AS fixture_id,
    event AS gameweek,
    team_h,
    team_a,
    team_h_score,
    team_a_score,
    kickoff_time,
    finished,
    team_h_difficulty,
    team_a_difficulty
FROM {{ source('raw', 'fpl_fixtures') }}