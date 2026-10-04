from dataclasses import asdict
from unittest.mock import Mock
from weather_dashboard.models import Coordinates, CurrentWeather, ForecastDay, Forecast
from weather_dashboard.service import WeatherService

def test_service_get_current_cache_miss():
    fake_cache = Mock()
    fake_cache.get.return_value = None

    weather = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_api_client = Mock()
    fake_api_client.get_current_weather.return_value = weather

    coordinates = Coordinates(latitude=12.344553,longitude=29.9089837)

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )

    result = service.get_current(coordinates)

    assert result == weather
    fake_api_client.get_current_weather.assert_called_once_with(coordinates)
    fake_cache.get.assert_called_once()
    fake_cache.set.assert_called_once_with(
        "current_12.344553_29.9089837",
        {
            "description": "sunny",
            "temperature": 29,
            "feels_like": 30,
        },
    )

def test_service_get_current_cache_hit():
    weather = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_cache = Mock()
    fake_cache.get.return_value = asdict(weather)

    fake_api_client = Mock()
    fake_api_client.get_current_weather.return_value = weather

    coordinates = Coordinates(latitude=12.344553, longitude=29.9089837)

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )

    result = service.get_current(coordinates)

    assert result == weather
    fake_api_client.get_current_weather_assert_not_called()
    fake_cache.get.assert_called_once_with("current_12.344553_29.9089837")
    fake_cache.set.assert_not_called()

def test_service_get_forecast_cache_miss():
    fake_cache = Mock()
    fake_cache.get.return_value = None

    fake_response = [
        ForecastDay(
            date='2026-10-04',
            forecast=[Forecast(hour=23, description='ciel dégagé', temperature=25.0)]),
        ForecastDay(
            date='2026-10-05',
            forecast=[Forecast(hour=2, description='ciel dégagé', temperature=25.0),
                      Forecast(hour = 5, description = 'ciel dégagé', temperature = 23.0),
            ],
        )
    ]

    fake_api_client = Mock()
    fake_api_client.get_forecast.return_value = fake_response

    coordinates = Coordinates(latitude=12.344553,longitude=29.9089837)

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )

    result = service.get_forecast(coordinates)

    assert result == fake_response
    fake_api_client.get_forecast.assert_called_once_with(coordinates)
    fake_cache.get.assert_called_once_with("forecast_12.344553_29.9089837")
    fake_cache.set.assert_called_once_with(
        "forecast_12.344553_29.9089837",
            [
                {
                    "date": '2026-10-04',
                    "forecast": [
                        {
                            "hour": 23,
                            "description": "ciel dégagé",
                            "temperature": 25.0,
                        },
                    ],
                },
                {
                    "date": '2026-10-05',
                    "forecast": [
                        {
                             "hour":2,
                             "description": "ciel dégagé",
                             "temperature": 25.0,
                        },
                        {
                            "hour": 5,
                            "description": "ciel dégagé",
                            "temperature": 23.0,
                        },
                    ],
                },
            ]
    )

def test_service_get_forecast_cache_hit():
    cached_data = [
        {
            "date": '2026-10-04',
            "forecast": [
                {
                    "hour": 23,
                    "description": "ciel dégagé",
                    "temperature": 25.0,
                },
            ],
        },
        {
            "date": '2026-10-05',
            "forecast": [
                {
                     "hour":2,
                     "description": "ciel dégagé",
                     "temperature": 25.0,
                },
                {
                    "hour": 5,
                    "description": "ciel dégagé",
                    "temperature": 23.0,
                },
            ],
        },
    ]

    fake_cache = Mock()
    fake_cache.get.return_value = cached_data

    fake_response = [
        ForecastDay(
            date='2026-10-04',
            forecast=[Forecast(hour=23, description='ciel dégagé', temperature=25.0)]),
        ForecastDay(
            date='2026-10-05',
            forecast=[Forecast(hour=2, description='ciel dégagé', temperature=25.0),
                      Forecast(hour = 5, description = 'ciel dégagé', temperature = 23.0),
            ],
        )
    ]

    fake_api_client = Mock()
    fake_api_client.get_forecast.return_value = fake_response

    coordinates = Coordinates(latitude=12.344553,longitude=29.9089837)

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )

    result = service.get_forecast(coordinates)

    assert result == fake_response
    fake_api_client.get_forecast.assert_not_called()
    fake_cache.get.assert_called_once_with("forecast_12.344553_29.9089837")
    fake_cache.set.assert_not_called()

def test_service_get_geocodes_cache_miss():
    fake_cache = Mock()
    fake_cache.get.return_value = None

    coordinates = Coordinates(
        latitude=36.8002068,
        longitude=10.1857757,
    )

    fake_api_client = Mock()
    fake_api_client.get_geocodes.return_value = coordinates

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )
    location = "tunis"
    result = service.get_geocodes(location)

    assert result == coordinates
    fake_api_client.get_geocodes.assert_called_once_with(location)
    fake_cache.get.assert_called_once_with("geocode_tunis")
    fake_cache.set.assert_called_once_with(
        "geocode_tunis",
        {
            "latitude": 36.8002068,
            "longitude": 10.1857757,
        },
    )

def test_service_get_geocodes_cache_hit():
    fake_cache = Mock()
    fake_cache.get.return_value = {
            "latitude": 36.8002068,
            "longitude": 10.1857757,
        }

    coordinates = Coordinates(
        latitude=36.8002068,
        longitude=10.1857757,
    )

    fake_api_client = Mock()
    fake_api_client.get_geocodes.return_value = coordinates

    service = WeatherService(
        api_client=fake_api_client,
        cache=fake_cache,
    )
    location = "tunis"
    result = service.get_geocodes(location)

    assert result == coordinates
    fake_api_client.get_geocodes.assert_not_called()
    fake_cache.get.assert_called_once_with("geocode_tunis")
    fake_cache.set.assert_not_called()