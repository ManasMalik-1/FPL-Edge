with completed_fixtures as (

    select
        fixture_id,
        gameweek,
        team_h,
        team_a,
        team_h_score,
        team_a_score,
        kickoff_time

    from {{ ref('stg_fpl__fixtures') }}

    where finished = true

),

home_team_results as (

    select
        team_h as team_id,
        gameweek,
        team_h_score as goals_for,
        team_a_score as goals_against,

        case
            when team_h_score > team_a_score then 3
            when team_h_score = team_a_score then 1
            else 0
        end as points

    from completed_fixtures

),

away_team_results as (

    select
        team_a as team_id,
        gameweek,
        team_a_score as goals_for,
        team_h_score as goals_against,

        case
            when team_a_score > team_h_score then 3
            when team_a_score = team_h_score then 1
            else 0
        end as points

    from completed_fixtures

),

all_results as (

    select * from home_team_results

    union all

    select * from away_team_results

),

team_totals as (

    select
        team_id,

        count(*) as matches_played,

        sum(points) as total_points,

        sum(goals_for) as goals_for,

        sum(goals_against) as goals_against,

        avg(goals_for::numeric) as goals_for_per_match,

        avg(goals_against::numeric) as goals_against_per_match,

        avg(points::numeric) as points_per_match

    from all_results

    group by team_id

),

strengths as (

    select
        team_id,
        matches_played,
        total_points,
        goals_for,
        goals_against,

        round(goals_for_per_match, 3)
            as goals_for_per_match,

        round(goals_against_per_match, 3)
            as goals_against_per_match,

        round(points_per_match, 3)
            as points_per_match,

        /*
         * Attack strength:
         * Higher scoring teams receive a higher value.
         */
        round(
            goals_for_per_match,
            3
        ) as attack_strength,

        /*
         * Defence strength:
         * Lower goals conceded = stronger defence.
         */
        round(
            5.0 - goals_against_per_match,
            3
        ) as defence_strength

    from team_totals

)

select *
from strengths