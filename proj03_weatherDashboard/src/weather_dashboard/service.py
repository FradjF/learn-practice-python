import json
from pathlib import Path
from dataclasses import asdict
from weather_dashboard.models import Coordinates, CurrentWeather, Forecast, ForecastDay
from weather_dashboard.cache import WeatherCache
from weather_dashboard.providers.weather_api import WeatherApiClient


class WeatherService:

    def __init__(
            self,
            api_client:WeatherApiClient,
            cache:WeatherCache
    ):
        self.api_client = api_client
        self.cache =  cache

    def get_geocodes(self, location: str) -> Coordinates:
        key = f"geocode_{location.lower()}"
        cached = self.cache.get(key)

        if cached is not None:
            return Coordinates(**cached)

        coordinates = self.api_client.get_geocodes(location)
        self.cache.set(key, asdict(coordinates))

        return coordinates

    def get_current(self, coordinates: Coordinates) -> CurrentWeather:
        key = f"current_{coordinates.latitude}_{coordinates.longitude}"
        cached = self.cache.get(key)

        if cached is not None:
            return CurrentWeather(**cached)

        weather = self.api_client.get_current_weather(coordinates)
        self.cache.set(key, asdict(weather))
        return weather

    def get_forecast(self, coordinates: Coordinates) -> list[ForecastDay]:
        key = f"forecast_{coordinates.latitude}_{coordinates.longitude}"
        cached_forecast = self.cache.get(key)

        if cached_forecast is not None:
            return [
                ForecastDay(
                    date=day["date"],
                    forecast=[
                        Forecast(**forecast)
                        for forecast in day["forecast"]
                    ]
                )
                for day in cached_forecast
            ]

        forecast = self.api_client.get_forecast(coordinates)
        self.cache.set(
            key,
            [asdict(day) for day in forecast]
        )

        return forecast


def build_report(location:str, current:CurrentWeather, forecast:list[ForecastDay]|None) -> dict:
    export = None
    if current is not None:
        export = {
            "location": location,
            "current":asdict(current)
        }
        if forecast:
            weather_forecast = {"forecast": [asdict(day) for day in forecast]}
            export.update(weather_forecast)
    return export

def export_json(report:dict, json_path:Path) -> None:
    if report is not None:
        with open(f"{json_path}/export.json", "w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=2)




