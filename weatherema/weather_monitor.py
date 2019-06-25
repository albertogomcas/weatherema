import configparser
import datetime
import time
from pathlib import Path

import pyowm
from dataclasses import dataclass


class WeatherInfo:
    """Thin wrapper over OWM info"""

    def __init__(self, owm_weather):
        self.owm_weather = owm_weather

    @property
    def clouds(self):
        return self.owm_weather.get_clouds()

    @property
    def sunset(self):
        return self.owm_weather.get_sunset_time("date")

    @property
    def sunrise(self):
        return self.owm_weather.get_sunrise_time("date")

    @property
    def reference_time(self):
        return self.owm_weather.get_reference_time("date")

    @property
    def month(self):
        return int(self.reference_time.strftime("%m"))

    @property
    def max_temperature(self):
        return self.owm_weather.get_temperature('celsius')['temp_max']

    @property
    def wind(self):
        return self.owm_weather.get_wind('meters_sec')['speed']


@dataclass
class FakeWeather:
    clouds: int
    sunset: datetime.datetime
    sunrise: datetime.datetime
    reference_time: datetime.datetime
    month: int
    max_temperature: float
    wind: float

    @classmethod
    def from_weather(cls, weather: WeatherInfo):
        return cls(clouds=weather.clouds,
                   sunset=weather.sunset,
                   sunrise=weather.sunrise,
                   reference_time=weather.reference_time,
                   month=weather.month,
                   max_temperature=weather.max_temperature,
                   wind=weather.wind)

class WeatherMonitor:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(Path(__file__).parent / "owm_config.ini")
        self.api_key = config["DEFAULT"]["owm_id"]
        self.location_id = int(config["DEFAULT"]["location"])
        self.owm = pyowm.OWM(API_key=self.api_key)
        self.last_check = None
        self.last_weather = None

    def get_weather(self):
        if self.last_check and time.time() - self.last_check < self.min_interval:
            return self.last_weather

        observation = self.owm.weather_at_id(self.location_id)
        weather = observation.get_weather()
        print(f'Temp: {weather.get_temperature(unit="celsius")["temp"]}')

        self.last_check = time.time()
        self.last_weather = weather

        return WeatherInfo(weather)
