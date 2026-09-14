import requests

def get_wave_data(LATITUDE, LONGITUDE) -> dict:
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": "wave_height,wave_period,wave_direction,swell_wave_height,swell_wave_period,swell_wave_direction"
    }
    response = requests.get(url, params=params)
    return response.json()
