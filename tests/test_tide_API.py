from datetime import datetime
import pytest

import Data.Tide_API as Tide_API


@pytest.fixture(autouse=True)
def clear_tide_cache():
    Tide_API._cache.clear()


class FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


def test_get_tide_data_returns_parsed_json(monkeypatch, fake_tide_api_response):
    def fake_get(url, params=None):
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)
    result = Tide_API.get_tide_data("9410660")
    assert result == fake_tide_api_response


def test_get_tide_data_calls_correct_url_and_params(monkeypatch, fake_tide_api_response):
    captured = {}

    def fake_get(url, params=None):
        captured["url"] = url
        captured["params"] = params
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)
    Tide_API.get_tide_data("9410660")

    assert captured["url"] == "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    assert captured["params"]["station"] == "9410660"
    assert captured["params"]["product"] == "predictions"
    assert captured["params"]["interval"] == "6"
    assert captured["params"]["datum"] == "MLLW"


def test_get_tide_data_caches_within_window(monkeypatch, fake_tide_api_response):
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)
    monkeypatch.setattr(Tide_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    Tide_API.get_tide_data("9410660")
    Tide_API.get_tide_data("9410660")  # should hit cache

    assert call_count["count"] == 1


def test_get_tide_data_refetches_after_12_hours(monkeypatch, fake_tide_api_response):
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)

    times = iter([
        datetime(2026, 9, 13, 0, 0),
        datetime(2026, 9, 13, 12, 1),  # just past the 12hr window
    ])
    monkeypatch.setattr(Tide_API, "_utcnow_naive", lambda: next(times))

    Tide_API.get_tide_data("9410660")
    Tide_API.get_tide_data("9410660")

    assert call_count["count"] == 2


def test_get_tide_data_still_cached_at_11_hours(monkeypatch, fake_tide_api_response):
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)

    times = iter([
        datetime(2026, 9, 13, 0, 0),
        datetime(2026, 9, 13, 11, 0),  # still within the 12hr window
    ])
    monkeypatch.setattr(Tide_API, "_utcnow_naive", lambda: next(times))

    Tide_API.get_tide_data("9410660")
    Tide_API.get_tide_data("9410660")

    assert call_count["count"] == 1


def test_different_stations_are_cached_separately(monkeypatch, fake_tide_api_response):
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_tide_api_response)

    monkeypatch.setattr(Tide_API.requests, "get", fake_get)
    monkeypatch.setattr(Tide_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    Tide_API.get_tide_data("9410660")
    Tide_API.get_tide_data("9410230")  # different station -- must refetch

    assert call_count["count"] == 2