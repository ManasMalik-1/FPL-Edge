select
    player_id,
    gameweek,
    fixture,
    count(*) as record_count
from {{ ref('fct_player_gameweek') }}
group by
    player_id,
    gameweek,
    fixture
having count(*) > 1