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
        min(fixture_difficulty) as next_fixture_difficulty,
        avg(fixture_difficulty) as avg_fixture_difficulty
    from {{ ref('player_fixture_context') }}

    where finished = false

    group by player_id

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

        coalesce(f.next_fixture_difficulty, 5) as next_fixture_difficulty,
        coalesce(f.avg_fixture_difficulty, 5) as avg_fixture_difficulty

    from value v

    left join performance p
        on v.player_id = p.player_id

    left join fixtures f
        on v.player_id = f.player_id

),

scored as (

    select
        *,

        (
            coalesce(points_per_million, 0) * 0.30
            +
            coalesce(points_per_match, 0) * 0.25
            +
            coalesce(xgi_per_million, 0) * 0.15
            +
            coalesce(nullif(form, '')::numeric, 0) * 0.15
            +
            (6 - next_fixture_difficulty) * 0.15
        ) as recommendation_score

    from combined

)

select
    *,
    round(recommendation_score, 2) as recommendation_score_rounded

from scored

order by recommendation_score desc