from datetime import datetime
from Data.Parsing import parse_wave_dict, HourlyReading, parse_wind_dict, WindReading
 
 
def test_parse_wave_dict_returns_correct_number_of_readings(fake_api_response):
    result = parse_wave_dict(fake_api_response)
    assert len(result) == 3
 
 
def test_parse_wave_dict_keys_are_datetimes(fake_api_response):
    result = parse_wave_dict(fake_api_response)
    for key in result:
        assert isinstance(key, datetime)
 
 
def test_parse_wave_dict_produces_hourly_reading_objects(fake_api_response):
    result = parse_wave_dict(fake_api_response)
    for reading in result.values():
        assert isinstance(reading, HourlyReading)
 
 
def test_parse_wave_dict_maps_fields_correctly(fake_api_response):
    result = parse_wave_dict(fake_api_response)
    first_hour = datetime(2026, 9, 13, 0, 0)
    reading = result[first_hour]
 
    assert reading.time == first_hour
    assert reading.wave_height == 0.9
    assert reading.wave_period == 10.0
    assert reading.wave_direction == 220
    assert reading.swell_height == 0.5
    assert reading.swell_period == 12.0
    assert reading.swell_direction == 195
 
 
def test_parse_wave_dict_key_matches_readings_own_time_field(fake_api_response):
    # Each reading should be stored under the same time it reports internally --
    # catches a copy/paste bug where the key and the .time field could drift apart.
    result = parse_wave_dict(fake_api_response)
    for key, reading in result.items():
        assert key == reading.time
 
 
def test_parse_wave_dict_handles_empty_hourly_data():
    empty_response = {
        "hourly": {
            "time": [],
            "wave_height": [],
            "wave_period": [],
            "wave_direction": [],
            "swell_wave_height": [],
            "swell_wave_period": [],
            "swell_wave_direction": [],
        }
    }
    result = parse_wave_dict(empty_response)
    assert result == {}
 
 
def test_parse_wind_dict_returns_correct_number_of_readings(fake_wind_api_response):
    result = parse_wind_dict(fake_wind_api_response)
    assert len(result) == 3
 
 
def test_parse_wind_dict_produces_wind_reading_objects(fake_wind_api_response):
    result = parse_wind_dict(fake_wind_api_response)
    for reading in result.values():
        assert isinstance(reading, WindReading)
 
 
def test_parse_wind_dict_maps_fields_correctly(fake_wind_api_response):
    result = parse_wind_dict(fake_wind_api_response)
    first_hour = datetime(2026, 9, 13, 0, 0)
    reading = result[first_hour]
 
    assert reading.time == first_hour
    assert reading.wind_speed == 5.2
    assert reading.wind_direction == 270
 
 
def test_parse_wind_dict_key_matches_readings_own_time_field(fake_wind_api_response):
    result = parse_wind_dict(fake_wind_api_response)
    for key, reading in result.items():
        assert key == reading.time
 
 
def test_parse_wind_dict_handles_empty_hourly_data():
    empty_response = {
        "hourly": {
            "time": [],
            "wind_speed_10m": [],
            "wind_direction_10m": [],
        }
    }
    result = parse_wind_dict(empty_response)
    assert result == {}
 