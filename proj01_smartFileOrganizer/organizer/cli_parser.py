import argparse

def parse_arguments() -> argparse.Namespace:
    """Define and parse command-line arguments."""

    parser = argparse.ArgumentParser(description="This is a parser to process entered path.")
    parser.add_argument("folder_path", type=str, help="Path to the folder to be organized.")
    parser.add_argument("--dry-run", action="store_true", help="Preview moves without executing them.")
    parser.add_argument("--config", type=str, default=None, help="Path to a JSON configuration file.")
    args = parser.parse_args()

    return args