import json
from weather_dashboard.config import load_config
from weather_dashboard.providers.weather_api import WeatherApiClient


def main():
    config = load_config()
    client = WeatherApiClient(config)

    location = input("Provide a location: ")

    coordinates = client.get_geocodes(location)
    print(coordinates)
    weather = client.get_current_weather(coordinates)
    print(weather)
    forecast = client.get_forecast(coordinates)
    for day in forecast:
        print(day)
        print()

if __name__ == "__main__":
    main()