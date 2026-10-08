import json
from weather_dashboard.models import CurrentWeather, Forecast, ForecastDay
from weather_dashboard.service import build_report, export_json

def test_build_report_with_forecast():

    fake_current = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_forecast = [
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

    report = build_report("Tunis", fake_current, fake_forecast)

    assert report["location"] == "Tunis"
    assert report["current"] == {
        "description": "sunny",
        "temperature": 29,
        "feels_like": 30,
    }
    assert len(report["forecast"]) == 2

def test_build_report_without_forecast():

    fake_current = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )

    report = build_report("Tunis", fake_current, None)

    assert report["location"] == "Tunis"
    assert report["current"] == {
        "description": "sunny",
        "temperature": 29,
        "feels_like": 30,
    }
    assert "forecast" not in report

def test_build_report_export(tmp_path):

    fake_current = CurrentWeather(
        description="sunny",
        temperature=29,
        feels_like=30,
    )
    fake_forecast = [
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

    report = build_report("Tunis", fake_current, fake_forecast)
    export_json(report, tmp_path)

    with open(tmp_path/"export.json", "r") as file:
        content = json.load(file)

    assert content["location"] == "Tunis"
    assert content["current"] == {
        "description": "sunny",
        "temperature": 29,
        "feels_like": 30,
    }
    assert len(content["forecast"]) == 2

