import pytest
from datetime import datetime
from unittest.mock import Mock
from weather_dashboard.models import Coordinates
from weather_dashboard.config import Config
from weather_dashboard.providers import weather_api
from weather_dashboard.providers.weather_api import WeatherApiClient, BadRequestError, AuthenticationError


def test_geocodes_success(monkeypatch):
    """
    1. What is the behaviour?
        Give a location, return its coordinates.
    2. What are the dependencies:
        requests.get
    3. What should the dependency do in this scenario?
        Scenario: request successful, status_code=200
                ↓
        Coordinates("lat":lat, "lon":lon)
    4. What should my function do?
        requests.get(
            url = "http://test",
            params = {
                "q":"location",
                "appid":api_key
            }
        )
    5. What do I need to assert?
        coordinates == Coordinates("lat":lat, "lon":lon)
    """

    class FakeResponse:
        status_code = 200
        def json(self):
            return [
                {
                    "lat": 12.13445,
                    "lon": 29.29034,
                },
            ]

    def mock_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("weather_dashboard.providers.weather_api.requests.get",
                        mock_get)

    config = Config(
        api_key="test-key",
        api_base_url="https://api.test1",
        api_geo_base_url="https://api.test",
        cache_ttl=300)
    client = WeatherApiClient(config)
    response = client.get_geocodes("Paris")

    assert response.latitude == 12.13445
    assert response.longitude == 29.29034

def test_geocodes_bad_request(monkeypatch):

    class FakeResponse:
        status_code = 400

    def mock_get(*args, **kwargs):
        assert kwargs["url"] == "https://api.test/geo/1.0/direct"
        assert kwargs["params"]["q"] == "Paris"
        assert kwargs["params"]["appid"] == "test-key"
        assert kwargs["timeout"] == 10

        return FakeResponse()

    monkeypatch.setattr("weather_dashboard.providers.weather_api.requests.get",
                        mock_get)

    config = Config(
        api_key="test-key",
        api_base_url="https://api.test1",
        api_geo_base_url="https://api.test",
        cache_ttl=300)
    client = WeatherApiClient(config)

    with pytest.raises(BadRequestError, match="missing or incorrect"):
        client.get_geocodes("Paris")

def test_get_current_success(monkeypatch):

    #Arrange
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
            "main": {
                "temp":24,
                "feels_like": 26,
            },
            "weather": [
                {"description": "cloudy",}
            ],
    }

    fake_get = Mock(return_value=fake_response)

    monkeypatch.setattr("weather_dashboard.providers.weather_api.requests.get",
                        fake_get)

    config = Config(
        api_key="test-key",
        api_base_url="https://api.test1",
        api_geo_base_url="https://api.test",
        cache_ttl=300)

    client = WeatherApiClient(config)


    #Act

    response = client.get_current_weather(Coordinates(12.13445, 29.29034))

    #Assert
    assert response.description == "cloudy"
    assert response.temperature == 24
    assert response.feels_like == 26

    fake_get.assert_called_once_with(
        url="https://api.test1/data/2.5/weather",
        params={
            "lat": 12.13445,
            "lon": 29.29034,
            "appid": "test-key",
            "units": "metric",
            "lang": "FR"
        },
        timeout=10,
    )

def test_get_current_auth_error(monkeypatch):
    #Arrange
    fake_response = Mock()
    fake_response.status_code = 401

    fake_get = Mock(return_value=fake_response)

    monkeypatch.setattr(
        weather_api.requests,
        "get",
        fake_get,
    )

    #Act
    config = Config(
        api_key="test-key",
        api_base_url="https://api.test1",
        api_geo_base_url="https://api.test",
        cache_ttl=300

    )
    client = WeatherApiClient(config)
    coordinates = Coordinates(12.78683, 28.90809)

    #Assert
    with pytest.raises(AuthenticationError):
        client.get_current_weather(coordinates)

def test_get_forecast_success(monkeypatch):
    #Arrange
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value ={
        "list": [
            {
                "dt": int(datetime(2026, 9, 28, 9).timestamp()),
                "main": {
                    "temp": 18,
                },
                "weather": [
                    {
                        "description": "cloudy",
                    },
                ],
            },
            {
                "dt": int(datetime(2026, 9, 28, 12).timestamp()),
                "main": {
                    "temp": 20,
                },
                "weather": [
                    {
                        "description": "sunny",
                    },
                ],
            },
            {
                "dt": int(datetime(2026, 9, 29, 9).timestamp()),
                "main": {
                    "temp": 16,
                },
                "weather": [
                    {
                        "description": "rain",
                    },
                ],
            },
        ]
    }

    fake_get = Mock(return_value=fake_response)

    monkeypatch.setattr(weather_api.requests,
                        "get",
                        fake_get)

    #Act
    config = Config(
        api_key="test-key",
        api_base_url="https://api.test1",
        api_geo_base_url="https://api.test",
        cache_ttl=300
    )
    client = WeatherApiClient(config)
    data = client.get_forecast(Coordinates(
        latitude=12.7883,
        longitude=28.8734)
    )

    #Assert
    assert data[0].forecast[0].temperature == 18
    assert data[0].forecast[1].temperature == 20
    assert data[1].forecast[0].temperature == 16