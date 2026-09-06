from .cli_parser import parse_argument
from .config import get_configuration
from .validations import validate_path, validate_configuration
from .core import organize_folder
from .logger import configure_logging
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
config_path = Path(__file__).parent / "config.json"

def main() -> None:
    configure_logging()
    args = parse_argument()
    source = validate_path(args.folder_path)

    if source is None:
        raise FileNotFoundError("Folder has not been found.")
    dry_run = args.dry_run

    categories = get_configuration(config_path)
    if not validate_configuration(categories):
        logger.error("Configuration file has the wrong format.")
        raise ValueError("Invalid configuration.")
    else:
        logger.info("Configuration file is valid.")
        organize_folder(source, categories, dry_run)

if __name__ == "__main__":
    main()