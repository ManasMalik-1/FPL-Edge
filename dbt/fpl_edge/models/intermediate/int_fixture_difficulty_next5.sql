with fixtures as (

    select
        fixture_id,
        gameweek,
        team_h,
        team_a,
        team_h_difficulty,
        team_a_difficulty,
        kickoff_time,
        finished

    from {{ ref('fixture_difficulty') }}

),

team_fixtures as (

    select
        team_h as team_id,
        fixture_id,
        gameweek,
        team_h_difficulty as difficulty,
        kickoff_time

    from fixtures

    union all

    select
        team_a as team_id,
        fixture_id,
        gameweek,
        team_a_difficulty as difficulty,
        kickoff_time

    from fixtures

),

future_fixtures as (

    select
        team_id,
        fixture_id,
        gameweek,
        difficulty,
        kickoff_time,

        row_number() over (
            partition by team_id
            order by kickoff_time
        ) as fixture_number

    from team_fixtures

    where kickoff_time::timestamp with time zone >= current_timestamp

),

next5 as (

    select
        team_id,

        avg(difficulty) as avg_difficulty_next5

    from future_fixtures

    where fixture_number <= 5

    group by team_id

)

select
    team_id,
    avg_difficulty_next5

from next5