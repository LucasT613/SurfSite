"""
Shared test fixtures and helpers.
"""
from datetime import datetime, timedelta
import pytest

from Data.Parsing import HourlyReading


def make_reading(hour_offset: int, base_time: datetime = None, **overrides) -> HourlyReading:
    """
    Build a HourlyReading for tests without typing out all 7 fields every time.

    hour_offset: how many hours after base_time this reading represents.
    overrides: pass any field name to override its default value,
               e.g. make_reading(2, wave_height=3.0)
    """
    base_time = base_time or datetime(2026, 9, 13, 0, 0)
    defaults = dict(
        time=base_time + timedelta(hours=hour_offset),
        wave_height=1.0,
        wave_period=10.0,
        wave_direction=200,
        swell_height=0.8,
        swell_period=11.0,
        swell_direction=190,
    )
    defaults.update(overrides)
    return HourlyReading(**defaults)


@pytest.fixture
def sample_readings():
    """24 hourly readings starting at 2026-09-13T00:00, values 0..23 for wave_height."""
    return [make_reading(i, wave_height=float(i)) for i in range(24)]


@pytest.fixture
def sample_readings_dict(sample_readings):
    """Same 24 readings, keyed by time, matching what parse_forecast_dict produces."""
    return {r.time: r for r in sample_readings}


@pytest.fixture
def fake_api_response():
    """
    A small, hand-built fake of what Open-Meteo's marine API returns,
    trimmed to 3 hours so tests are easy to read and verify by hand.
    """
    return {
        "latitude": 33.66,
        "longitude": -117.99,
        "hourly_units": {
            "time": "iso8601",
            "wave_height": "m",
            "wave_period": "s",
            "wave_direction": "\u00b0",
            "swell_wave_height": "m",
            "swell_wave_period": "s",
            "swell_wave_direction": "\u00b0",
        },
        "hourly": {
            "time": [
                "2026-09-13T00:00",
                "2026-09-13T01:00",
                "2026-09-13T02:00",
            ],
            "wave_height": [0.9, 1.0, 1.1],
            "wave_period": [10.0, 10.2, 10.4],
            "wave_direction": [220, 221, 222],
            "swell_wave_height": [0.5, 0.55, 0.6],
            "swell_wave_period": [12.0, 12.1, 12.2],
            "swell_wave_direction": [195, 196, 197],
        },
    }
