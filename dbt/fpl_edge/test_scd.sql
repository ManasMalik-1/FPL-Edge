BEGIN;

UPDATE raw.fpl_players
SET now_cost = 50
WHERE id = 2
  AND _ingested_at = (
      SELECT MAX(_ingested_at)
      FROM raw.fpl_players
      WHERE id = 2
  );

SELECT id, web_name, now_cost, _ingested_at
FROM raw.fpl_players
WHERE id = 2
ORDER BY _ingested_at DESC
LIMIT 1;

ROLLBACK;