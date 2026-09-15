from datetime import datetime

import Data.Breaks
from Data.Forcast import Forecast
from tests.conftest import make_reading


def make_test_forecast() -> Forecast:
    readings = [make_reading(i, wave_height=float(i)) for i in range(5)]
    return Forecast({r.time: r for r in readings})


def test_huntington_state_beach_name():
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=make_test_forecast())
    assert beach.get_break_name() == "Huntington State Beach"


def test_huntington_state_beach_location():
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=make_test_forecast())
    assert beach.get_break_location() == "Huntington Beach, CA"


def test_huntington_state_beach_description_is_nonempty_string():
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=make_test_forecast())
    description = beach.get_break_description()
    assert isinstance(description, str)
    assert len(description) > 0


def test_huntington_state_beach_coordinates():
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=make_test_forecast())
    assert beach.get_cordinates() == (33.6595, -117.9988)


def test_huntington_state_beach_get_wave_forecast_returns_injected_forecast():
    forecast = make_test_forecast()
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=forecast)
    assert beach.get_wave_forecast() is forecast


def test_huntington_state_beach_forecast_data_is_queryable():
    forecast = make_test_forecast()
    beach = Data.Breaks.HuntingtonStateBeach(wave_forecast=forecast)

    reading = beach.get_wave_forecast().get_hourly_reading_at_time(
        datetime(2026, 9, 13, 2, 0)
    )
    assert reading.wave_height == 2.0