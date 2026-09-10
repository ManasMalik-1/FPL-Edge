import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'analytics'
      AND table_name = 'team_strength'
    ORDER BY ordinal_position
""")

for row in cur.fetchall():
    print(row)

cur.close()
conn.close()