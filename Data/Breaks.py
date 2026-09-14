import abc
from Data.API import get_wave_data
from Data.Parsing import parse_forecast_dict
from Data.Wave_Data import Forecast

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

    def __init__(self, forecast: Forecast | None = None):
        self.forecast = forecast if forecast is not None else Forecast(
            parse_forecast_dict(get_wave_data(self.LATITUDE, self.LONGITUDE))
        )

    def get_break_name(self) -> str:
        return "Huntington State Beach"

    def get_break_location(self) -> str:
        return "Huntington Beach, CA"

    def get_break_description(self) -> str:
        return "A popular surf spot known for its consistent waves and vibrant surf culture."

    def get_cordinates(self) -> tuple:
        return (self.LATITUDE, self.LONGITUDE)

    def get_break_forecast(self):
        return self.forecast