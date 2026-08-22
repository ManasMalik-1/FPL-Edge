from sqlalchemy import text
from database.connection import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    print("Database connected successfully!")
    print(result.fetchone()[0])