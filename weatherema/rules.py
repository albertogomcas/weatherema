import logging
from typing import TYPE_CHECKING

from dataclasses import dataclass

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .actions import Action


@dataclass
class Rule:
    priority: int
    action: Action

    def check(self, information=None):
        return False

    def __lt__(self, other: "Rule"):
        pass


class RuleChecker:
    def __init__(self, rules):
        self.rules = rules

    def check_rules(self, information=None):
        relevant = [rule for rule in self.rules if rule.check(information)]
