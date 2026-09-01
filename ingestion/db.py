import json
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine, text

from .config import DATABASE_URL


def get_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )


def get_connection():
    engine = get_engine()
    return engine.connect()


def load_dataframe(df, table, schema="raw", if_exists="append"):
    engine = get_engine()

    df = df.copy()

    # Convert nested API objects into JSON strings
    # so PostgreSQL can store them safely.
    for column in df.columns:
        if df[column].apply(
            lambda value: isinstance(value, (dict, list))
        ).any():
            df[column] = df[column].apply(
                lambda value: json.dumps(value)
                if isinstance(value, (dict, list))
                else value
            )

    df.to_sql(
        table,
        engine,
        schema=schema,
        if_exists=if_exists,
        index=False
    )


def start_pipeline_run(pipeline_name):
    engine = get_engine()

    started_at = datetime.now(timezone.utc)

    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO raw.pipeline_runs (
                    pipeline_name,
                    started_at,
                    status
                )
                VALUES (
                    :pipeline_name,
                    :started_at,
                    'RUNNING'
                )
                RETURNING run_id
            """),
            {
                "pipeline_name": pipeline_name,
                "started_at": started_at
            }
        )

        run_id = result.scalar()

    return run_id


def finish_pipeline_run(
    run_id,
    status,
    rows_loaded=None,
    max_gameweek_loaded=None,
    error_message=None
):
    engine = get_engine()

    finished_at = datetime.now(timezone.utc)

    with engine.begin() as connection:
        connection.execute(
            text("""
                UPDATE raw.pipeline_runs
                SET
                    finished_at = :finished_at,
                    status = :status,
                    rows_loaded = :rows_loaded,
                    max_gameweek_loaded = :max_gameweek_loaded,
                    error_message = :error_message
                WHERE run_id = :run_id
            """),
            {
                "run_id": run_id,
                "finished_at": finished_at,
                "status": status,
                "rows_loaded": rows_loaded,
                "max_gameweek_loaded": max_gameweek_loaded,
                "error_message": error_message
            }
        )


def get_last_successful_gameweek(pipeline_name):
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COALESCE(MAX(max_gameweek_loaded), 0)
                FROM raw.pipeline_runs
                WHERE pipeline_name = :pipeline_name
                  AND status = 'SUCCESS'
            """),
            {
                "pipeline_name": pipeline_name
            }
        )

        return result.scalar()


def get_latest_finished_gameweek():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT COALESCE(MAX(id), 0)
                FROM raw.fpl_events
                WHERE finished = TRUE
            """)
        )

        return result.scalar()


def should_refresh_player_history(pipeline_name):
    latest_finished = get_latest_finished_gameweek()
    last_loaded = get_last_successful_gameweek(pipeline_name)

    return latest_finished > last_loaded


def get_existing_player_fixtures():
    """
    Return existing (player_id, fixture) pairs from raw history.
    Used for bulk duplicate filtering.
    """

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT player_id, fixture
                FROM raw.fpl_player_history
            """)
        )

        return {
            (row.player_id, row.fixture)
            for row in result
        }


def fixture_history_exists(player_id, fixture):
    """
    Check whether one player/fixture combination already exists.

    Useful for testing/debugging. Production ingestion uses the
    bulk get_existing_player_fixtures() helper instead.
    """

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT EXISTS (
                    SELECT 1
                    FROM raw.fpl_player_history
                    WHERE player_id = :player_id
                      AND fixture = :fixture
                )
            """),
            {
                "player_id": player_id,
                "fixture": fixture
            }
        )

        return result.scalar()