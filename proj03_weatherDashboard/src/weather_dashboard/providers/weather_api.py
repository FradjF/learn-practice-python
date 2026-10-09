import requests
from datetime import datetime
from weather_dashboard.config import Config
from weather_dashboard.models import Coordinates, CurrentWeather, ForecastDay, Forecast


class WeatherApiError(RuntimeError):
    pass

class BadRequestError(WeatherApiError):
    pass

class AuthenticationError(WeatherApiError):
    pass

class NotFoundError(WeatherApiError):
    pass

class RateLimitError(WeatherApiError):
    pass

class ServerError(WeatherApiError):
    pass

class NetworkError(WeatherApiError):
    pass

class WeatherApiClient:
    def __init__(self, config: Config):
        self.api_key = config.api_key
        self.api_base_url = config.api_base_url
        self.api_geo_base_url = config.api_geo_base_url

    def _handle_response(self, response):
        status_code = response.status_code
        if 200 <= status_code < 300:
            return
        if status_code == 400:
            raise BadRequestError("Request parameters missing or incorrect.")
        if status_code == 401:
            raise AuthenticationError("Invalid API key.")
        if status_code == 404:
            raise NotFoundError("Requested data not found.")
        if status_code == 429:
            raise RateLimitError("Request quota for the API key has been exceeded.")
        if 500 <= status_code < 600:
            raise ServerError("API server error.")

        raise WeatherApiError("OpenWeather error.")

    def _get(self, url:str, params:dict):
        try:
            return requests.get(
                url=url,
                params=params,
                timeout=10,
            )
        except requests.exceptions.RequestException as exc:
            raise NetworkError("Internet connection issue.") from exc

    def get_geocodes(self, location: str) -> Coordinates:
        response = self._get(
            url = f"{self.api_geo_base_url}/geo/1.0/direct",
            params = {
                    "q": location,
                    "appid": self.api_key,
                },
            )

        self._handle_response(response)

        data = response.json()
        if not data:
            raise NotFoundError(
                f"The provided location has not been found: {location}"
            )

        data = data[0]

        return Coordinates(
            latitude = data["lat"],
            longitude = data["lon"],
        )

    def get_current_weather(self, coordinates: Coordinates) -> CurrentWeather:
        response = self._get(
            url = f"{self.api_base_url}/data/2.5/weather",
            params = {
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "appid": self.api_key,
                "units": "metric",
                "lang": "FR",
            },
        )

        self._handle_response(response)

        data = response.json()

        return CurrentWeather(
            description = data["weather"][0]["description"],
            temperature = round(data["main"]["temp"], 0),
            feels_like = round(data["main"]["feels_like"], 0),
        )

    def get_forecast(self, coordinates: Coordinates) -> list[ForecastDay]:

        response = self._get(
            url = f"{self.api_base_url}/data/2.5/forecast",
            params = {
                "lat": coordinates.latitude,
                "lon": coordinates.longitude,
                "appid": self.api_key,
                "units": "metric",
                "lang": "FR",
            },
        )

        self._handle_response(response)

        data = response.json()["list"]

        days = []
        day = []
        previous_date = None
        for item in data:
            date = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            three_hour_forecast = Forecast(
                    hour=int(datetime.fromtimestamp(item["dt"]).strftime("%H")),
                    description=item["weather"][0]["description"],
                    temperature=round(item["main"]["temp"], 0)
                )

            if previous_date is None:
                previous_date = date

            if date != previous_date:
                days.append(
                    ForecastDay(
                        date=previous_date,
                        forecast=day,
                    ),
                )
                previous_date = date
                day = []

            day.append(three_hour_forecast)

        if day:
            days.append(
                ForecastDay(
                    date=previous_date,
                    forecast=day,
                ),
            )

        return days
