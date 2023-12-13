from dataclasses import dataclass
from itertools import groupby
from typing import Iterator

from day_factory.day import Day


@dataclass
class Pattern:
    grid: list[str]

    def find_reflection_for_dim(
        self, dimension: int, size_dim: int, size_opposite_dim: int
    ) -> int:
        for i in range(size_dim - 1):
            j = 0
            is_reflection = True
            while 0 <= i - j and i + 1 + j < size_dim and is_reflection:
                if dimension == 100 and self.grid[i - j] != self.grid[i + 1 + j]:
                    is_reflection = False
                elif dimension == 1:
                    for k in range(size_opposite_dim):
                        if self.grid[k][i - j] != self.grid[k][i + 1 + j]:
                            is_reflection = False
                            break
                j += 1
            if is_reflection:
                return dimension * (i + 1)
        return 0

    def find_reflection(self) -> int:
        res = self.find_reflection_for_dim(100, len(self.grid), len(self.grid[0]))
        if res == 0:
            return self.find_reflection_for_dim(1, len(self.grid[0]), len(self.grid))
        return res

    def find_new_reflection_for_dim(
        self, dimension: int, size_dim: int, size_opposite_dim: int
    ) -> int:
        for i in range(size_dim - 1):
            j = 0
            nb_difference = 0
            while 0 <= i - j and i + 1 + j < size_dim and nb_difference < 2:
                for k in range(size_opposite_dim):
                    if (
                        dimension == 100
                        and self.grid[i - j][k] != self.grid[i + 1 + j][k]
                    ):
                        nb_difference += 1
                    elif (
                        dimension == 1
                        and self.grid[k][i - j] != self.grid[k][i + 1 + j]
                    ):
                        nb_difference += 1
                j += 1
            if nb_difference == 1:
                return dimension * (i + 1)
        return 0

    def find_new_reflection(self) -> int:
        res = self.find_new_reflection_for_dim(100, len(self.grid), len(self.grid[0]))
        if res == 0:
            return self.find_new_reflection_for_dim(
                1, len(self.grid[0]), len(self.grid)
            )
        return res


class Day13(Day):
    FIRST_STAR_TEST_RESULT = 405
    SECOND_STAR_TEST_RESULT = 400

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(patterns_str: Iterator[str]):
        return sum(
            [
                Pattern(list(group)).find_reflection()
                for key, group in groupby(patterns_str, lambda x: x != "")
                if key
            ]
        )

    @staticmethod
    def solve_2(patterns_str: Iterator[str]):
        return sum(
            [
                Pattern(list(group)).find_new_reflection()
                for key, group in groupby(patterns_str, lambda x: x != "")
                if key
            ]
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
