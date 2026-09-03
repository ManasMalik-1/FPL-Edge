with players as (

    select *
    from {{ ref('stg_fpl_players') }}

),

performance as (

    select *
    from {{ ref('player_performance') }}

),

final as (

    select
        p.player_id,
        p.player_name,
        p.team_id,
        p.position_id,
        p.price,
        p.status,
	p.form,
	p.selected_by_percent,
        p.total_points,
        p.minutes,

        perf.fixtures_played,
        perf.points_per_match,
        perf.xg,
        perf.xa,
        perf.xgi,

        round(
            case
                when p.price > 0
                then p.total_points / p.price
                else 0
            end,
            2
        ) as points_per_million,

        round(
            case
                when p.price > 0 and p.minutes > 0
                then perf.xgi / p.price
                else 0
            end,
            3
        ) as xgi_per_million

    from players p

    left join performance perf
        on p.player_id = perf.player_id

)

select *
from final