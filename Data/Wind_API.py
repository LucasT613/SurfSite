import requests
from datetime import datetime, timedelta, timezone

CACHE_DURATION = timedelta(minutes=30)
_cache = {}  # (lat, lon) -> (time_fetched, data)


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_wind_data(LATITUDE, LONGITUDE) -> dict:
    key = (LATITUDE, LONGITUDE)
    now = _utcnow_naive()

    if key in _cache:
        cached_time, cached_data = _cache[key]
        if now - cached_time < CACHE_DURATION:
            return cached_data

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "wind_speed_10m,wind_direction_10m",
        "wind_speed_unit": "kn",
    }
    response = requests.get(url, params=params)
    data = response.json()

    _cache[key] = (now, data)
    return data