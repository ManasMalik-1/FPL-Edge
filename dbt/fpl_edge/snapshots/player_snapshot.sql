{% snapshot player_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='id',
        strategy='check',
        check_cols=[
            'web_name',
            'now_cost',
            'team',
            'element_type',
            'total_points',
            'minutes',
            'goals_scored',
            'assists',
            'clean_sheets',
            'goals_conceded',
            'own_goals',
            'penalties_saved',
            'penalties_missed',
            'yellow_cards',
            'red_cards',
            'saves',
            'bonus',
            'bps',
            'influence',
            'creativity',
            'threat',
            'ict_index',
            'expected_goals',
            'expected_assists',
            'expected_goal_involvements',
            'expected_goals_conceded',
            'form',
            'points_per_game',
            'selected_by_percent',
            'transfers_in',
            'transfers_out',
            'value_form',
            'value_season',
            'status',
            'chance_of_playing_next_round',
            'chance_of_playing_this_round'
        ]
    )
}}

select
    id,
    web_name,
    now_cost,
    team,
    element_type,

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

    _ingested_at,
    _source_file

from (
    select
        *,
        row_number() over (
            partition by id
            order by _ingested_at desc
        ) as rn
    from {{ source('raw', 'fpl_players') }}
) latest

where rn = 1

{% endsnapshot %}