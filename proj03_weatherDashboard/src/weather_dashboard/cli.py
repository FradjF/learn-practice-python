import json
from pathlib import Path
from weather_dashboard.config import load_config
from weather_dashboard.providers.weather_api import WeatherApiClient
from weather_dashboard.service import WeatherService
from weather_dashboard.cache import WeatherCache


def main():
    config = load_config()

    api_client = WeatherApiClient(config)
    cache = WeatherCache(Path("cache"),config.cache_ttl)
    service = WeatherService(api_client, cache)

    location = "tunis" #input("Provide a location: ")
    coordinates = service.get_geocodes(location)
    print(coordinates)
    weather = service.get_forecast(coordinates)
    print(weather)



if __name__ == "__main__":
    main()