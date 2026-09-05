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

def validate_configuration(config:dict[str, list[str]]) -> bool:
    """
        This function validates whether the config file has the right structure
        Returns true/false
    """
    if not isinstance(config, dict) or not config:
        return False

    for (key, value) in config.items():
        if not isinstance(value,list):
            return False
        else:
            for ext in value:
                if not isinstance(ext,str):
                    return False
    return True