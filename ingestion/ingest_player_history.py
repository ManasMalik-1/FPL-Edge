import logging
from datetime import datetime, timezone
from pathlib import Path
import json
import time

import pandas as pd

from .db import (
    finish_pipeline_run,
    get_existing_player_fixtures,
    get_latest_finished_gameweek,
    get_last_successful_gameweek,
    load_dataframe,
    start_pipeline_run,
)
from .fpl_client import FPLClient


logger = logging.getLogger(__name__)


PIPELINE_NAME = "player_history"

RAW_DIR = Path("data/raw/player_history")
BOOTSTRAP_DIR = Path("data/raw/bootstrap")

REQUEST_DELAY = 0.5


def load_player_ids():
    """Load player IDs from the latest bootstrap raw JSON."""

    bootstrap_files = sorted(
        BOOTSTRAP_DIR.glob("*.json")
    )

    if not bootstrap_files:
        raise FileNotFoundError(
            "No bootstrap JSON files found."
        )

    latest_file = bootstrap_files[-1]

    logger.info(
        "Using bootstrap file: %s",
        latest_file
    )

    with latest_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        payload = json.load(file)

    player_ids = [
        player["id"]
        for player in payload["elements"]
    ]

    return player_ids


def save_raw_json(payload, player_id):
    """Save one player's complete history response."""

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ingestion_date = datetime.now(
        timezone.utc
    ).strftime("%Y-%m-%d")

    output_file = (
        RAW_DIR
        / f"{ingestion_date}_player_{player_id}.json"
    )

    if output_file.exists():
        logger.info(
            "Raw history already exists for player %s: %s",
            player_id,
            output_file
        )
        return output_file

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            payload,
            file,
            ensure_ascii=False,
            indent=2
        )

    return output_file


def normalize_history(
    payload,
    player_id,
    source_file
):
    """Convert player history into a DataFrame."""

    df = pd.DataFrame(
        payload["history"]
    )

    df["player_id"] = player_id

    df["_ingested_at"] = datetime.now(
        timezone.utc
    )

    df["_source_file"] = str(
        source_file
    )

    return df


def main():

    logger.info(
        "Starting player history ingestion..."
    )

    # ---------------------------------------------------------
    # 1. Determine gameweek state
    # ---------------------------------------------------------

    latest_finished_gw = (
        get_latest_finished_gameweek()
    )

    last_loaded_gw = (
        get_last_successful_gameweek(
            PIPELINE_NAME
        )
    )

    logger.info(
        "Latest finished GW: %s",
        latest_finished_gw
    )

    logger.info(
        "Last successfully loaded GW: %s",
        last_loaded_gw
    )

    # ---------------------------------------------------------
    # 2. Start pipeline run
    # ---------------------------------------------------------

    run_id = start_pipeline_run(
        PIPELINE_NAME
    )

    logger.info(
        "Started pipeline run: %s",
        run_id
    )

    # ---------------------------------------------------------
    # 3. Skip if there is no new completed gameweek
    # ---------------------------------------------------------

    if latest_finished_gw <= last_loaded_gw:

        finish_pipeline_run(
            run_id=run_id,
            status="SKIPPED",
            rows_loaded=0,
            max_gameweek_loaded=last_loaded_gw
        )

        logger.info(
            "No new completed gameweek. "
            "Skipping player history refresh."
        )

        return

    # ---------------------------------------------------------
    # 4. Start actual ingestion
    # ---------------------------------------------------------

    successful = 0
    failed = 0
    total_rows_loaded = 0

    try:

        player_ids = load_player_ids()

        logger.info(
            "Found %s players in bootstrap data.",
            len(player_ids)
        )

        # -----------------------------------------------------
        # Load existing player/fixture keys ONCE.
        # -----------------------------------------------------

        existing_keys = (
            get_existing_player_fixtures()
        )

        logger.info(
            "Existing player/fixture records: %s",
            len(existing_keys)
        )

        client = FPLClient()

        # -----------------------------------------------------
        # 5. Process each player
        # -----------------------------------------------------

        for index, player_id in enumerate(
            player_ids,
            start=1
        ):

            logger.info(
                "[%s/%s] Processing player %s...",
                index,
                len(player_ids),
                player_id
            )

            try:

                payload = client.get(
                    f"element-summary/{player_id}/"
                )

                source_file = save_raw_json(
                    payload,
                    player_id
                )

                df = normalize_history(
                    payload,
                    player_id,
                    source_file
                )

                # -------------------------------------------------
                # 6. Remove already-existing player/fixture rows
                # -------------------------------------------------

                if not df.empty:

                    df["history_key"] = list(
                        zip(
                            df["player_id"],
                            df["fixture"]
                        )
                    )

                    df = df[
                        ~df["history_key"].isin(
                            existing_keys
                        )
                    ].copy()

                    df.drop(
                        columns=["history_key"],
                        inplace=True
                    )

                    # ---------------------------------------------
                    # 7. Load only genuinely new rows
                    # ---------------------------------------------

                    if not df.empty:

                        load_dataframe(
                            df=df,
                            table="fpl_player_history",
                            schema="raw",
                            if_exists="append"
                        )

                        # Add newly inserted keys to the
                        # in-memory set so duplicates cannot
                        # occur during the same run.

                        existing_keys.update(
                            zip(
                                df["player_id"],
                                df["fixture"]
                            )
                        )

                        total_rows_loaded += len(df)

                successful += 1

                logger.info(
                    "  ✓ New rows loaded: %s",
                    len(df)
                )

            except Exception as error:

                failed += 1

                logger.error(
                    "  ✗ Player %s failed: %s",
                    player_id,
                    error
                )

            # -------------------------------------------------
            # Respect the FPL API
            # -------------------------------------------------

            if index < len(player_ids):

                time.sleep(
                    REQUEST_DELAY
                )

        # -----------------------------------------------------
        # 8. Handle partial failure
        # -----------------------------------------------------

        if failed > 0:

            finish_pipeline_run(
                run_id=run_id,
                status="FAILED",
                rows_loaded=total_rows_loaded,
                max_gameweek_loaded=last_loaded_gw,
                error_message=(
                    f"{failed} player requests failed."
                )
            )

            logger.info(
                "Player history ingestion completed with failures."
            )
            logger.info(
                "Successful: %s",
                successful
            )
            logger.info(
                "Failed: %s",
                failed
            )
            logger.info(
                "New rows loaded: %s",
                total_rows_loaded
            )

            return

        # -----------------------------------------------------
        # 9. Record successful run + watermark
        # -----------------------------------------------------

        finish_pipeline_run(
            run_id=run_id,
            status="SUCCESS",
            rows_loaded=total_rows_loaded,
            max_gameweek_loaded=latest_finished_gw
        )

        logger.info(
            "Player history ingestion completed successfully."
        )
        logger.info(
            "Successful: %s",
            successful
        )
        logger.info(
            "Failed: %s",
            failed
        )
        logger.info(
            "New rows loaded: %s",
            total_rows_loaded
        )
        logger.info(
            "Watermark updated to GW %s",
            latest_finished_gw
        )

    except Exception as error:

        # -----------------------------------------------------
        # 10. Handle unexpected pipeline-level failure
        # -----------------------------------------------------

        finish_pipeline_run(
            run_id=run_id,
            status="FAILED",
            rows_loaded=total_rows_loaded,
            max_gameweek_loaded=last_loaded_gw,
            error_message=str(error)
        )

        logger.exception(
            "Player history ingestion failed unexpectedly."
        )

        raise


if __name__ == "__main__":
    main()