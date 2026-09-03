import logging

import requests
from tenacity import retry, stop_after_attempt, wait_exponential


logger = logging.getLogger(__name__)


class FPLClient:
    BASE_URL = "https://fantasy.premierleague.com/api/"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "FPL-Edge/1.0"
        })

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=8),
    )
    def get(self, endpoint):
        url = f"{self.BASE_URL}{endpoint}"

        logger.info("Requesting FPL API: %s", endpoint)

        try:
            response = self.session.get(
                url,
                timeout=30
            )

            response.raise_for_status()

            logger.info(
                "FPL API request successful: %s",
                endpoint
            )

            return response.json()

        except requests.RequestException as e:
            logger.error(
                "FPL API request failed: %s | Error: %s",
                endpoint,
                e
            )
            raise


def get_bootstrap():
    client = FPLClient()
    return client.get("bootstrap-static/")


def get_fixtures():
    client = FPLClient()
    return client.get("fixtures/")


def get_player_history(player_id):
    client = FPLClient()
    return client.get(f"element-summary/{player_id}/")