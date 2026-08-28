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

    df.to_sql(
        table,
        engine,
        schema=schema,
        if_exists=if_exists,
        index=False
    )