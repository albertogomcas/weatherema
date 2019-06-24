import configparser
import time
from pathlib import Path

import pyowm


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

        return weather
