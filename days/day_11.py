from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day
from day_factory.day_utils import TestEnum


@dataclass
class Star:
    x: int
    y: int

    def get_distance(self, star):
        return abs(self.x - star.x) + abs(self.y - star.y)


@dataclass
class Galaxy:
    stars: list[Star]
    expansion: int

    @classmethod
    def build_from_string(cls, galaxy, expansion):
        stars = []
        i = 0
        columns = None
        # Expanse lines
        for line in galaxy:
            is_empty = True
            if columns is None:
                columns = [1] * len(line)
            for j, star in enumerate(line[::]):
                if star == "#":
                    stars.append(Star(i, j))
                    columns[j] = 0
                    is_empty = False
            i += expansion if is_empty else 1
        # Expanse columns
        count = 0
        for j, value in enumerate(columns):
            if value == 1:
                count += expansion - 1
            columns[j] = count
        stars = list(map(lambda s: Star(s.x, s.y + columns[s.y]), stars))
        return cls(stars, expansion)

    def get_total_distance(self):
        return sum(
            [
                self.stars[x].get_distance(self.stars[y])
                for x in range(len(self.stars) - 1)
                for y in range(x + 1, len(self.stars))
            ]
        )


class Day11(Day):
    FIRST_STAR_TEST_RESULT = 374
    SECOND_STAR_TEST_RESULT = 8410

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(galaxy_str: Iterator[str]):
        galaxy = Galaxy.build_from_string(galaxy_str, 2)
        return galaxy.get_total_distance()

    @staticmethod
    def solve_2(galaxy_str: Iterator[str], input_type):
        expansion = 100 if input_type == TestEnum.TEST else 1000000
        galaxy = Galaxy.build_from_string(galaxy_str, expansion)
        return galaxy.get_total_distance()

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value, input_type)
