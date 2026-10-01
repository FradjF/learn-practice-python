from dataclasses import dataclass

@dataclass
class Coordinates:
    latitude: float
    longitude: float

@dataclass
class CurrentWeather:
    description: str
    temperature: float
    feels_like: float

@dataclass
class Forecast:
    hour: int
    description: str
    temperature: float

@dataclass
class ForecastDay:
    timestamp: str
    forecast: list[Forecast]