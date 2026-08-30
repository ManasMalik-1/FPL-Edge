from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd
import requests

from .db import load_dataframe


BASE_URL = "https://fantasy.premierleague.com/api/"
RAW_DIR = Path("data/raw/bootstrap")


def fetch_bootstrap():
    """Fetch the complete bootstrap-static payload from the FPL API."""

    url = f"{BASE_URL}bootstrap-static/"

    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "FPL-Edge/1.0"
        }
    )

    response.raise_for_status()

    return response.json()


def save_raw_json(payload):
    """Save the complete API response as immutable raw JSON."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_file = RAW_DIR / f"{ingestion_date}.json"

    # Don't overwrite an existing raw file.
    if output_file.exists():
        print(f"Raw JSON already exists: {output_file}")
        return output_file

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return output_file


def normalize_payload(payload, source_file):
    """Convert the four required API sections into DataFrames."""

    ingested_at = datetime.now(timezone.utc)

    dataframes = {
        "fpl_players": pd.DataFrame(payload["elements"]),
        "fpl_teams": pd.DataFrame(payload["teams"]),
        "fpl_events": pd.DataFrame(payload["events"]),
        "fpl_element_types": pd.DataFrame(payload["element_types"]),
    }

    for df in dataframes.values():
        df["_ingested_at"] = ingested_at
        df["_source_file"] = str(source_file)

    return dataframes


def load_to_postgres(dataframes):
    """Append normalized data into the PostgreSQL raw schema."""

    for table_name, df in dataframes.items():
        load_dataframe(
            df=df,
            table=table_name,
            schema="raw",
            if_exists="append",
        )

        print(f"Loaded {len(df)} rows into raw.{table_name}")


def main():
    print("Starting FPL bootstrap ingestion...")

    payload = fetch_bootstrap()
    print("FPL bootstrap API request successful.")

    source_file = save_raw_json(payload)
    print(f"Raw JSON saved to {source_file}")

    dataframes = normalize_payload(
        payload,
        source_file
    )

    for table_name, df in dataframes.items():
        print(f"{table_name}: {len(df)} rows")

    load_to_postgres(dataframes)

    print("Bootstrap ingestion completed successfully.")


if __name__ == "__main__":
    main()