import requests
from datetime import datetime, timedelta, timezone

CACHE_DURATION = timedelta(hours=12)
_cache = {}  # station_id -> (time_fetched, data)


def _utcnow_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_tide_data(STATION_ID: str) -> dict:
    key = STATION_ID
    now = _utcnow_naive()

    if key in _cache:
        cached_time, cached_data = _cache[key]
        if now - cached_time < CACHE_DURATION:
            return cached_data

    url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
    params = {
        "station": STATION_ID,
        "product": "predictions",
        "datum": "MLLW",
        "time_zone": "gmt",
        "units": "english",
        "format": "json",
        "interval": "6",
        "range": "168",  # 7 days, in hours, looking forward from now
    }
    response = requests.get(url, params=params)
    data = response.json()

    _cache[key] = (now, data)
    return data