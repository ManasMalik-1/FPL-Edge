select
    id as player_id,
    web_name as player_name,
    team as team_id,
    element_type as position_id,

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

    cast(influence as numeric) as influence,
    cast(creativity as numeric) as creativity,
    cast(threat as numeric) as threat,
    cast(ict_index as numeric) as ict_index,

    cast(expected_goals as numeric) as expected_goals,
    cast(expected_assists as numeric) as expected_assists,
    cast(expected_goal_involvements as numeric) as expected_goal_involvements,
    cast(expected_goals_conceded as numeric) as expected_goals_conceded,

    form,
    points_per_game,
    cast(selected_by_percent as numeric) as selected_by_percent,

    transfers_in,
    transfers_out,

    value_form,
    value_season,

    status,
    chance_of_playing_next_round,
    chance_of_playing_this_round,

    dbt_valid_from,
    dbt_valid_to,

    case
        when dbt_valid_to is null then 'CURRENT'
        else 'HISTORICAL'
    end as version_status,

    _ingested_at,
    _source_file

from {{ ref('player_snapshot') }}