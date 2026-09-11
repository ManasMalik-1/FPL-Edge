{{ config(
    materialized='incremental',
    unique_key='player_gameweek_key'
) }}

select
    player_id,
    gameweek,
    fixture,
    opponent_team,
    total_points,
    was_home,
    kickoff_time,
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
    clearances_blocks_interceptions,
    recoveries,
    tackles,
    defensive_contribution,
    starts,
    influence,
    creativity,
    threat,
    ict_index,
    expected_goals,
    expected_assists,
    expected_goal_involvements,
    expected_goals_conceded,
    value,
    transfers_balance,
    selected,
    transfers_in,
    transfers_out,

    concat(player_id, '_', gameweek, '_', fixture) as player_gameweek_key

from {{ ref('stg_fpl__player_gameweek') }}

{% if is_incremental() %}

where gameweek > (
    select coalesce(max(gameweek), 0)
    from {{ this }}
)

{% endif %}