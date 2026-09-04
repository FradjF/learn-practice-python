import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

DEFAULT_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"]
}

def get_configuration() -> dict:

    try:
        config_path = Path(__file__).parent / "config.json"
        with config_path.open("r", encoding="utf-8") as file:
            categories = json.load(file)
            #print("Categ Success")
            logger.info("Categories loaded successfully from 'config.json'.")
            return categories
    except FileNotFoundError as e:
        #print(e)
        logger.error("'config.json' not found")
        return DEFAULT_CATEGORIES