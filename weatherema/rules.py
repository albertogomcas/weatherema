import datetime
import logging
import time

from dataclasses import dataclass

from .actions import Action, UP, DOWN

logger = logging.getLogger(__name__)


@dataclass
class Rule:
    priority: int
    action: Action
    expire: int = None

    def check(self, information=None):
        return self.expire is None or time.time() > self.expire

    def __lt__(self, other: "Rule"):
        return self.priority < other.priority


class Day(Rule):
    delay_hours = datetime.timedelta(hours=2)
    advance_hours = datetime.timedelta(hours=2)

    def check(self, information):
        return super().check() and information.sunrise + Day.delay_hours < information.reference_time < information.sunset - Day.advance_hours


class ColdMonths(Rule):
    months = [1, 2, 3, 4, 11, 12]

    def check(self, information):
        return super().check() and information.month in ColdMonths.months


class ColdDay(Rule):
    max_temperature = 18

    def check(self, information):
        return super().check() and information.max_temperature < ColdDay.max_temperature


class Windy(Rule):
    max_windspeed = 11  # m/s 10-13.8 is strong breeze in Beaufort scale

    def check(self, information):
        return super().check() and information.wind > Windy.max_windspeed


class Covered(Rule):
    min_coverage = 80  # percent

    def check(self, information):
        return super().check() and information.clouds >= Covered.min_coverage


class Default(Rule):
    def check(self, information):
        return True


class ManualUp(Rule):
    def check(self, information):
        return super().check()


class ManualDown(Rule):
    def check(self, information):
        return super().check()

default_rules = [
    Windy(priority=100, action=UP),
    ColdMonths(priority=90, action=UP),
    ColdDay(priority=90, action=UP),
    Covered(priority=80, action=UP),
    Day(priority=50, action=DOWN),
    Default(priority=0, action=UP)
]


class RuleChecker:
    def __init__(self, rules):
        self.rules = rules
        self.dead_time_min = 60
        self.last_action = None
        self.last_action_time = 0
        self.override_dead_time_prio = 99

    def check_rules(self, information):
        relevant = sorted([rule for rule in self.rules if rule.check(information)])
        print(relevant)

        top_rule = max(relevant)
        print(f"Higher priority: {top_rule}")

        elapsed = time.time() - self.last_action_time

        if self.last_action and elapsed < self.dead_time_min * 60 and top_rule.priority < self.override_dead_time_prio:
            print("Rule overriden")
        else:
            self.execute(top_rule)

    def execute(self, rule):
        rule.action.run()
        self.last_action = rule.action
        self.last_action_time = time.time()
