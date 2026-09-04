import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DEFAULT_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}

def get_configuration() -> dict:

    try:
        config_path = Path(__file__).parent / "config.json"
        with config_path.open("r", encoding="utf-8") as file:
            categories = json.load(file)
            logger.info("Categories loaded successfully from 'config.json'.")
            return categories
    except FileNotFoundError:
        logger.warning("'config.json' not found. Using default configuration.")
        return DEFAULT_CATEGORIES