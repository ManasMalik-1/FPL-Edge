with fixtures as (

    select
        fixture_id,
        gameweek,
        team_h,
        team_a,
        team_h_difficulty,
        team_a_difficulty,
        kickoff_time,
        finished,

        row_number() over (
            partition by fixture_id
            order by kickoff_time desc
        ) as rn

    from {{ ref('stg_fpl_fixtures') }}

),

final as (

    select
        fixture_id,
        gameweek,
        team_h,
        team_a,
        team_h_difficulty,
        team_a_difficulty,
        kickoff_time,
        finished

    from fixtures

    where rn = 1

)

select *
from final