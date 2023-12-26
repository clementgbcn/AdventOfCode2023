from dataclasses import dataclass
from typing import Iterator

import numpy as np

from day_factory.day import Day
from day_factory.day_utils import TestEnum
from utils.utils import extract_int


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @classmethod
    def build_from_string(cls, hailstone_str: str):
        x, y, z, dx, dy, dz = extract_int(hailstone_str)
        return Hailstone(x, y, z, dx, dy, dz)

    def get_y_from_x(self, x):
        return self.y + self.dy / self.dx * (x - self.x)

    def get_z_from_x(self, x):
        return self.z + self.dz / self.dz * (x - self.x)

    def get_intersect_x(self, other):
        return (
            (self.y - other.y)
            + (other.dy / other.dx * other.x - self.dy / self.dx * self.x)
        ) / (other.dy / other.dx - self.dy / self.dx)

    def get_t_from_x(self, x):
        return (x - self.x) / self.dx

    def get_intersect(self, other):
        if other.dy / other.dx - self.dy / self.dx == 0:
            return None, None, None, None
        x = self.get_intersect_x(other)
        y = self.get_y_from_x(x)
        t1 = self.get_t_from_x(x)
        t2 = other.get_t_from_x(x)
        return x, y, t1, t2


class Day24(Day):
    FIRST_STAR_TEST_RESULT = 2
    SECOND_STAR_TEST_RESULT = 47

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(hailstones_str: Iterator[str], input_type):
        if input_type == TestEnum.TEST:
            lowest_bound = 7
            highest_bound = 27
        else:
            lowest_bound = 200000000000000
            highest_bound = 400000000000000
        hailstones = list(map(lambda h: Hailstone.build_from_string(h), hailstones_str))
        count = 0
        for i, h1 in enumerate(hailstones[:-1]):
            for j, h2 in enumerate(hailstones[i + 1 :]):
                x, y, t1, t2 = h1.get_intersect(h2)
                if x is None and y is None:
                    print(h1, h2)
                if (
                    x is not None
                    and y is not None
                    and t1 >= 0
                    and t2 >= 0
                    and lowest_bound <= x <= highest_bound
                    and lowest_bound <= y <= highest_bound
                ):
                    count += 1
        return count

    @staticmethod
    def solve_2(hailstones_str: Iterator[str]):
        hailstones = list(map(lambda h: Hailstone.build_from_string(h), hailstones_str))
        h0 = hailstones[0]
        a = []
        b = []
        for h in hailstones[1:4]:
            a.append([h.dy - h0.dy, -h.dx + h0.dx, 0, h0.y - h.y, h.x - h0.x, 0])
            a.append([h.dz - h0.dz, 0, -h.dx + h0.dx, h0.z - h.z, 0, h.x - h0.x])
            b.append(h.x * h.dy - h.y * h.dx - h0.x * h0.dy + h0.y * h0.dx)
            b.append(h.x * h.dz - h.z * h.dx - h0.x * h0.dz + h0.z * h0.dx)
        x = np.linalg.solve(np.array(a), np.array(b))
        print(x)
        return round(sum(x[0:3]))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
