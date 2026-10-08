from pathlib import Path
from weather_dashboard.config import load_config
from weather_dashboard.providers.weather_api import WeatherApiClient
from weather_dashboard.service import WeatherService, build_report, export_json
from weather_dashboard.cache import WeatherCache
from weather_dashboard.cli_parser import parse_arguments

def run(location:str, service: WeatherService, show_forecast:bool, json_option:bool):

    coordinates = service.get_geocodes(location)
    current = service.get_current(coordinates)
    print(f"Weather: {location.capitalize()}\n")
    print("Current weather")
    print("---------------")
    print(f"Temperature: {current.temperature}°C\n"
          f"Feels like: {current.feels_like}°C\n"
          f"Conditions: {current.description}\n")

    forecast = None
    if show_forecast:
        forecast = service.get_forecast(coordinates)
        print("Forecast")
        print("--------")
        for day in forecast:
            print(day.date)
            for item in day.forecast:
                print(f"{item.hour:02d}:00 {item.description} {item.temperature}°C")
            print()

    if json_option:
        report = build_report(location, current, forecast)
        export_json(report, Path("."))

def main():
    args = parse_arguments()

    config = load_config()
    api_client = WeatherApiClient(config)
    cache = WeatherCache(Path(".cache"),config.cache_ttl)
    service = WeatherService(
        api_client=api_client,
        cache=cache)

    run(
        location=args.location,
        service=service,
        show_forecast=args.forecast,
        json_option=args.json,
    )



if __name__ == "__main__":
    main()