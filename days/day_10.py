from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Iterator

from day_factory.day import Day
from utils.utils import extract_int


class Tiles(Enum):
    NS = "|", {
        (-1, 0): {"a": [(0, -1)], "b": [(0, 1)]},
        (1, 0): {"a": [(0, 1)], "b": [(0, -1)]},
    }
    EW = "-", {
        (0, -1): {"a": [(1, 0)], "b": [(-1, 0)]},
        (0, 1): {"a": [(-1, 0)], "b": [(1, 0)]},
    }
    NE = "L", {
        (-1, 0): {"a": [(1, 0), (0, -1)], "b": []},
        (0, 1): {"a": [], "b": [(1, 0), (0, -1)]},
    }
    NW = "J", {
        (-1, 0): {"a": [], "b": [(0, 1), (1, 0)]},
        (0, -1): {"a": [(0, 1), (1, 0)], "b": []},
    }
    SW = "7", {
        (1, 0): {"a": [(0, 1), (-1, 0)], "b": []},
        (0, -1): {"a": [], "b": [(0, 1), (-1, 0)]},
    }
    SE = "F", {
        (1, 0): {"a": [], "b": [(-1, 0), (0, -1)]},
        (0, 1): {"a": [(-1, 0), (0, -1)], "b": []},
    }
    GROUND = ".", {}
    START = "S", {(1, 0): {}, (0, 1): {}, (-1, 0): {}, (0, -1): {}}

    @property
    def code(self):
        return self.value[0]

    @property
    def directions(self):
        return self.value[1]


TILES_MAPPING = {tile.code: tile for tile in Tiles}


@dataclass
class Area:
    area: list[list[Tiles]]
    start: tuple[int, int]

    @classmethod
    def build_from_string(cls, string):
        area = list(
            map(lambda line: list(map(lambda c: TILES_MAPPING[c], line[::])), string)
        )
        i, j = 0, 0
        found = False
        while i < len(area) and not found:
            j = 0
            while j < len(area[i]) and not found:
                if area[i][j] == Tiles.START:
                    found = True
                    break
                j += 1
            if found:
                break
            i += 1
        return cls(area, (i, j))


class Day10(Day):
    FIRST_STAR_TEST_RESULT = 8
    SECOND_STAR_TEST_RESULT = 4

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(desert: Iterator[str]):
        area_class = Area.build_from_string(desert)
        area = area_class.area
        # Found all directions
        current_positions = [area_class.start]
        path = {area_class.start}
        distance = 0
        while len(current_positions) > 0:
            next_positions = []
            for pos in current_positions:
                for dir in area[pos[0]][pos[1]].directions.keys():
                    x, y = dir[0], dir[1]
                    if (-x, -y) in area[pos[0] + x][pos[1] + y].directions and (
                        pos[0] + x,
                        pos[1] + y,
                    ) not in path:
                        next_positions.append((pos[0] + x, pos[1] + y))
                        path.add((pos[0] + x, pos[1] + y))
            current_positions = next_positions
            distance += 1
        return distance - 1

    @staticmethod
    def solve_2(desert: Iterator[str]):
        area_class = Area.build_from_string(desert)
        area = area_class.area
        # Found all directions
        current_positions = [(area_class.start[0], area_class.start[1])]
        path = {current_positions[0]}
        side_a = set()
        side_b = set()
        while len(current_positions) > 0:
            next_positions = []
            for pos in current_positions:
                for dir, side in area[pos[0]][pos[1]].directions.items():
                    x, y = dir[0], dir[1]
                    if (-x, -y) in area[pos[0] + x][pos[1] + y].directions and (
                        pos[0] + x,
                        pos[1] + y,
                    ) not in path:
                        # Add the external part of the path
                        for elt in side.get("a", []):
                            side_a.add((pos[0] + elt[0], pos[1] + elt[1]))
                        for elt in side.get("b", []):
                            side_b.add((pos[0] + elt[0], pos[1] + elt[1]))
                        next_positions.append((pos[0] + x, pos[1] + y))
                        path.add((pos[0] + x, pos[1] + y))
                        break
            current_positions = next_positions
        side_a.difference_update(path)
        side_b.difference_update(path)
        # Propagate the sides
        for i in range(len(area)):
            for j in range(len(area[i])):
                if (i, j) not in path and (i, j) not in side_a and (i, j) not in side_b:
                    encountered = set()
                    current_set = [(i, j)]
                    side_type = None
                    while len(current_set) > 0:
                        cur = current_set.pop()
                        if (
                            cur not in path
                            and cur not in side_a
                            and cur not in side_b
                            and cur not in encountered
                        ):
                            encountered.add(cur)
                            for x in [-1, 0, 1]:
                                for y in [-1, 0, 1]:
                                    if (
                                        0 <= cur[0] + x < len(area)
                                        and 0 <= cur[1] + y < len(area[0])
                                        and (x != 0 or y != 0)
                                    ):
                                        current_set.append((cur[0] + x, cur[1] + y))
                        elif cur in path:
                            continue
                        elif cur in side_a:
                            side_type = "a"
                        elif cur in side_b:
                            side_type = "b"
                    if side_type == "a":
                        side_a.update(encountered)
                    else:
                        side_b.update(encountered)
        return len(side_a) if (0, 0) in side_b else len(side_b)

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
