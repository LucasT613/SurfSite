from datetime import datetime, timedelta
import Data.Wave_API as Wave_API


class FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


def test_second_call_within_window_uses_cache_not_network(monkeypatch, fake_api_response):
    Wave_API._cache.clear()
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(Wave_API.requests, "get", fake_get)
    monkeypatch.setattr(Wave_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    Wave_API.get_wave_data(33.66, -117.99)
    Wave_API.get_wave_data(33.66, -117.99)

    assert call_count["count"] == 1


def test_call_after_expiry_refetches(monkeypatch, fake_api_response):
    Wave_API._cache.clear()
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(Wave_API.requests, "get", fake_get)

    times = iter([
        datetime(2026, 9, 13, 12, 0),
        datetime(2026, 9, 13, 12, 45),
    ])
    monkeypatch.setattr(Wave_API, "_utcnow_naive", lambda: next(times))

    Wave_API.get_wave_data(33.66, -117.99)
    Wave_API.get_wave_data(33.66, -117.99)

    assert call_count["count"] == 2


def test_different_locations_are_cached_separately(monkeypatch, fake_api_response):
    Wave_API._cache.clear()
    call_count = {"count": 0}

    def fake_get(url, params=None):
        call_count["count"] += 1
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(Wave_API.requests, "get", fake_get)
    monkeypatch.setattr(Wave_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    Wave_API.get_wave_data(33.66, -117.99)
    Wave_API.get_wave_data(34.02, -118.78)

    assert call_count["count"] == 2


def test_cached_data_matches_original_response(monkeypatch, fake_api_response):
    Wave_API._cache.clear()

    def fake_get(url, params=None):
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(Wave_API.requests, "get", fake_get)
    monkeypatch.setattr(Wave_API, "_utcnow_naive", lambda: datetime(2026, 9, 13, 12, 0))

    first = Wave_API.get_wave_data(33.66, -117.99)
    second = Wave_API.get_wave_data(33.66, -117.99)

    assert first == second == fake_api_response