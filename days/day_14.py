import bisect
from dataclasses import dataclass
from enum import Enum
from typing import Iterator

from day_factory.day import Day


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    WEST = "east"
    EAST = "west"


@dataclass
class Grid:
    rounded_by_row: dict[int, list[int]]
    rounded_by_col: dict[int, list[int]]
    ordered_row: list[int]
    ordered_col: list[int]
    cubes: set[tuple[int, int]]
    nb_row: int
    nb_col: int

    @classmethod
    def build_from_string(cls, grid_str: Iterator[str]):
        cubes = set()
        rounded_by_col = {}
        ordered_col = []
        nb_row, nb_col = 0, 0
        for row, line in enumerate(grid_str):
            nb_col = len(line)
            for col, char in enumerate(line):
                if char == "#":
                    cubes.add((row, col))
                elif char == "O":
                    rounded_by_col[col] = rounded_by_col.get(col, []) + [row]
                    if len(rounded_by_col[col]) == 1:
                        bisect.insort(ordered_col, col)
            nb_row = row
        nb_row += 1
        return cls({}, rounded_by_col, [], ordered_col, cubes, nb_row, nb_col)

    def get_hash(self):
        hsh = ""
        for j, rows in self.rounded_by_col.items():
            col = ["."] * self.nb_row
            for i in rows:
                col[i] = "#"
            hsh += "".join(col)
        return hsh

    def get_sum(self):
        total = 0
        for j, rows in self.rounded_by_col.items():
            for i in rows:
                total += self.nb_row - i
        return total

    def get_sum_from_row(self):
        total = 0
        for i, cols in self.rounded_by_row.items():
            total += (self.nb_row - i) * len(cols)
        return total

    def process_direction(self, direction: Direction):
        if direction == Direction.NORTH:
            self.process_north()
        elif direction == Direction.SOUTH:
            self.process_south()
        elif direction == Direction.EAST:
            self.process_east()
        else:
            self.process_west()

    def process_north(self):
        self.rounded_by_row = {}
        self.ordered_row = []
        for j in sorted(self.rounded_by_col.keys()):
            for i in self.rounded_by_col[j]:
                k = i - 1
                while (
                    k >= 0
                    and (k, j) not in self.cubes
                    and j > self.rounded_by_row.get(k, [-1])[-1]
                ):
                    k -= 1
                k += 1
                if k not in self.rounded_by_row:
                    self.rounded_by_row[k] = []
                    bisect.insort(self.ordered_row, k)
                self.rounded_by_row[k].append(j)

    def process_south(self):
        self.rounded_by_row = {}
        self.ordered_row = []
        for j in self.ordered_col:
            for i in self.rounded_by_col[j][::-1]:
                k = i + 1
                while (
                    k < self.nb_row
                    and (k, j) not in self.cubes
                    and j > self.rounded_by_row.get(k, [-1])[-1]
                ):
                    k += 1
                k -= 1
                if k not in self.rounded_by_row:
                    self.rounded_by_row[k] = []
                    bisect.insort(self.ordered_row, k)
                self.rounded_by_row[k].append(j)

    def process_east(self):
        self.rounded_by_col = {}
        self.ordered_col = []
        for i in self.ordered_row:
            for j in self.rounded_by_row[i][::-1]:
                k = j + 1
                while (
                    k < self.nb_col
                    and (i, k) not in self.cubes
                    and i > self.rounded_by_col.get(k, [-1])[-1]
                ):
                    k += 1
                k -= 1
                if k not in self.rounded_by_col:
                    self.rounded_by_col[k] = []
                    bisect.insort(self.ordered_col, k)
                self.rounded_by_col[k].append(i)

    def process_west(self):
        self.rounded_by_col = {}
        self.ordered_col = []
        for i in self.ordered_row:
            for j in self.rounded_by_row[i]:
                k = j - 1
                while (
                    k >= 0
                    and (i, k) not in self.cubes
                    and i > self.rounded_by_col.get(k, [-1])[-1]
                ):
                    k -= 1
                k += 1
                if k not in self.rounded_by_col:
                    self.rounded_by_col[k] = []
                    bisect.insort(self.ordered_col, k)
                self.rounded_by_col[k].append(i)


class Day14(Day):
    FIRST_STAR_TEST_RESULT = 136
    SECOND_STAR_TEST_RESULT = 64

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(reflector_str: Iterator[str]):
        grid = Grid.build_from_string(reflector_str)
        grid.process_direction(Direction.NORTH)
        return grid.get_sum_from_row()

    @staticmethod
    def solve_2(reflector_str: Iterator[str]):
        nb_round = 1000000000
        grid = Grid.build_from_string(reflector_str)
        r = 0
        positions = {grid.get_hash(): (r, None)}
        totals = {}
        while r < nb_round:
            for direction in [
                Direction.NORTH,
                Direction.WEST,
                Direction.SOUTH,
                Direction.EAST,
            ]:
                grid.process_direction(direction)
            hsh = grid.get_hash()
            if hsh in positions:
                start = positions[hsh][0]
                end = positions[hsh][1]
                if end is None:
                    positions[hsh] = (start, r + 1)
                    end = r
                loop_size = end - start
                return totals[start + ((nb_round - start) % loop_size) - 1]
            else:
                positions[hsh] = (r, None)
            totals[r] = grid.get_sum()
            r += 1
        return grid.get_sum()

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
