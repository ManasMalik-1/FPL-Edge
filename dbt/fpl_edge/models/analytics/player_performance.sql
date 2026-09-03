with history as (

    select *
    from {{ ref('stg_fpl_player_history') }}

),

performance as (

    select
        player_id,

        count(distinct fixture) as fixtures_played,

        sum(minutes) as minutes,

        sum(total_points) as total_points,

        sum(goals_scored) as goals,
        sum(assists) as assists,

        sum(clean_sheets) as clean_sheets,
        sum(goals_conceded) as goals_conceded,

        sum(bonus) as bonus,
        sum(bps) as bps,

        sum(cast(expected_goals as numeric)) as xg,
        sum(cast(expected_assists as numeric)) as xa,

        sum(cast(expected_goal_involvements as numeric)) as xgi,
        sum(cast(expected_goals_conceded as numeric)) as xgc,

        sum(saves) as saves,

        max(round) as latest_gameweek

    from history

    group by player_id

),

final as (

    select
        player_id,
        fixtures_played,
        minutes,

        total_points,

        goals,
        assists,

        clean_sheets,
        goals_conceded,

        bonus,
        bps,

        xg,
        xa,
        xgi,
        xgc,

        saves,

        latest_gameweek,

        round(
   	   case
       		 when fixtures_played > 0
      		  then total_points * 1.0 / fixtures_played
     		   else 0
  	  end,
    	  2
	) as points_per_match,

        round(
            case
                when minutes >= 180
                then xg * 90.0 / minutes
                else 0
            end,
            2
        ) as xg_per_90,

        round(
            case
                when minutes >= 180
                then xa * 90.0 / minutes
                else 0
            end,
            2
        ) as xa_per_90

    from performance

)
select *
from final