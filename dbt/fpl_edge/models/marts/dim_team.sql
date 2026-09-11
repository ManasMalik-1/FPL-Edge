{{ config(materialized='table') }}

select
    team_id,
    team_name,
    short_name,
    code,
    position,
    played,
    win,
    draw,
    loss,
    points,
    form,
    strength,
    strength_overall_home,
    strength_overall_away,
    strength_attack_home,
    strength_attack_away,
    strength_defence_home,
    strength_defence_away,
    unavailable
from {{ ref('stg_fpl__teams') }}