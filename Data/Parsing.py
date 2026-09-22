from dataclasses import dataclass
from datetime import datetime

@dataclass
class WaveReading():
    time: datetime
    wave_height: float
    wave_period: float
    wave_direction: float
    swell_height: float
    swell_period: float
    swell_direction: float

@dataclass
class WindReading():
    time: datetime
    wind_speed: float
    wind_direction: float

@dataclass
class TideReading():
    time: datetime
    height: float


def parse_wave_dict(data) -> dict:
    hourly = data['hourly']
    readings = {}
    for i in range(len(hourly['time'])):
        reading = WaveReading(
            time=datetime.fromisoformat(hourly['time'][i]),
            wave_height=hourly['wave_height'][i],
            wave_period=hourly['wave_period'][i],
            wave_direction=hourly['wave_direction'][i],
            swell_height=hourly['swell_wave_height'][i],
            swell_period=hourly['swell_wave_period'][i],
            swell_direction=hourly['swell_wave_direction'][i],
        )
        readings[reading.time] = reading
    return readings
 
def parse_wind_dict(data) -> dict:
    hourly = data['hourly']
    readings = {}
    for i in range(len(hourly['time'])):
        reading = WindReading(
            time=datetime.fromisoformat(hourly['time'][i]),
            wind_speed=hourly['wind_speed_10m'][i],
            wind_direction=hourly['wind_direction_10m'][i],
        )
        readings[reading.time] = reading
    return readings

def parse_tide_dict(data) -> dict:
    predictions = data['predictions']
    readings = {}
    for entry in predictions:
        time = datetime.strptime(entry['t'], "%Y-%m-%d %H:%M")
        reading = TideReading(
            time=time,
            height=float(entry['v']),
        )
        readings[reading.time] = reading
    return readings
