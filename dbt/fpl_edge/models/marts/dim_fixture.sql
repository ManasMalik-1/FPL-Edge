{{ config(materialized='table') }}

select
    fixture_id,
    gameweek,
    team_h,
    team_a,
    team_h_score,
    team_a_score,
    kickoff_time,
    finished,
    team_h_difficulty,
    team_a_difficulty
from {{ ref('stg_fpl__fixtures') }}