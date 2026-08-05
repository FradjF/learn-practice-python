import argparse
from pathlib import Path
from organizer import move_file


def validate_path(parsed_path) -> Path:
    if Path(parsed_path).exists() and Path(parsed_path).is_dir():
        full_path = Path(parsed_path).expanduser()
        print(f"Folder exists.\nFull path is: {full_path}")
    else:
        full_path = None
        print("Folder could not be found.")
    return full_path

def parse_argument() -> Path:
    """
        This function parses an entered argument.
    """
    parser = argparse.ArgumentParser(description="This is a parser to process entered path.")
    parser.add_argument("folder_path", type=str, help="Folder to be organized")
    args = parser.parse_args()

    return args.folder_path

def main() -> None:
    arg = parse_argument()
    if validate_path(arg) is None:
        raise FileNotFoundError("File has not been found.")
    else:
        source = validate_path(arg)
        print("Scanning folder ...\n")
        move_file(source)

if __name__ == "__main__":
    main()