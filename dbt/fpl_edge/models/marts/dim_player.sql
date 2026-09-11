{{ config(materialized='table') }}

select
    id as player_id,
    web_name as player_name,
    team as team_id,
    element_type as position_id,
    case
        when element_type = 1 then 'GKP'
        when element_type = 2 then 'DEF'
        when element_type = 3 then 'MID'
        when element_type = 4 then 'FWD'
    end as position,
    now_cost / 10.0 as price,

    total_points,
    minutes,
    goals_scored,
    assists,
    clean_sheets,
    goals_conceded,
    own_goals,
    penalties_saved,
    penalties_missed,
    yellow_cards,
    red_cards,
    saves,
    bonus,
    bps,
    influence,
    creativity,
    threat,
    ict_index,
    expected_goals,
    expected_assists,
    expected_goal_involvements,
    expected_goals_conceded,
    form,
    points_per_game,
    selected_by_percent,
    transfers_in,
    transfers_out,
    value_form,
    value_season,
    status,
    chance_of_playing_next_round,
    chance_of_playing_this_round,

    dbt_valid_from as valid_from,
    dbt_valid_to as valid_to,

    case
        when dbt_valid_to is null then true
        else false
    end as is_current

from {{ ref('player_snapshot') }}