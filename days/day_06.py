import math
from functools import reduce
from typing import Iterator

from day_factory.day import Day
from utils.utils import extract_int


class Day06(Day):
    FIRST_STAR_TEST_RESULT = 288
    SECOND_STAR_TEST_RESULT = 71503

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def get_nb_values(t: int, d: int) -> int:
        delta = math.sqrt(t * t - 4 * d)
        start, end = (t - delta) / 2, (t + delta) / 2
        start = int(start) + 1 if start.is_integer() else math.ceil(start)
        end = int(end) if end.is_integer() else math.ceil(end)
        return end - start

    @staticmethod
    def solve_1(values: Iterator[str]):
        targets = list(zip(extract_int(next(values)), extract_int(next(values))))
        return reduce(
            lambda x, y: x * y, map(lambda x: Day06.get_nb_values(x[0], x[1]), targets)
        )

    @staticmethod
    def solve_2(values: Iterator[str]):
        t = int(next(values).replace("Time:", " ").replace(" ", ""))
        d = int(next(values).replace("Distance:", " ").replace(" ", ""))
        return Day06.get_nb_values(t, d)

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
