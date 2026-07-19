import argparse
from pathlib import Path


parser = argparse.ArgumentParser(description="This is a parser to process entered path")
parser.add_argument("folder_path", type=str, help="Folder to be organized")
args = parser.parse_args()

#print(Path(args.folder_path).exists)
for item in Path(args.folder_path).iterdir():
    print(item.name)
