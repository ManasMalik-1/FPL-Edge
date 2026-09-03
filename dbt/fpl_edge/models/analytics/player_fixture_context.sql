with players as (

    select
        player_id,
        player_name,
        team_id,
        position_id,
        price,
        total_points,
        form
    from {{ ref('stg_fpl_players') }}

),

fixtures as (

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

player_fixtures as (

    select
        p.player_id,
        p.player_name,
        p.team_id,
        p.position_id,
        p.price,
        p.total_points,
        p.form,

        f.fixture_id,
        f.gameweek,
        f.kickoff_time,
        f.finished,

        case
            when p.team_id = f.team_h
                then f.team_h_difficulty
            when p.team_id = f.team_a
                then f.team_a_difficulty
        end as fixture_difficulty,

        case
            when p.team_id = f.team_h
                then f.team_a
            when p.team_id = f.team_a
                then f.team_h
        end as opponent_team_id

    from players p

    inner join fixtures f
        on p.team_id = f.team_h
        or p.team_id = f.team_a

)

select *
from player_fixtures