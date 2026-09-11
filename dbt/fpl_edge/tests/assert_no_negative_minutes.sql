select *
from {{ ref('fct_player_gameweek') }}
where minutes < 0