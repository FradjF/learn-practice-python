import argparse

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