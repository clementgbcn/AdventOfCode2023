from dataclasses import dataclass
from enum import Enum
from functools import cmp_to_key
from typing import Iterator

from day_factory.day import Day


class Direction(Enum):
    NORTH = "north", [-1, 1, -1, 1]
    SOUTH = "south", [1, -1, -1, 1]
    WEST = "east", [-1, 1, -1, 1]
    EAST = "west", [-1, 1, 1, -1]

    @property
    def ordering(self):
        return self.value[1]


@dataclass
class Grid:
    rounded: list[complex]
    rounded_set: set[complex]
    cubes: set[complex]
    nb_row: int
    nb_col: int

    @classmethod
    def build_from_string(cls, grid_str: Iterator[str]):
        cubes = set()
        rounded = []
        i = complex(0, 1)
        nb_row, nb_col = 0, 0
        for row, line in enumerate(grid_str):
            nb_col = len(line)
            for col, char in enumerate(line):
                if char == "#":
                    cubes.add(row * i + col)
                elif char == "O":
                    rounded.append(row * i + col)
            nb_row = row
        nb_row += 1
        return cls(rounded, set(rounded), cubes, nb_row, nb_col)

    def get_hash(self):
        hsh = ""
        for x in range(self.nb_row):
            for y in range(self.nb_col):
                hsh += "#" if x * complex(0, 1) + y in self.rounded_set else "."
        return hsh

    @staticmethod
    def get_key_cmp(direction: Direction):
        def key_cmp(a, b):
            return Grid.sort_direction(a, b, direction)

        return cmp_to_key(key_cmp)

    @staticmethod
    def sort_direction(a: complex, b: complex, direction: Direction):
        if a.imag < b.imag:
            return direction.ordering[0]
        elif a.imag > b.imag:
            return direction.ordering[1]
        elif a.real < b.real:
            return direction.ordering[2]
        elif a.real > b.real:
            return direction.ordering[3]
        return 0

    def process_direction(self, direction: Direction):
        self.rounded = sorted(self.rounded, key=Grid.get_key_cmp(direction))
        new_rounded_set = set()
        if direction == Direction.NORTH:
            self.process_north(new_rounded_set)
        elif direction == Direction.SOUTH:
            self.process_south(new_rounded_set)
        elif direction == Direction.EAST:
            self.process_east(new_rounded_set)
        else:
            self.process_west(new_rounded_set)
        self.rounded_set = new_rounded_set
        self.rounded = list(new_rounded_set)

    def process_north(self, new_rounded_set):
        for rock in self.rounded:
            res = rock - complex(0, 1)
            while (
                res.imag >= 0 and res not in self.cubes and res not in new_rounded_set
            ):
                res -= complex(0, 1)
            res += complex(0, 1)
            new_rounded_set.add(res)

    def process_south(self, new_rounded_set):
        for rock in self.rounded:
            res = rock + complex(0, 1)
            while (
                res.imag < self.nb_row
                and res not in self.cubes
                and res not in new_rounded_set
            ):
                res += complex(0, 1)
            res -= complex(0, 1)
            new_rounded_set.add(res)

    def process_east(self, new_rounded_set):
        for rock in self.rounded:
            res = rock + 1
            while (
                res.real < self.nb_col
                and res not in self.cubes
                and res not in new_rounded_set
            ):
                res += 1
            res -= 1
            new_rounded_set.add(res)

    def process_west(self, new_rounded_set):
        for rock in self.rounded:
            res = rock - 1
            while (
                res.real >= 0 and res not in self.cubes and res not in new_rounded_set
            ):
                res -= 1
            res += 1
            new_rounded_set.add(res)


class Day14(Day):
    FIRST_STAR_TEST_RESULT = 136
    SECOND_STAR_TEST_RESULT = 64

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(reflector_str: Iterator[str]):
        grid = Grid.build_from_string(reflector_str)
        grid.process_direction(Direction.NORTH)
        return sum(map(lambda rock: int(grid.nb_row - rock.imag), grid.rounded))

    @staticmethod
    def solve_2(reflector_str: Iterator[str]):
        nb_round = 1000000000
        grid = Grid.build_from_string(reflector_str)
        r = 0
        positions = {grid.get_hash(): (r, None)}
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
                r = nb_round - ((nb_round - r) % loop_size)
            else:
                positions[hsh] = (r, None)
            r += 1
        return sum(map(lambda rock: int(grid.nb_row - rock.imag), grid.rounded))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
