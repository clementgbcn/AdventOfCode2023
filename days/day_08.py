import re
from dataclasses import dataclass

from functools import reduce
from math import lcm
from typing import Iterator

from day_factory.day import Day


@dataclass
class Edge:
    left: str
    right: str

    def get_next(self, order: str, step: int):
        direction = order[step % len(order)]
        return self.left if direction == "L" else self.right


class Day08(Day):
    FIRST_STAR_TEST_RESULT = 2
    SECOND_STAR_TEST_RESULT = 6

    PATH_PATTERN = re.compile(r"([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)")

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def parse_paths(paths: Iterator[str]) -> (str, dict[str, Edge]):
        order = next(paths)
        next(paths)
        mapping = {
            p[0]: Edge(p[1], p[2])
            for p in map(lambda path: Day08.PATH_PATTERN.findall(path)[0], paths)
        }
        return order, mapping

    @staticmethod
    def solve_1(paths: Iterator[str]):
        order, mapping = Day08.parse_paths(paths)
        current_pos = "AAA"
        step = 0
        while current_pos != "ZZZ":
            current_pos = mapping[current_pos].get_next(order, step)
            step += 1
        return step

    @staticmethod
    def solve_2(paths: Iterator[str]):
        order, mapping = Day08.parse_paths(paths)
        current_positions = list(filter(lambda p: p[-1] == "A", mapping.keys()))
        data = []
        for pos in current_positions:
            step = 0
            current_position = pos
            while current_position[-1] != "Z":
                current_position = mapping[current_position].get_next(order, step)
                step += 1
            data.append(step)
        return reduce(lambda x, y: lcm(x, y), data)

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
