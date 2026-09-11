select *
from {{ ref('dim_player') }}
where price < 3.5
   or price > 16.0