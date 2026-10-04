import json
from pathlib import Path
from weather_dashboard.config import load_config
from weather_dashboard.providers.weather_api import WeatherApiClient
from weather_dashboard.cache import WeatherCache


def main():
    config = load_config()
    client = WeatherApiClient(config)

    location = input("Provide a location: ")

    coordinates = client.get_geocodes(location)
    print(coordinates)
    weather = client.get_current_weather(coordinates)
    print(weather)

    cache = WeatherCache(Path("cache"), 300)
    cache.set("test", 29)
    forecast = client.get_forecast(coordinates)
    for day in forecast:
        print(day)
        print()

if __name__ == "__main__":
    main()