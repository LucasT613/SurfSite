import abc
from Data.Wave_API import get_wave_data
from Data.Parsing import parse_wave_dict, parse_wind_dict
from Data.Forcast import Forecast
from Data.Wind_API import get_wind_data

class Break(abc.ABC):

    @abc.abstractmethod
    def get_break_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_break_location(self) -> str:
        pass

    @abc.abstractmethod
    def get_break_description(self) -> str:
        pass

    @abc.abstractmethod
    def get_cordinates(self) -> tuple:
        pass

    def get_break_forecast(self):
        pass

class HuntingtonStateBeach(Break):
    LATITUDE = 33.6595
    LONGITUDE = -117.9988

    def __init__(self, wave_forecast: Forecast | None = None, wind_forecast: Forecast | None = None):
        self.wave_forecast = wave_forecast if wave_forecast is not None else Forecast(
            parse_wave_dict(get_wave_data(self.LATITUDE, self.LONGITUDE))
        )
        self.wind_forecast = wind_forecast if wind_forecast is not None else Forecast(
            parse_wind_dict(get_wind_data(self.LATITUDE, self.LONGITUDE))
        )

    def get_break_name(self) -> str:
        return "Huntington State Beach"

    def get_break_location(self) -> str:
        return "Huntington Beach, CA"

    def get_break_description(self) -> str:
        return "A popular surf spot known for its consistent waves and vibrant surf culture."

    def get_cordinates(self) -> tuple:
        return (self.LATITUDE, self.LONGITUDE)

    def get_wave_forecast(self):
        return self.wave_forecast

    def get_wind_forecast(self):
        return self.wind_forecast