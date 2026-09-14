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

def parse_forecast_dict(data) -> dict:
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