import time

import requests


class FPLClient:
    BASE_URL = "https://fantasy.premierleague.com/api/"

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "FPL-Edge/1.0"
        })

    def get(self, endpoint, retries=3, backoff_factor=2):
        url = f"{self.BASE_URL}{endpoint}"

        for attempt in range(retries):
            try:
                response = self.session.get(
                    url,
                    timeout=30
                )

                response.raise_for_status()

                return response.json()

            except requests.RequestException:
                if attempt == retries - 1:
                    raise

                sleep_time = backoff_factor ** attempt

                print(
                    f"Request failed. "
                    f"Retrying in {sleep_time} seconds..."
                )

                time.sleep(sleep_time)