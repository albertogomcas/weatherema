from weatherema.weather_monitor import WeatherMonitor


def test_get_weather():
    w = WeatherMonitor()
    weather = w.get_weather()
