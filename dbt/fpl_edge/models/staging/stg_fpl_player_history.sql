with source as (

    select *
    from {{ source('raw', 'fpl_player_history') }}

),

cleaned as (

    select
        player_id,
        fixture,
        opponent_team,
        total_points,

        was_home,

        kickoff_time,
        round,

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

        cast(influence as numeric) as influence,
        cast(creativity as numeric) as creativity,
        cast(threat as numeric) as threat,
        cast(ict_index as numeric) as ict_index,

        cast(expected_goals as numeric) as expected_goals,
        cast(expected_assists as numeric) as expected_assists,
        cast(expected_goal_involvements as numeric) as expected_goal_involvements,
        cast(expected_goals_conceded as numeric) as expected_goals_conceded,

        value,
        transfers_balance,
        selected,
        transfers_in,
        transfers_out,

        _ingested_at,
        _source_file

    from source

)

select *
from cleaned