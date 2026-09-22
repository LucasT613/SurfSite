from datetime import datetime, timedelta
import pytest

from Data.Breaks import Break, HuntingtonStateBeach
from Data.Forecast import Forecast
from Data.Parsing import TideReading
from tests.conftest import make_reading


def make_test_wave_forecast() -> Forecast:
    """A small, known wave Forecast to hand to Break objects under test."""
    readings = [make_reading(i, wave_height=float(i)) for i in range(5)]
    return Forecast({r.time: r for r in readings})


def make_test_wind_forecast() -> Forecast:
    """A small, known wind Forecast to hand to Break objects under test."""
    readings = [make_reading(i, wave_height=float(i)) for i in range(5)]
    return Forecast({r.time: r for r in readings})


def make_test_tide_forecast() -> Forecast:
    """A small, known tide Forecast (6-minute interval) to hand to Break objects under test."""
    base = datetime(2026, 9, 13, 0, 0)
    readings = {}
    for i in range(5):
        t = base + timedelta(minutes=6 * i)
        readings[t] = TideReading(time=t, height=float(i))
    return Forecast(readings, interval_minutes=6)


def make_all_forecasts() -> dict:
    return {
        "wave_forecast": make_test_wave_forecast(),
        "wind_forecast": make_test_wind_forecast(),
        "tide_forecast": make_test_tide_forecast(),
    }


def test_huntington_state_beach_name():
    beach = HuntingtonStateBeach(**make_all_forecasts())
    assert beach.get_break_name() == "Huntington State Beach"


def test_huntington_state_beach_location():
    beach = HuntingtonStateBeach(**make_all_forecasts())
    assert beach.get_break_location() == "Huntington Beach, CA"


def test_huntington_state_beach_description_is_nonempty_string():
    beach = HuntingtonStateBeach(**make_all_forecasts())
    description = beach.get_break_description()
    assert isinstance(description, str)
    assert len(description) > 0


def test_huntington_state_beach_coordinates():
    beach = HuntingtonStateBeach(**make_all_forecasts())
    assert beach.get_cordinates() == (33.6595, -117.9988)


def test_huntington_state_beach_get_wave_forecast_returns_injected_forecast():
    forecasts = make_all_forecasts()
    beach = HuntingtonStateBeach(**forecasts)
    assert beach.get_wave_forecast() is forecasts["wave_forecast"]


def test_huntington_state_beach_get_wind_forecast_returns_injected_forecast():
    forecasts = make_all_forecasts()
    beach = HuntingtonStateBeach(**forecasts)
    assert beach.get_wind_forecast() is forecasts["wind_forecast"]


def test_huntington_state_beach_get_tide_forecast_returns_injected_forecast():
    forecasts = make_all_forecasts()
    beach = HuntingtonStateBeach(**forecasts)
    assert beach.get_tide_forecast() is forecasts["tide_forecast"]


def test_huntington_state_beach_wave_forecast_data_is_queryable():
    beach = HuntingtonStateBeach(**make_all_forecasts())

    reading = beach.get_wave_forecast().get_reading_at_time(
        datetime(2026, 9, 13, 2, 0)
    )
    assert reading.wave_height == 2.0


def test_huntington_state_beach_tide_forecast_data_is_queryable_at_six_minute_marks():
    beach = HuntingtonStateBeach(**make_all_forecasts())

    reading = beach.get_tide_forecast().get_reading_at_time(
        datetime(2026, 9, 13, 0, 12)  # third reading, 6*2 minutes in
    )
    assert reading.height == 2.0


def test_huntington_state_beach_tide_forecast_keeps_its_own_interval():
    beach = HuntingtonStateBeach(**make_all_forecasts())
    assert beach.get_tide_forecast().interval_minutes == 6
    # wave/wind still default to hourly, unaffected by tide's interval
    assert beach.get_wave_forecast().interval_minutes == 60
    assert beach.get_wind_forecast().interval_minutes == 60