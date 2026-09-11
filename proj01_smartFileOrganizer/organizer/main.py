from .cli_parser import parse_arguments
from .config import get_configuration, DEFAULT_CATEGORIES
from .validations import validate_path, validate_configuration
from .core import organize_folder
from .logger import configure_logging
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def main() -> int:
    configure_logging()
    #Parse arguments
    args = parse_arguments()

    #Validate folder
    try:
        source = validate_path(args.folder_path)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 1

    #Load configuration
    config = args.config
    if config is not None:
        try:
            categories = get_configuration(Path(config))
        except FileNotFoundError as exc:
            print(f"Error: {exc}")
            return 1
        except ValueError as exc:
            print(f"Error: {exc}")
            return 1
    else:
        categories = DEFAULT_CATEGORIES

    #Validate configuration
    if validate_configuration(categories):
        logger.info("Configuration file is valid.")
        organize_folder(source, categories, args.dry_run)
        return 0
    else:
        logger.error("Configuration file has the wrong format.")
        print("Error: Config file has the wrong format.")
        return 1

if __name__ == "__main__":
    main()