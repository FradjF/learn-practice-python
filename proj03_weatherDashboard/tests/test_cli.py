from unittest.mock import Mock
from weather_dashboard.cli import run
from weather_dashboard.models import Coordinates, CurrentWeather, Forecast, ForecastDay

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

    run("tunis", fake_service, False, False)
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

    run("tunis", fake_service, True, False)
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

