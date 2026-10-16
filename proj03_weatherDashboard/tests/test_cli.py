from unittest.mock import Mock
from argparse import Namespace
import weather_dashboard.cli as cli
from weather_dashboard.config import Config
from weather_dashboard.config import ConfigurationError
from weather_dashboard.models import Coordinates, CurrentWeather, Forecast, ForecastDay
from weather_dashboard.providers.weather_api import NetworkError, NotFoundError, AuthenticationError
def test_cli_current_weather(capsys):
    fake_service = Mock()
    fake_service.get_geocodes.return_value = Coordinates(
        latitude=12.98930,
        longitude=23.989844,
    )
    fake_service.get_current.return_value = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_service.get_forecast.return_value = None

    cli.run("tunis", fake_service, False, False)
    captured = capsys.readouterr()
    expected_output = (
        "Weather: Tunis\n"
        "\n"
        "Current weather\n"
        "---------------\n"
        "Temperature: 29°C\n"
        "Feels like: 30°C\n"
        "Conditions: sunny\n"
        "\n"
    )
    fake_service.get_geocodes.assert_called_once_with("tunis")
    fake_service.get_current.assert_called_once_with(
        Coordinates(
            latitude=12.98930,
            longitude=23.989844,
        )
    )
    fake_service.get_forecast.assert_not_called()
    assert captured.out == expected_output

def test_cli_forecast_requested(capsys):
    fake_service = Mock()
    fake_service.get_geocodes.return_value = Coordinates(
        latitude=12.98930,
        longitude=23.989844,
    )
    fake_service.get_current.return_value = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_service.get_forecast.return_value = [
        ForecastDay(
            date='2026-10-04',
            forecast=[Forecast(hour=23, description='ciel dégagé', temperature=25.0)]
        ),
        ForecastDay(
            date='2026-10-05',
            forecast=[Forecast(hour=2, description='ciel dégagé', temperature=25.0),
                      Forecast(hour = 5, description = 'ciel dégagé', temperature = 23.0),
            ],
        )
    ]

    cli.run("tunis", fake_service, True, False)
    captured = capsys.readouterr()
    expected_output = (
        "Weather: Tunis\n"
        "\n"
        "Current weather\n"
        "---------------\n"
        "Temperature: 29°C\n"
        "Feels like: 30°C\n"
        "Conditions: sunny\n"
        "\n"
        "Forecast\n"
        "--------\n"
        "2026-10-04\n"
        "23:00 ciel dégagé 25.0°C\n"
        "\n"
        "2026-10-05\n"
        "02:00 ciel dégagé 25.0°C\n"
        "05:00 ciel dégagé 23.0°C\n"
        "\n"
    )
    fake_service.get_geocodes.assert_called_once_with("tunis")
    fake_service.get_current.assert_called_once_with(
        Coordinates(
            latitude=12.98930,
            longitude=23.989844,
        )
    )
    fake_service.get_forecast.assert_called_once()
    assert captured.out == expected_output

def test_main_config_error(capsys, monkeypatch):

    def fake_load_cfg():
        raise ConfigurationError("WEATHER_API_KEY not found.")


    monkeypatch.setattr(
        cli,
        "parse_arguments",
        lambda: Namespace(location="Paris", forecast=False, json=False),
    )

    monkeypatch.setattr(
        cli,
        "load_config",
        fake_load_cfg
    )

    result = cli.main()
    captured = capsys.readouterr()

    assert result == 1
    assert "Configuration error" in captured.out
    assert "WEATHER_API_KEY not found" in captured.out
    assert "Traceback" not in captured.err

def test_main_authentication_error(capsys, monkeypatch):
    #Arrange
    def fake_load_config():
        return Config(
            api_key="fake-api-key",
            api_geo_base_url="https://testgeobase.com",
            api_base_url="https://testbase.com",
            cache_ttl=300,
        )

    def fake_run(**kwargs):
        raise AuthenticationError("Invalid API key.")

    monkeypatch.setattr(
        cli,
        "parse_arguments",
        lambda: Namespace(location="Paris", forecast=False, json=False),
    )

    monkeypatch.setattr(cli,
                        "load_config",
                        fake_load_config)

    monkeypatch.setattr(cli,
                        "run",
                        fake_run)

    #Act
    result = cli.main()

    #Assert
    captured = capsys.readouterr()

    assert result == 1
    assert "Invalid API key" in captured.out

def test_main_not_found_error(capsys, monkeypatch):
    #Arrange
    def fake_load_config():
        return Config(
            api_key="fake-api-key",
            api_geo_base_url="https://testgeobase.com",
            api_base_url="https://testbase.com",
            cache_ttl=300,
        )

    def fake_run(**kwargs):
        raise NotFoundError("Resource not found.")

    monkeypatch.setattr(
        cli,
        "parse_arguments",
        lambda: Namespace(location="Paris", forecast=False, json=False),
    )

    monkeypatch.setattr(cli,
                        "load_config",
                        fake_load_config)

    monkeypatch.setattr(cli,
                        "run",
                        fake_run)

    #Act
    result = cli.main()
    captured = capsys.readouterr()

    #Assert
    assert result == 1
    assert "Resource not found" in captured.out

def test_main_network_error(capsys, monkeypatch):
    #Arrange
    def fake_load_config():
        return Config(
            api_key="fake-api-key",
            api_geo_base_url="https://testgeobase.com",
            api_base_url="https://testbase.com",
            cache_ttl=300,
        )

    def fake_run(**kwargs):
        raise NetworkError("Unable to connect to the weather service.")


    monkeypatch.setattr(
        cli,
        "parse_arguments",
        lambda: Namespace(location="Paris", forecast=False, json=False),
    )
    monkeypatch.setattr(cli,
                        "load_config",
                        fake_load_config)

    monkeypatch.setattr(cli,
                        "run",
                        fake_run)

    #Act
    result = cli.main()
    captured = capsys.readouterr()

    #Assert
    assert result == 1
    assert "Unable to connect" in captured.out
    assert "Traceback" not in captured.err