with performance as (

    select
        player_id,
        fixtures_played,
        minutes,
        total_points,
        goals,
        assists,
        xg,
        xa,
        xgi,
        points_per_match,
        xg_per_90,
        xa_per_90
    from {{ ref('player_performance') }}

),

value as (

    select
        player_id,
        player_name,
        position_id,
        price,
        points_per_million,
        xgi_per_million,
        form,
        selected_by_percent
    from {{ ref('player_value') }}

),

fixtures as (

    select
        player_id,
        gameweek,
        opponent_team_id,
        is_home,
        fixture_difficulty,

        avg(fixture_difficulty) over (
            partition by player_id
        ) as avg_fixture_difficulty,

        avg(opponent_defence_strength) over (
            partition by player_id
        ) as avg_opponent_defence_strength,

        first_value(opponent_team_id) over (
            partition by player_id
            order by kickoff_time
        ) as next_opponent_team_id,

        first_value(gameweek) over (
            partition by player_id
            order by kickoff_time
        ) as next_gameweek,

        first_value(is_home) over (
            partition by player_id
            order by kickoff_time
        ) as next_is_home,

        first_value(fixture_difficulty) over (
            partition by player_id
            order by kickoff_time
        ) as next_fixture_difficulty

    from {{ ref('player_fixture_context') }}

    where finished = false

),

fixture_summary as (

    select distinct
        player_id,
        next_gameweek,
        next_opponent_team_id,
        next_is_home,
        next_fixture_difficulty,
        avg_fixture_difficulty,
        avg_opponent_defence_strength

    from fixtures

),

combined as (

    select
        v.player_id,
        v.player_name,
        v.position_id,
        v.price,

        p.fixtures_played,
        p.minutes,
        p.total_points,
        p.goals,
        p.assists,

        p.xg,
        p.xa,
        p.xgi,

        p.points_per_match,
        p.xg_per_90,
        p.xa_per_90,

        v.points_per_million,
        v.xgi_per_million,
        v.form,
        v.selected_by_percent,

        f.next_gameweek,
        f.next_opponent_team_id,
        f.next_is_home,
        f.next_fixture_difficulty,
        f.avg_fixture_difficulty,
        f.avg_opponent_defence_strength

    from value v

    left join performance p
        on v.player_id = p.player_id

    left join fixture_summary f
        on v.player_id = f.player_id

),

scored as (

    select
        *,

        (
            coalesce(points_per_million, 0) * 0.25
            +
            coalesce(points_per_match, 0) * 0.20
            +
            coalesce(xgi_per_million, 0) * 0.15
            +
            coalesce(nullif(form, '')::numeric, 0) * 0.15
            +
            (6 - coalesce(next_fixture_difficulty, 5)) * 0.10
            +
            (6 - coalesce(avg_opponent_defence_strength, 5)) * 0.15

        ) as recommendation_score

    from combined

)

select
    player_id,
    player_name,
    position_id,
    price,

    form,
    selected_by_percent,

    next_gameweek,
    next_opponent_team_id,
    next_is_home,
    next_fixture_difficulty,

    avg_fixture_difficulty,
    avg_opponent_defence_strength,

    round(recommendation_score, 2)
        as recommendation_score_rounded,

    recommendation_score

from scored

order by recommendation_score desc