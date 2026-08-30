import json

from sqlalchemy import create_engine
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