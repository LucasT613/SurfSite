from datetime import datetime, timedelta
from Data.Parsing import HourlyReading

class Forecast:

    def __init__(self, hourly_readings: dict):
        self.hourly_readings_dict = hourly_readings

    def get_hourly_readings_dict(self) -> dict:
        return self.hourly_readings_dict

    def get_hourly_reading_at_time(self, time: datetime) -> HourlyReading:
        return self.hourly_readings_dict[time]

    def get_hourly_readings_over_range(self, start_time: datetime, end_time: datetime) -> list:
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        end_time = end_time.replace(minute=0, second=0, microsecond=0)
        readings = []
        while start_time <= end_time:
            if start_time in self.hourly_readings_dict:
                readings.append(self.hourly_readings_dict[start_time])
            start_time += timedelta(hours=1)
        return readings