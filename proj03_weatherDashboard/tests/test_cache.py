import json
import time

from weather_dashboard.cache import WeatherCache

def test_cache_miss(tmp_path):
    #Act
    cache = WeatherCache(tmp_path, ttl=300)

    #Assert
    assert cache.get("missing") is None

def test_cache_success_0(tmp_path):
    cache_dir = tmp_path/"weather/"
    cache_dir.mkdir()
    cache_file = cache_dir / "paris.json"
    cache_file.touch()

    data = {
        "created_at": time.time(),
        "value": {
            "temperature": 18,
            "description": "cloudy",
        },
    }

    with cache_file.open("w") as file:
        json.dump(data, file)

    cache = WeatherCache(tmp_path, ttl=300)
    assert cache.get("paris") == data["value"]

def test_cache_success(tmp_path):
    cache = WeatherCache(tmp_path, ttl=300)
    data = {
        "value": {
            "temperature": 18,
            "description": "cloudy",
        },
    }

    cache.set("paris", data)

    assert cache.get("paris") == data

def test_cache_expired(monkeypatch, tmp_path):
    current_time = 1_000_000
    monkeypatch.setattr("weather_dashboard.cache.time.time",
                        lambda: current_time)

    cache = WeatherCache(tmp_path, ttl=300)
    value = {
        "value": {
            "temperature": 18,
            "description": "cloudy",
        },
    }

    cache.set("paris", value)

    monkeypatch.setattr("weather_dashboard.cache.time.time",
                        lambda: current_time + 300)
    assert cache.get("paris") is None