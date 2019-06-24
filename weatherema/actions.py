import logging
from typing import Callable

from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Action:
    name: str
    func: Callable

    def run(self):
        logger.info(f"Executing {self.name}")
        self.func()
