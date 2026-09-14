from datetime import datetime, timedelta
import pytest

from Data.Wave_Data import Forecast
from tests.conftest import make_reading


def test_get_hourly_readings_dict_returns_the_same_dict(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    assert forecast.get_hourly_readings_dict() == sample_readings_dict


def test_get_hourly_reading_at_time_returns_correct_reading(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    target_time = datetime(2026, 9, 13, 5, 0)
    reading = forecast.get_hourly_reading_at_time(target_time)
    assert reading.time == target_time
    assert reading.wave_height == 5.0


def test_get_hourly_reading_at_time_raises_for_missing_time(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    missing_time = datetime(2099, 1, 1, 0, 0)
    with pytest.raises(KeyError):
        forecast.get_hourly_reading_at_time(missing_time)


def test_get_range_includes_both_boundaries(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    start = datetime(2026, 9, 13, 5, 0)
    end = datetime(2026, 9, 13, 8, 0)
    result = forecast.get_hourly_readings_over_range(start, end)

    # hours 5, 6, 7, 8 -> 4 readings, both ends included
    assert len(result) == 4
    assert result[0].time == start
    assert result[-1].time == end


def test_get_range_returns_readings_in_chronological_order(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    result = forecast.get_hourly_readings_over_range(
        datetime(2026, 9, 13, 2, 0), datetime(2026, 9, 13, 6, 0)
    )
    times = [r.time for r in result]
    assert times == sorted(times)


def test_get_range_normalizes_messy_start_and_end_times(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    messy_start = datetime(2026, 9, 13, 2, 0, 17, 123)
    messy_end = datetime(2026, 9, 13, 4, 0, 59, 999)

    result = forecast.get_hourly_readings_over_range(messy_start, messy_end)

    assert len(result) == 3  # hours 2, 3, 4
    assert result[0].time == datetime(2026, 9, 13, 2, 0)
    assert result[-1].time == datetime(2026, 9, 13, 4, 0)


def test_get_range_with_single_hour_span(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    same_time = datetime(2026, 9, 13, 10, 0)
    result = forecast.get_hourly_readings_over_range(same_time, same_time)
    assert len(result) == 1
    assert result[0].time == same_time


def test_get_range_returns_empty_list_when_start_after_end(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    start = datetime(2026, 9, 13, 10, 0)
    end = datetime(2026, 9, 13, 5, 0)  # before start
    result = forecast.get_hourly_readings_over_range(start, end)
    assert result == []


def test_get_range_skips_missing_hours_without_erroring():
    readings = [make_reading(0), make_reading(1), make_reading(5)]
    readings_dict = {r.time: r for r in readings}
    forecast = Forecast(readings_dict)

    result = forecast.get_hourly_readings_over_range(
        datetime(2026, 9, 13, 0, 0), datetime(2026, 9, 13, 5, 0)
    )

    assert len(result) == 3
    assert [r.time.hour for r in result] == [0, 1, 5]


def test_get_range_outside_available_data_returns_empty_list(sample_readings_dict):
    forecast = Forecast(sample_readings_dict)
    result = forecast.get_hourly_readings_over_range(
        datetime(2026, 9, 20, 0, 0), datetime(2026, 9, 20, 5, 0)
    )
    assert result == []
