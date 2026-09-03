import logging

from ingestion.ingest_bootstrap import load_bootstrap, save_bootstrap
from ingestion.ingest_fixtures import load_fixtures, save_fixtures


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Starting FPL Edge ingestion pipeline")

    # Bootstrap
    bootstrap_data = load_bootstrap()
    save_bootstrap(
        bootstrap_data,
        "api://bootstrap-static/"
    )

    # Fixtures
    fixtures = load_fixtures()
    save_fixtures(
        fixtures,
        "api://fixtures/"
    )

    logger.info("FPL Edge ingestion pipeline completed successfully")


if __name__ == "__main__":
    main()