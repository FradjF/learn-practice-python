from .cli_parser import parse_argument
from .config import get_configuration, DEFAULT_CATEGORIES
from .validations import validate_path, validate_configuration
from .core import organize_folder
from .logger import configure_logging
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
#config_path = Path(__file__).parent / "config.json"

def main() -> int:
    configure_logging()
    #Parse arguments
    args = parse_argument()

    #Validate folder
    source = validate_path(args.folder_path)
    if source is None:
        raise FileNotFoundError("Folder has not been found.")

    #Load configuration
    config = args.config
    if not config is None:
        try:
            categories = get_configuration(Path(config))
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return 1
        except ValueError as e:
            print(f"Error: {e}")
            return 1
    else:
        categories = DEFAULT_CATEGORIES

    #Validate configuration
    if validate_configuration(categories):
        logger.info("Configuration file is valid.")
        dry_run = args.dry_run
        organize_folder(source, categories, dry_run)
    else:
        logger.error("Configuration file has the wrong format.")
        print("Error: Config file has the wrong format.")
        return 1

if __name__ == "__main__":
    main()