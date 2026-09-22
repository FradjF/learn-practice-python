import logging

from aiohttp.hdrs import PRAGMA

from expense_tracker.database import initialize_database
from expense_tracker.cli import menu
from expense_tracker.logging_config import configure_logging


logger = logging.getLogger(__name__)

def main():
    configure_logging()
    initialize_database()
    logger.info("DB initialized successfully.")

    #menu()


if __name__ == "__main__":
    main()