from pathlib import Path

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