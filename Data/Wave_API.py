import requests
from datetime import datetime, timedelta, timezone

CACHE_DURATION = timedelta(minutes=30)
_cache = {}

def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def get_wave_data(LATITUDE, LONGITUDE) -> dict:
    key = (LATITUDE, LONGITUDE)
    now = _utcnow_naive()

    if key in _cache:
        cached_time, cached_data = _cache[key]
        if now - cached_time < CACHE_DURATION:
            return cached_data

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "wave_height,wave_period,wave_direction,swell_wave_height,swell_wave_period,swell_wave_direction"
    }
    response = requests.get(url, params=params)
    data = response.json()

    _cache[key] = (now, data)
    return data
