from datetime import datetime, timedelta
import pytest

from Data.Forecast import Forecast
from Data.Parsing import TideReading
from tests.conftest import make_reading


def test_get_readings_dict_returns_the_same_dict(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    assert forecast.get_readings_dict() == sample_readings_dict


def test_get_reading_at_time_returns_correct_reading(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    target_time = datetime(2026, 9, 13, 5, 0)
    reading = forecast.get_reading_at_time(target_time)
    assert reading.time == target_time
    assert reading.wave_height == 5.0


def test_get_reading_at_time_raises_for_missing_time(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    missing_time = datetime(2099, 1, 1, 0, 0)
    with pytest.raises(KeyError):
        forecast.get_reading_at_time(missing_time)


def test_get_range_includes_both_boundaries(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    start = datetime(2026, 9, 13, 5, 0)
    end = datetime(2026, 9, 13, 8, 0)
    result = forecast.get_readings_over_range(start, end)

    assert len(result) == 4
    assert result[0].time == start
    assert result[-1].time == end


def test_get_range_returns_readings_in_chronological_order(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    result = forecast.get_readings_over_range(
        datetime(2026, 9, 13, 2, 0), datetime(2026, 9, 13, 6, 0)
    )
    times = [r.time for r in result]
    assert times == sorted(times)


def test_get_range_normalizes_messy_start_and_end_times(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    messy_start = datetime(2026, 9, 13, 2, 0, 17, 123)
    messy_end = datetime(2026, 9, 13, 4, 0, 59, 999)

    result = forecast.get_readings_over_range(messy_start, messy_end)

    assert len(result) == 3  # hours 2, 3, 4
    assert result[0].time == datetime(2026, 9, 13, 2, 0)
    assert result[-1].time == datetime(2026, 9, 13, 4, 0)


def test_get_range_with_single_hour_span(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    same_time = datetime(2026, 9, 13, 10, 0)
    result = forecast.get_readings_over_range(same_time, same_time)
    assert len(result) == 1
    assert result[0].time == same_time


def test_get_range_returns_empty_list_when_start_after_end(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    start = datetime(2026, 9, 13, 10, 0)
    end = datetime(2026, 9, 13, 5, 0)  # before start
    result = forecast.get_readings_over_range(start, end)
    assert result == []


def test_get_range_skips_missing_hours_without_erroring():
    readings = [make_reading(0), make_reading(1), make_reading(5)]
    readings_dict = {r.time: r for r in readings}
    forecast = Forecast(readings_dict)

    result = forecast.get_readings_over_range(
        datetime(2026, 9, 13, 0, 0), datetime(2026, 9, 13, 5, 0)
    )

    # Only the 3 hours that actually exist should come back, not 6
    assert len(result) == 3
    assert [r.time.hour for r in result] == [0, 1, 5]


def test_get_range_outside_available_data_returns_empty_list(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    result = forecast.get_readings_over_range(
        datetime(2026, 9, 20, 0, 0), datetime(2026, 9, 20, 5, 0)
    )
    assert result == []


def make_tide_readings_dict(base_time: datetime, count: int) -> dict:
    """count readings, 6 minutes apart, starting at base_time."""
    readings = {}
    for i in range(count):
        t = base_time + timedelta(minutes=6 * i)
        readings[t] = TideReading(time=t, height=float(i))
    return readings


def test_default_interval_would_miss_six_minute_data():
    base = datetime(2026, 9, 13, 0, 0)
    readings_dict = make_tide_readings_dict(base, count=20)  # 0:00 through 1:54
    forecast = Forecast(readings_dict)  # interval_minutes defaults to 60

    result = forecast.get_readings_over_range(base, base + timedelta(hours=2))

    assert len(result) == 2
    assert [r.time for r in result] == [base, base + timedelta(hours=1)]


def test_interval_minutes_six_returns_all_readings_in_range():
    base = datetime(2026, 9, 13, 0, 0)
    readings_dict = make_tide_readings_dict(base, count=20)  # 0:00 through 1:54
    forecast = Forecast(readings_dict, interval_minutes=6)

    result = forecast.get_readings_over_range(base, base + timedelta(hours=2))

    assert len(result) == 20
    assert result[0].time == base
    assert result[-1].time == base + timedelta(minutes=6 * 19)


def test_interval_minutes_six_respects_range_boundaries():
    base = datetime(2026, 9, 13, 0, 0)
    readings_dict = make_tide_readings_dict(base, count=20)
    forecast = Forecast(readings_dict, interval_minutes=6)

    result = forecast.get_readings_over_range(base, base + timedelta(minutes=30))

    assert len(result) == 6
    assert result[-1].time == base + timedelta(minutes=30)


def test_interval_minutes_defaults_to_sixty_when_unspecified(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    assert forecast.interval_minutes == 60