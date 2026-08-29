import argparse
from pathlib import Path
from organizer import organize_folder


def validate_path(parsed_path: Path) -> Path | None:
    if Path(parsed_path).exists() and Path(parsed_path).is_dir():
        full_path = Path(parsed_path).expanduser()
        print(f"Folder exists.\nFull path is: {full_path}")
    else:
        full_path = None
    return full_path

def parse_argument() -> argparse.Namespace:
    """
        This function parses an entered argument.
    """
    parser = argparse.ArgumentParser(description="This is a parser to process entered path.")
    parser.add_argument("folder_path", type=str, help="Folder to be organized")
    parser.add_argument("--dry-run", action="store_true", help="Preview moves without executing them")
    args = parser.parse_args()

    return args

def main() -> None:
    args = parse_argument()
    source = validate_path(args.folder_path)
    if source is None:
        raise FileNotFoundError("File has not been found.")

    dry_run = args.dry_run
    organize_folder(source,dry_run)

if __name__ == "__main__":
    main()