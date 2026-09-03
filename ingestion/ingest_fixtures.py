import json
import logging
from datetime import datetime, timezone

from ingestion.db import get_engine
from ingestion.fpl_client import get_fixtures
from sqlalchemy import text


logger = logging.getLogger(__name__)


def load_fixtures():
    logger.info("Starting FPL fixtures ingestion")

    fixtures = get_fixtures()

    logger.info(
        "Fetched %s fixtures from FPL API",
        len(fixtures)
    )

    return fixtures


def save_fixtures(fixtures, source_file):
    engine = get_engine()

    if not fixtures:
        logger.warning("No fixtures found")
        return 0

    ingested_at = datetime.now(timezone.utc)

    logger.info(
        "Loading %s fixtures into raw.fpl_fixtures",
        len(fixtures)
    )

    with engine.begin() as connection:
        for fixture in fixtures:
            connection.execute(
                text("""
                    INSERT INTO raw.fpl_fixtures (
                        code,
                        event,
                        finished,
                        finished_provisional,
                        id,
                        kickoff_time,
                        minutes,
                        provisional_start_time,
                        started,
                        team_a,
                        team_a_score,
                        team_h,
                        team_h_score,
                        stats,
                        team_h_difficulty,
                        team_a_difficulty,
                        pulse_id,
                        _ingested_at,
                        _source_file
                    )
                    VALUES (
                        :code,
                        :event,
                        :finished,
                        :finished_provisional,
                        :id,
                        :kickoff_time,
                        :minutes,
                        :provisional_start_time,
                        :started,
                        :team_a,
                        :team_a_score,
                        :team_h,
                        :team_h_score,
                        :stats,
                        :team_h_difficulty,
                        :team_a_difficulty,
                        :pulse_id,
                        :_ingested_at,
                        :_source_file
                    )
                """),
                {
                    "code": fixture.get("code"),
                    "event": fixture.get("event"),
                    "finished": fixture.get("finished"),
                    "finished_provisional": fixture.get(
                        "finished_provisional"
                    ),
                    "id": fixture.get("id"),
                    "kickoff_time": fixture.get("kickoff_time"),
                    "minutes": fixture.get("minutes"),
                    "provisional_start_time": fixture.get(
                        "provisional_start_time"
                    ),
                    "started": fixture.get("started"),
                    "team_a": fixture.get("team_a"),
                    "team_a_score": fixture.get("team_a_score"),
                    "team_h": fixture.get("team_h"),
                    "team_h_score": fixture.get("team_h_score"),
                    "stats": json.dumps(
                        fixture.get("stats")
                    ) if fixture.get("stats") is not None else None,
                    "team_h_difficulty": fixture.get(
                        "team_h_difficulty"
                    ),
                    "team_a_difficulty": fixture.get(
                        "team_a_difficulty"
                    ),
                    "pulse_id": fixture.get("pulse_id"),
                    "_ingested_at": ingested_at,
                    "_source_file": source_file,
                }
            )

    logger.info(
        "Fixtures ingestion completed: %s fixtures loaded",
        len(fixtures)
    )

    return len(fixtures)