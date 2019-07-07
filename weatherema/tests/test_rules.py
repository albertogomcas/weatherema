import datetime

import pytz

from weatherema.actions import UP
from weatherema.rules import RuleChecker, default_rules
from weatherema.weather_monitor import WeatherMonitor, FakeWeather


def utc_now():
    return pytz.utc.localize(datetime.datetime.utcnow())


wmon = WeatherMonitor()

weather = wmon.get_weather()

warm = FakeWeather.from_weather(weather)
warm.clouds = 0
warm.month = 8
warm.max_temperature = 35

cold = FakeWeather.from_weather(weather)
cold.max_temperature = 14

windy = FakeWeather.from_weather(weather)
windy.wind = 20

checker = RuleChecker(rules=default_rules)


def test_rule_check():
    checker.check_rules(information=weather)


def test_cold_up():
    checker.last_action_time = 0
    checker.check_rules(information=cold)
    assert checker.last_action == UP


def test_too_near_overriden():
    checker.last_action_time = 0
    checker.check_rules(information=cold)
    assert checker.last_action == UP
    checker.check_rules(information=weather)
    assert checker.last_action == UP


def test_windy_up():
    checker.check_rules(information=windy)
    assert checker.last_action == UP


def test_manual():
    pass


def test_windy_overrides_manual():
    pass
