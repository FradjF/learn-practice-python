import argparse
from pathlib import Path
from organizer.core import organize_folder
from logger import configure_logging
from config import get_configuration, validate_configuration
import logging

logger = logging.getLogger(__name__)

def validate_path(parsed_path: Path) -> Path | None:
    """
        Validates the parsed path: Makes sure the path/folder exists.

    """
    full_path = Path(parsed_path).expanduser()
    if full_path.exists() and full_path.is_dir():
        print(f"Folder exists.\nFull path is: {full_path}")
    else:
        full_path = None
    return full_path

def parse_argument() -> argparse.Namespace:
    """
        This function defines arguments for the CLI and
        parses the entered argument(s).
    """
    parser = argparse.ArgumentParser(description="This is a parser to process entered path.")
    parser.add_argument("folder_path", type=str, help="Folder to be organized")
    parser.add_argument("--dry-run", action="store_true", help="Preview moves without executing them")
    args = parser.parse_args()

    return args

def main() -> None:
    configure_logging()
    args = parse_argument()
    source = validate_path(args.folder_path)

    if source is None:
        raise FileNotFoundError("Folder has not been found.")
    dry_run = args.dry_run

    categories = get_configuration()
    if not validate_configuration(categories):
        logger.error("Configuration file has the wrong format.")
        raise ValueError("Invalid configuration.")
    else:
        logger.info("Configuration file is valid.")
        organize_folder(source, categories, dry_run)

if __name__ == "__main__":
    main()