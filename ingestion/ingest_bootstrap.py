import logging
from datetime import datetime, timezone

from ingestion.db import get_engine
from ingestion.fpl_client import get_bootstrap
from sqlalchemy import text


logger = logging.getLogger(__name__)


def load_bootstrap():
    logger.info("Starting FPL bootstrap ingestion")

    data = get_bootstrap()

    players = data.get("elements", [])

    logger.info("Fetched %s players from FPL API", len(players))

    return data


def save_bootstrap(data, source_file):
    engine = get_engine()

    players = data.get("elements", [])

    if not players:
        logger.warning("No players found in bootstrap data")
        return 0

    ingested_at = datetime.now(timezone.utc)

    logger.info(
        "Loading %s players into raw.fpl_players",
        len(players)
    )

    with engine.begin() as connection:
        for player in players:
            connection.execute(
                text("""
                    INSERT INTO raw.fpl_players (
                        id,
                        first_name,
                        second_name,
                        web_name,
                        team,
                        element_type,
                        now_cost,
                        total_points,
                        event_points,
                        form,
                        selected_by_percent,
                        minutes,
                        goals_scored,
                        assists,
                        clean_sheets,
                        goals_conceded,
                        own_goals,
                        penalties_saved,
                        penalties_missed,
                        yellow_cards,
                        red_cards,
                        saves,
                        bonus,
                        bps,
                        influence,
                        creativity,
                        threat,
                        ict_index,
                        expected_goals,
                        expected_assists,
                        expected_goal_involvements,
                        expected_goals_conceded,
                        _ingested_at,
                        _source_file
                    )
                    VALUES (
                        :id,
                        :first_name,
                        :second_name,
                        :web_name,
                        :team,
                        :element_type,
                        :now_cost,
                        :total_points,
                        :event_points,
                        :form,
                        :selected_by_percent,
                        :minutes,
                        :goals_scored,
                        :assists,
                        :clean_sheets,
                        :goals_conceded,
                        :own_goals,
                        :penalties_saved,
                        :penalties_missed,
                        :yellow_cards,
                        :red_cards,
                        :saves,
                        :bonus,
                        :bps,
                        :influence,
                        :creativity,
                        :threat,
                        :ict_index,
                        :expected_goals,
                        :expected_assists,
                        :expected_goal_involvements,
                        :expected_goals_conceded,
                        :_ingested_at,
                        :_source_file
                    )
                """),
                {
                    "id": player.get("id"),
                    "first_name": player.get("first_name"),
                    "second_name": player.get("second_name"),
                    "web_name": player.get("web_name"),
                    "team": player.get("team"),
                    "element_type": player.get("element_type"),
                    "now_cost": player.get("now_cost"),
                    "total_points": player.get("total_points"),
                    "event_points": player.get("event_points"),
                    "form": player.get("form"),
                    "selected_by_percent": player.get("selected_by_percent"),
                    "minutes": player.get("minutes"),
                    "goals_scored": player.get("goals_scored"),
                    "assists": player.get("assists"),
                    "clean_sheets": player.get("clean_sheets"),
                    "goals_conceded": player.get("goals_conceded"),
                    "own_goals": player.get("own_goals"),
                    "penalties_saved": player.get("penalties_saved"),
                    "penalties_missed": player.get("penalties_missed"),
                    "yellow_cards": player.get("yellow_cards"),
                    "red_cards": player.get("red_cards"),
                    "saves": player.get("saves"),
                    "bonus": player.get("bonus"),
                    "bps": player.get("bps"),
                    "influence": player.get("influence"),
                    "creativity": player.get("creativity"),
                    "threat": player.get("threat"),
                    "ict_index": player.get("ict_index"),
                    "expected_goals": player.get("expected_goals"),
                    "expected_assists": player.get("expected_assists"),
                    "expected_goal_involvements": player.get(
                        "expected_goal_involvements"
                    ),
                    "expected_goals_conceded": player.get(
                        "expected_goals_conceded"
                    ),
                    "_ingested_at": ingested_at,
                    "_source_file": source_file,
                }
            )

    logger.info(
        "Bootstrap ingestion completed: %s players loaded",
        len(players)
    )

    return len(players)