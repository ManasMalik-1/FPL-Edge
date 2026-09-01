from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd

from .db import load_dataframe
from .fpl_client import FPLClient


RAW_DIR = Path("data/raw/fixtures")


def save_raw_json(payload):
    """Save the complete fixtures API response."""

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_file = RAW_DIR / f"{ingestion_date}.json"

    if output_file.exists():
        print(f"Raw fixtures file already exists: {output_file}")
        return output_file

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)

    return output_file


def normalize_fixtures(payload, source_file):
    """Convert fixtures payload into a DataFrame."""

    df = pd.DataFrame(payload)

    df["_ingested_at"] = datetime.now(timezone.utc)
    df["_source_file"] = str(source_file)

    return df


def main():
    print("Starting FPL fixtures ingestion...")

    client = FPLClient()

    payload = client.get("fixtures/")

    print(f"Received {len(payload)} fixtures.")

    source_file = save_raw_json(payload)

    print(f"Raw JSON saved to {source_file}")

    df = normalize_fixtures(
        payload,
        source_file
    )

    print(f"Prepared {len(df)} fixture rows.")

    load_dataframe(
        df=df,
        table="fpl_fixtures",
        schema="raw",
        if_exists="append"
    )

    print(
        f"Loaded {len(df)} rows into raw.fpl_fixtures"
    )

    print("Fixtures ingestion completed successfully.")


if __name__ == "__main__":
    main()