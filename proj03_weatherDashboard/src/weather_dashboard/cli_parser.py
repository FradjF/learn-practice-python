import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="This is a parser to process"
                                                 "an entered location.")
    parser.add_argument("location", type=str, help="Name of the city for which to retrieve the weather.")
    parser.add_argument("--forecast", action="store_true", help="Gets weather forecast for the next 5 days.")
    parser.add_argument("--json", action="store_true", help="Export the result into a .json file.")

    args = parser.parse_args()

    return args