with fixtures as (

    select *
    from {{ ref('stg_fpl_fixtures') }}

),

final as (

    select
        gameweek,
        fixture_id,

        team_h,
        team_a,

        team_h_difficulty,
        team_a_difficulty,

        kickoff_time,

        finished

    from fixtures

)

select *
from final