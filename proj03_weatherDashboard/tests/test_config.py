import pytest
from dotenv import load_dotenv
from weather_dashboard.config import load_config, ConfigurationError


def test_valid_config(monkeypatch):
    monkeypatch.setenv("WEATHER_API_KEY", "TEST_ABI38UOIK29")
    monkeypatch.setenv("WEATHER_API_GEO_BASE_URL", "http://test1")
    monkeypatch.setenv("WEATHER_API_BASE_URL", "http://test2")
    monkeypatch.setenv("CACHE_TTL","500")

    config = load_config()

    assert config.api_key == "TEST_ABI38UOIK29"
    assert config.api_geo_base_url == "http://test1"
    assert config.api_base_url == "http://test2"
    assert config.cache_ttl == 500

def test_missing_key(monkeypatch):
    monkeypatch.setattr("weather_dashboard.config.load_dotenv", lambda: None)

    monkeypatch.delenv("WEATHER_API_KEY", False)
    monkeypatch.setenv("WEATHER_API_GEO_BASE_URL", "http://test1")
    monkeypatch.setenv("WEATHER_API_BASE_URL", "http://test2")
    monkeypatch.setenv("CACHE_TTL","500")

    with pytest.raises(ConfigurationError, match="WEATHER_API_KEY"):
        load_config()

def test_base_url(monkeypatch):
    monkeypatch.setattr("weather_dashboard.config.load_dotenv", lambda: None)

    monkeypatch.setenv("WEATHER_API_KEY", "TEST_ABI38UOIK29")
    monkeypatch.setenv("WEATHER_API_GEO_BASE_URL", "http://test1")
    monkeypatch.delenv("WEATHER_API_BASE_URL", False)
    monkeypatch.setenv("CACHE_TTL","500")

    with pytest.raises(ConfigurationError, match="WEATHER_API_BASE_URL"):
        load_config()

def test_invalid_cache_ttl(monkeypatch):

    monkeypatch.setenv("WEATHER_API_KEY", "TEST_ABI38UOIK29")
    monkeypatch.setenv("WEATHER_API_GEO_BASE_URL", "http://test1")
    monkeypatch.setenv("WEATHER_API_BASE_URL", "http://test2")
    monkeypatch.setenv("CACHE_TTL","ABC")

    with pytest.raises(ConfigurationError, match="CACHE_TTL"):
        load_config()