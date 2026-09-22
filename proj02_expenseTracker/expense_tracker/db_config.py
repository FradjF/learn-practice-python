import os
from pathlib import Path

# Calling env variable from Windows
# import os
#
# try:
#     DATABASE_PATH = Path(os.environ["DATABASE_PATH"])
# except KeyError as exc:
#     raise RuntimeError("DATABASE_PATH is not configured.") from exc

# Calling env variable from .env file

from dotenv import load_dotenv

load_dotenv()

try:
    DATABASE_PATH = Path(os.environ["DATABASE_PATH"])
except KeyError as exc:
    raise RuntimeError("DATABASE_PATH is not configured.") from exc
