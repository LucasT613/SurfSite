from dataclasses import dataclass
from datetime import datetime

@dataclass
class HourlyReading:
    time: datetime
    wave_height: float
    wave_period: float
    wave_direction: float
    swell_height: float
    swell_period: float
    swell_direction: float

@dataclass
class WindReading:
    time: datetime
    wind_speed: float
    wind_direction: float

def parse_wave_dict(data) -> dict:
    hourly = data['hourly']
    readings = {}
    for i in range(len(hourly['time'])):
        reading = HourlyReading(
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