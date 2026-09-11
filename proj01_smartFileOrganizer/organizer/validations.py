from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def validate_path(parsed_path: Path) -> Path:
    """Validate that the path exists and is a directory."""

    full_path = Path(parsed_path).expanduser()
    if full_path.exists() and full_path.is_dir():
        logger.info("Folder exists: %s", full_path)
        return full_path

    logger.error("Folder has not been found.")
    raise FileNotFoundError("Folder has not been found: %s", full_path)


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