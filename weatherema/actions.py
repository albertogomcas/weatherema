import logging
from typing import Callable

from dataclasses import dataclass

logger = logging.getLogger(__name__)


def roll_up():
    print("UP")
    # subprocess.check_call(['aircontrol', '-c', 'aircontrol.conf', '-t', 'warema_up'])


def roll_down():
    print("DOWN")
    # subprocess.check_call(['aircontrol', '-c', 'aircontrol.conf', '-t', 'warema_down'])

@dataclass
class Action:
    name: str
    func: Callable

    def run(self):
        logger.info(f"Executing {self.name}")
        self.func()


UP = Action(name="UP", func=roll_up)
DOWN = Action(name="DOWN", func=roll_down)
