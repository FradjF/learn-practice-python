import json
import logging

logger = logging.getLogger(__name__)

DEFAULT_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}

def get_configuration(config_path) -> dict:

        try:
            with config_path.open("r", encoding="utf-8") as file:
                categories = json.load(file)
                logger.info(
                    "Categories loaded successfully from '%s'.",
                    config_path)
                return categories
        except FileNotFoundError:
            logger.error(
                "Config file not found: %s",
                config_path)
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except json.JSONDecodeError as exc:
            logger.error(
                "Config file contains invalid JSON: %s",
                config_path)
            raise ValueError(f"Invalid JSON in config file: {config_path}") from exc