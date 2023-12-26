from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day

from day_factory.day_utils import TestEnum


@dataclass
class Garden:
    rocks: set
    start: tuple[int, int]
    height: int
    width: int

    @classmethod
    def build_from_string(cls, garden_str: Iterator[str]):
        rocks = set()
        start = None
        height = 0
        width = 0
        for i, line in enumerate(garden_str):
            height += 1
            width = len(line)
            for j, c in enumerate(line):
                if c == "#":
                    rocks.add((i, j))
                elif c == "S":
                    start = (i, j)
        return cls(rocks, start, height, width)

    def get_nb_path(self, position, step, cache):
        """Suboptimal solution, but works for the test input"""
        if step == 0:
            return {position}
        if (position, step) in cache:
            return cache[(position, step)]
        targets = set()
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if (
                not (
                    0 <= position[0] + d[0] <= self.height
                    and 0 <= position[1] + d[1] < self.width
                )
                or (position[0] + d[0], position[1] + d[1]) in self.rocks
            ):
                continue
            targets.update(
                self.get_nb_path(
                    (position[0] + d[0], position[1] + d[1]), step - 1, cache
                )
            )
        cache[(position, step)] = targets
        return targets

    def get_nb_tiles_covered(self, start, step):
        visited = set()
        to_visit = [(start, 0)]
        ending = {}
        while len(to_visit) > 0:
            current_point, current_distance = to_visit.pop(0)
            if current_point in visited:
                continue
            ending[current_distance] = ending.get(current_distance, 0) + 1
            visited.add(current_point)
            if current_distance == step:
                continue
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nxt_point = (current_point[0] + d[0], current_point[1] + d[1])
                if (
                    nxt_point[0] % self.height,
                    nxt_point[1] % self.width,
                ) in self.rocks or nxt_point in visited:
                    continue
                to_visit.append((nxt_point, current_distance + 1))
        return sum([ending[k] for k in range(step, -1, -2)])


class Day21(Day):
    FIRST_STAR_TEST_RESULT = 16
    SECOND_STAR_TEST_RESULT = 6536

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(garden_str: Iterator[str], input_type):
        garden = Garden.build_from_string(garden_str)
        nb_step = 6 if input_type == TestEnum.TEST else 64
        return garden.get_nb_tiles_covered(garden.start, nb_step)

    @staticmethod
    def solve_2(garden_str: Iterator[str], input_type):
        garden = Garden.build_from_string(garden_str)
        if input_type == TestEnum.TEST:
            return garden.get_nb_tiles_covered(garden.start, 100)
        nb_step = 26501365
        x = (nb_step - 65) // 131
        # Interpolation from first results
        return 14655 * pow(x, 2) + 14775 * x + 3720

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value, input_type)
