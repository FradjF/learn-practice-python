import os
from dotenv import load_dotenv
from dataclasses import dataclass

class ConfigurationError(RuntimeError):
    pass

@dataclass
class Config:
    api_key: str
    api_geo_base_url: str
    api_base_url: str
    cache_ttl: int

def get_required_env(var_name):
    try:
        env_var = os.environ[var_name]
        return env_var
    except KeyError as exc:
        raise ConfigurationError(f"Environment variable {var_name} not found.") from exc

def load_config():
    load_dotenv()
    try:
        cache_ttl = int(get_required_env("CACHE_TTL"))
    except ValueError as exc:
        raise ConfigurationError("CACHE_TTL must be an integer.") from exc

    return Config(
        api_key=get_required_env("WEATHER_API_KEY"),
        api_geo_base_url=get_required_env("WEATHER_API_GEO_BASE_URL"),
        api_base_url=get_required_env("WEATHER_API_BASE_URL"),
        cache_ttl=cache_ttl,
    )


