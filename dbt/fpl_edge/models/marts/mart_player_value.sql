{{ config(materialized='table') }}

with latest_form as (

    select
        player_id,
        rolling_5_gw_points
    from (
        select
            player_id,
            gameweek,
            rolling_5_gw_points,

            row_number() over (
                partition by player_id
                order by gameweek desc
            ) as row_num

        from {{ ref('int_player_form_rolling') }}
    ) ranked

    where row_num = 1

),

current_players as (

    select *
    from (
        select
            *,
            row_number() over (
                partition by player_id
                order by valid_from desc
            ) as row_num

        from {{ ref('dim_player') }}

        where is_current = true
    ) ranked

    where row_num = 1

)

select
    p.player_id,
    p.player_name,
    p.team_id,
    t.team_name,
    p.position_id,
    p.price,
    p.total_points,
    p.minutes,
    p.goals_scored,
    p.assists,
    p.clean_sheets,
    p.form,
    p.points_per_game,
    p.selected_by_percent,
    p.transfers_in,
    p.transfers_out,
    p.value_form,
    p.value_season,

    f.rolling_5_gw_points,

    d.avg_difficulty_next5

from current_players p

left join {{ ref('dim_team') }} t
    on p.team_id = t.team_id

left join latest_form f
    on p.player_id = f.player_id

left join {{ ref('int_fixture_difficulty_next5') }} d
    on p.team_id = d.team_id