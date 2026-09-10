with player_history as (

    select
        player_id,
        round as gameweek,
        total_points

    from {{ ref('stg_fpl_player_history') }}

),

final as (

    select
        player_id,
        gameweek,
        total_points,

        avg(total_points) over (
            partition by player_id
            order by gameweek
            rows between 4 preceding and current row
        ) as rolling_5_gw_points

    from player_history

)

select *
from final