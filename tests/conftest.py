from dataclasses import replace
from datetime import datetime, timedelta
import pytest

from Data.Parsing import WaveReading


def make_reading(hour_offset: int, base_time: datetime | None = None, **overrides) -> WaveReading:
    base_time = base_time or datetime(2026, 9, 13, 0, 0)
    reading = WaveReading(
        time=base_time + timedelta(hours=hour_offset),
        wave_height=1.0,
        wave_period=10.0,
        wave_direction=200,
        swell_height=0.8,
        swell_period=11.0,
        swell_direction=190,
    )
    return replace(reading, **overrides)


@pytest.fixture
def sample_readings():
    return [make_reading(i, wave_height=float(i)) for i in range(24)]


@pytest.fixture
def sample_readings_dict(sample_readings):
    return {r.time: r for r in sample_readings}


@pytest.fixture
def fake_api_response():
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

@pytest.fixture
def fake_wind_api_response():
    """
    A small, hand-built fake of what Open-Meteo's regular forecast API
    returns for wind, trimmed to 3 hours to match fake_api_response above.
    """
    return {
        "latitude": 33.66,
        "longitude": -117.99,
        "hourly_units": {
            "time": "iso8601",
            "wind_speed_10m": "mp/h",
            "wind_direction_10m": "\u00b0",
        },
        "hourly": {
            "time": [
                "2026-09-13T00:00",
                "2026-09-13T01:00",
                "2026-09-13T02:00",
            ],
            "wind_speed_10m": [5.2, 6.1, 7.8],
            "wind_direction_10m": [270, 265, 260],
        },
    }

@pytest.fixture
def fake_tide_api_response():
    """
    A small, hand-built fake of what NOAA CO-OPS returns for 6-minute-interval
    tide predictions, trimmed to a few points to keep tests easy to verify.
    Note: NOAA's timestamps use a space, not 'T', and values come back as
    strings -- both worth handling deliberately when parsing.
    """
    return {
        "predictions": [
            {"t": "2026-09-13 00:00", "v": "2.145"},
            {"t": "2026-09-13 00:06", "v": "2.198"},
            {"t": "2026-09-13 00:12", "v": "2.251"},
        ]
    }
