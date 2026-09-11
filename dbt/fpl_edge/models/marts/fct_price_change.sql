{{ config(materialized='table') }}

with snapshot_data as (

    select
        id as player_id,
        now_cost / 10.0 as price,
        dbt_valid_from as valid_from,
        dbt_valid_to as valid_to
    from {{ ref('player_snapshot') }}

),

price_changes as (

    select
        player_id,
        price,
        valid_from,
        valid_to,

        lag(price) over (
            partition by player_id
            order by valid_from
        ) as previous_price

    from snapshot_data

)

select
    player_id,
    price,
    previous_price,
    price - previous_price as price_change,
    valid_from,
    valid_to

from price_changes

where previous_price is not null