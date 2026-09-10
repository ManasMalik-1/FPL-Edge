import json
import logging
from datetime import datetime, timezone

from ingestion.db import get_engine
from ingestion.fpl_client import get_bootstrap
from sqlalchemy import text


logger = logging.getLogger(__name__)


def serialize(value):
    """
    Convert nested API objects/lists into JSON strings.
    PostgreSQL stores these columns as text.
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return value


def load_bootstrap():
    logger.info("Starting FPL bootstrap ingestion")

    data = get_bootstrap()

    players = data.get("elements", [])
    teams = data.get("teams", [])
    events = data.get("events", [])

    logger.info("Fetched %s players from FPL API", len(players))
    logger.info("Fetched %s teams from FPL API", len(teams))
    logger.info("Fetched %s gameweeks from FPL API", len(events))

    return data


def save_bootstrap(data, source_file):
    engine = get_engine()

    players = data.get("elements", [])
    teams = data.get("teams", [])
    events = data.get("events", [])

    if not players:
        logger.warning("No players found in bootstrap data")
        return 0

    ingested_at = datetime.now(timezone.utc)

    with engine.begin() as connection:

        # =========================================================
        # PLAYERS
        # =========================================================

        logger.info(
            "Loading %s players into raw.fpl_players",
            len(players)
        )

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

        # =========================================================
        # TEAMS
        # =========================================================

        logger.info(
            "Refreshing raw.fpl_teams with %s teams",
            len(teams)
        )

        connection.execute(
            text("DELETE FROM raw.fpl_teams")
        )

        for team in teams:
            connection.execute(
                text("""
                    INSERT INTO raw.fpl_teams (
                        code,
                        draw,
                        form,
                        id,
                        loss,
                        name,
                        played,
                        points,
                        position,
                        short_name,
                        strength,
                        team_division,
                        unavailable,
                        win,
                        link_url,
                        strength_overall_home,
                        strength_overall_away,
                        strength_attack_home,
                        strength_attack_away,
                        strength_defence_home,
                        strength_defence_away,
                        pulse_id,
                        _ingested_at,
                        _source_file
                    )
                    VALUES (
                        :code,
                        :draw,
                        :form,
                        :id,
                        :loss,
                        :name,
                        :played,
                        :points,
                        :position,
                        :short_name,
                        :strength,
                        :team_division,
                        :unavailable,
                        :win,
                        :link_url,
                        :strength_overall_home,
                        :strength_overall_away,
                        :strength_attack_home,
                        :strength_attack_away,
                        :strength_defence_home,
                        :strength_defence_away,
                        :pulse_id,
                        :_ingested_at,
                        :_source_file
                    )
                """),
                {
                    "code": team.get("code"),
                    "draw": team.get("draw"),
                    "form": team.get("form"),
                    "id": team.get("id"),
                    "loss": team.get("loss"),
                    "name": team.get("name"),
                    "played": team.get("played"),
                    "points": team.get("points"),
                    "position": team.get("position"),
                    "short_name": team.get("short_name"),
                    "strength": team.get("strength"),
                    "team_division": team.get("team_division"),
                    "unavailable": team.get("unavailable"),
                    "win": team.get("win"),
                    "link_url": team.get("link_url"),
                    "strength_overall_home": team.get(
                        "strength_overall_home"
                    ),
                    "strength_overall_away": team.get(
                        "strength_overall_away"
                    ),
                    "strength_attack_home": team.get(
                        "strength_attack_home"
                    ),
                    "strength_attack_away": team.get(
                        "strength_attack_away"
                    ),
                    "strength_defence_home": team.get(
                        "strength_defence_home"
                    ),
                    "strength_defence_away": team.get(
                        "strength_defence_away"
                    ),
                    "pulse_id": team.get("pulse_id"),
                    "_ingested_at": ingested_at,
                    "_source_file": source_file,
                }
            )

        # =========================================================
        # EVENTS / GAMEWEEKS
        # =========================================================

        logger.info(
            "Refreshing raw.fpl_events with %s gameweeks",
            len(events)
        )

        connection.execute(
            text("DELETE FROM raw.fpl_events")
        )

        for event in events:
            connection.execute(
                text("""
                    INSERT INTO raw.fpl_events (
                        id,
                        name,
                        deadline_time,
                        release_time,
                        average_entry_score,
                        finished,
                        data_checked,
                        highest_scoring_entry,
                        deadline_time_epoch,
                        deadline_time_game_offset,
                        highest_score,
                        is_previous,
                        is_current,
                        is_next,
                        cup_leagues_created,
                        h2h_ko_matches_created,
                        can_enter,
                        can_manage,
                        released,
                        ranked_count,
                        overrides,
                        chip_plays,
                        most_selected,
                        most_transferred_in,
                        top_element,
                        top_element_info,
                        transfers_made,
                        most_captained,
                        most_vice_captained,
                        _ingested_at,
                        _source_file
                    )
                    VALUES (
                        :id,
                        :name,
                        :deadline_time,
                        :release_time,
                        :average_entry_score,
                        :finished,
                        :data_checked,
                        :highest_scoring_entry,
                        :deadline_time_epoch,
                        :deadline_time_game_offset,
                        :highest_score,
                        :is_previous,
                        :is_current,
                        :is_next,
                        :cup_leagues_created,
                        :h2h_ko_matches_created,
                        :can_enter,
                        :can_manage,
                        :released,
                        :ranked_count,
                        :overrides,
                        :chip_plays,
                        :most_selected,
                        :most_transferred_in,
                        :top_element,
                        :top_element_info,
                        :transfers_made,
                        :most_captained,
                        :most_vice_captained,
                        :_ingested_at,
                        :_source_file
                    )
                """),
                {
                    "id": event.get("id"),
                    "name": event.get("name"),
                    "deadline_time": event.get("deadline_time"),
                    "release_time": event.get("release_time"),
                    "average_entry_score": event.get(
                        "average_entry_score"
                    ),
                    "finished": event.get("finished"),
                    "data_checked": event.get("data_checked"),
                    "highest_scoring_entry": event.get(
                        "highest_scoring_entry"
                    ),
                    "deadline_time_epoch": event.get(
                        "deadline_time_epoch"
                    ),
                    "deadline_time_game_offset": event.get(
                        "deadline_time_game_offset"
                    ),
                    "highest_score": event.get("highest_score"),
                    "is_previous": event.get("is_previous"),
                    "is_current": event.get("is_current"),
                    "is_next": event.get("is_next"),
                    "cup_leagues_created": event.get(
                        "cup_leagues_created"
                    ),
                    "h2h_ko_matches_created": event.get(
                        "h2h_ko_matches_created"
                    ),
                    "can_enter": event.get("can_enter"),
                    "can_manage": event.get("can_manage"),
                    "released": event.get("released"),
                    "ranked_count": event.get("ranked_count"),
                    "overrides": serialize(event.get("overrides")),
                    "chip_plays": serialize(event.get("chip_plays")),
                    "most_selected": event.get("most_selected"),
                    "most_transferred_in": event.get(
                        "most_transferred_in"
                    ),
                    "top_element": event.get("top_element"),
                    "top_element_info": serialize(
                        event.get("top_element_info")
                    ),
                    "transfers_made": event.get("transfers_made"),
                    "most_captained": event.get("most_captained"),
                    "most_vice_captained": event.get(
                        "most_vice_captained"
                    ),
                    "_ingested_at": ingested_at,
                    "_source_file": source_file,
                }
            )

    logger.info(
        "Bootstrap ingestion completed: %s players, %s teams, %s gameweeks",
        len(players),
        len(teams),
        len(events)
    )

    return len(players)