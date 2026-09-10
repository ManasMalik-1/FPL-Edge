import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=True)

app = FastAPI(title="FPL Edge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    if database_url == "YOUR_DATABASE_URL":
        raise RuntimeError(
            "DATABASE_URL is still set to the placeholder YOUR_DATABASE_URL"
        )

    return psycopg2.connect(database_url)


@app.get("/")
def root():
    return {
        "name": "FPL Edge API",
        "status": "running"
    }


@app.get("/recommendations")
def get_recommendations(limit: int = 20):

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100"
        )

    query = """
        SELECT
            r.player_id,
            r.player_name,
            r.position_id,
            r.price,
            r.form,
            r.selected_by_percent,

            r.next_gameweek,
            r.next_opponent_team_id,
            r.next_is_home,
            r.next_fixture_difficulty,

            r.avg_fixture_difficulty,
            r.recommendation_score_rounded

        FROM analytics.player_recommendations r

        ORDER BY r.recommendation_score_rounded DESC

        LIMIT %s;
    """

    team_query = """
        SELECT
            id,
            name,
            short_name
        FROM raw.fpl_teams;
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # Get recommendations
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

            # Get team names once
            cursor.execute(team_query)
            teams = cursor.fetchall()

            team_map = {
                team_id: {
                    "name": name,
                    "short_name": short_name
                }
                for team_id, name, short_name in teams
            }

            columns = [
                "player_id",
                "player_name",
                "position_id",
                "price",
                "form",
                "selected_by_percent",
                "next_gameweek",
                "next_opponent_team_id",
                "next_is_home",
                "next_fixture_difficulty",
                "avg_fixture_difficulty",
                "recommendation_score"
            ]

            recommendations = []

            for row in rows:

                player = dict(zip(columns, row))

                opponent = team_map.get(
                    player["next_opponent_team_id"]
                )

                if opponent:
                    player["next_opponent"] = opponent["name"]
                    player["next_opponent_short"] = opponent["short_name"]
                else:
                    player["next_opponent"] = "Unknown"
                    player["next_opponent_short"] = "?"

                player["venue"] = (
                    "Home"
                    if player["next_is_home"]
                    else "Away"
                )

                recommendations.append(player)

            return recommendations

    finally:
        conn.close()