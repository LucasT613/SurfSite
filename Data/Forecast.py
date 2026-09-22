from datetime import datetime, timedelta
from datetime import datetime, timedelta
 
class Forecast:

    def __init__(self, readings: dict, interval_minutes: int = 60):
        self.readings_dict = readings
        self.interval_minutes = interval_minutes

    def get_readings_dict(self) -> dict:
        return self.readings_dict
 
    def get_reading_at_time(self, time: datetime):
        return self.readings_dict[time]

    def get_readings_over_range(self, start_time: datetime, end_time: datetime) -> list:
        start_time = start_time.replace(second=0, microsecond=0)
        end_time = end_time.replace(second=0, microsecond=0)
        readings = []
        while start_time <= end_time:
            if start_time in self.readings_dict:
                readings.append(self.readings_dict[start_time])
            start_time += timedelta(minutes=self.interval_minutes)
        return readings