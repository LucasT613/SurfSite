from datetime import datetime
import pytest

from Data.Parsing import parse_wind_dict, WindReading
import Data.Wind_API as Wind_API


@pytest.fixture(autouse=True)
def clear_wind_cache():
    Wind_API._cache.clear()


class FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data

def test_get_wind_data_returns_parsed_json(monkeypatch, fake_wind_api_response):
    def fake_get(url, params=None):
        return FakeResponse(fake_wind_api_response)

    monkeypatch.setattr(Wind_API.requests, "get", fake_get)
    result = Wind_API.get_wind_data(33.66, -117.99)
    assert result == fake_wind_api_response


def test_get_wind_data_calls_correct_url_and_params(monkeypatch, fake_wind_api_response):
    captured = {}

    def fake_get(url, params=None):
        captured["url"] = url
        captured["params"] = params
        return FakeResponse(fake_wind_api_response)

    monkeypatch.setattr(Wind_API.requests, "get", fake_get)
    Wind_API.get_wind_data(33.66, -117.99)

    assert captured["url"] == "https://api.open-meteo.com/v1/forecast"
    assert captured["params"]["latitude"] == 33.66
    assert captured["params"]["longitude"] == -117.99
    assert "wind_speed_10m" in captured["params"]["hourly"]
    assert "wind_direction_10m" in captured["params"]["hourly"]


def test_get_wind_data_caches_within_window(monkeypatch, fake_wind_api_response):
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_wind_api_response)

    monkeypatch.setattr(Wind_API.requests, "get", fake_get)
    monkeypatch.setattr(Wind_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    Wind_API.get_wind_data(33.66, -117.99)
    Wind_API.get_wind_data(33.66, -117.99)

    assert call_count["count"] == 1