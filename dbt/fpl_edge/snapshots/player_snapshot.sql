{% snapshot player_snapshot %}

{{
    config(
        target_schema='snapshots',
        unique_key='player_id',
        strategy='check',
        check_cols=[
            'price',
            'selected_by_percent',
            'status',
            'chance_of_playing_next_round'
        ]
    )
}}

select *
from {{ ref('stg_fpl__players_scd_test') }}

{% endsnapshot %}