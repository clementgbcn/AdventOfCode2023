from dataclasses import dataclass
from enum import Enum


class TestEnum(Enum):
    __test__ = False
    TEST = 0
    PROBLEM = 1


class Star(Enum):
    FIRST = 1
    SECOND = 2

    def __str__(self):
        if self.value == Star.FIRST.value:
            return "1st"
        else:
            return "2nd"


class UnknownStarException(Exception):
    def __init__(self, star):
        super().__init__("Unknown Star: " + star)


@dataclass
class Result:
    day: int
    test: TestEnum
    star: Star
    result: int
