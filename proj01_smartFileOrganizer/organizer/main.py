import argparse
from pathlib import Path
from organizer import move_file

def parse_input() -> Path:
    parser = argparse.ArgumentParser(description="This is a parser to process entered path.")
    parser.add_argument("folder_path", type=str, help="Folder to be organized")
    args = parser.parse_args()

    if Path(args.folder_path).exists():
        full_path = Path(args.folder_path).expanduser()
        print(f"Folder exists.\nFull path is: {full_path}")
    else:
        full_path = None
        print("Folder could not be found.")
    return full_path

source = parse_input()
print("Scanning folder ...\n")
move_file(source)