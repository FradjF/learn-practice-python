import json
import time
from typing import Any
from pathlib import Path

class WeatherCache:
    def __init__(self, cache_dir: Path, ttl: int):
        self.cache_dir = cache_dir / "weather"
        self.ttl = ttl

        self.cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def get(self, key: str):
        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        with cache_file.open("r") as file:
            data = json.load(file)

        age = time.time() - data["created_at"]

        if age >= self.ttl:
            cache_file.unlink()
            return None

        return data["value"]

    def set(self, key: str, value: Any):
        cache_file = self.cache_dir / f"{key}.json"
        data = {
            "created_at": time.time(),
            "value": value,
        }
        with cache_file.open("w") as file:
            json.dump(data, file)

