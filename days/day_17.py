import sys
from typing import Iterator

from day_factory.day import Day
from day_factory.day_utils import Star
from utils.utils import insert_sorted


class HeatMap:
    def __init__(self, heat_map_str: Iterator[str], star: Star):
        self.heat_map = [[int(c) for c in line] for line in heat_map_str]
        self.height = len(self.heat_map)
        self.width = len(self.heat_map[0])
        self.constraint_func = (
            self.apply_constraint_1 if star == Star.FIRST else self.apply_constraint_2
        )

    def find_shorted_path(self):
        visited = set()
        distances = {(0, 0, 0, 0, 0): 0}
        to_visit = [(0, 0, 0, 0, 0)]
        to_visit_set = set(to_visit)
        to_visit_keys = [0]
        minimal_distance = sys.maxsize
        while len(to_visit) > 0:
            while to_visit_keys[-1] > minimal_distance:
                skipped = to_visit.pop()
                visited.add(skipped)
                to_visit_set.remove(skipped)
                to_visit_keys.pop()
                break
            current_point = to_visit.pop(0)
            current_distance = to_visit_keys.pop(0)
            to_visit_set.remove(current_point)
            # Find the smallest distance in the border
            if current_point is None or current_distance >= minimal_distance:
                break
            if (
                current_point[0] == self.height - 1
                and current_point[1] == self.width - 1
            ):
                minimal_distance = min(current_distance, minimal_distance)
            visited.add(current_point)
            self.add_neighbours(
                current_point,
                current_distance,
                visited,
                distances,
                to_visit,
                to_visit_set,
                to_visit_keys,
            )
        return minimal_distance

    def add_neighbours(
        self,
        current_point: tuple[int, int, int, int, int],
        current_distance: int,
        visited,
        distances,
        to_visit,
        to_visit_set,
        to_visit_keys,
    ):
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if d[0] == -current_point[2] and d[1] == -current_point[3]:
                continue
            nxt_point = (current_point[0] + d[0], current_point[1] + d[1])
            if not (0 <= nxt_point[0] < self.height and 0 <= nxt_point[1] < self.width):
                continue
            direction_strike = (
                1 if d != (current_point[2], current_point[3]) else 1 + current_point[4]
            )
            nxt_point, direction_strike = self.constraint_func(
                direction_strike, nxt_point, d, current_distance, visited, distances
            )
            if nxt_point is None:
                continue
            if (
                nxt_point[0],
                nxt_point[1],
                d[0],
                d[1],
                direction_strike,
            ) not in to_visit_set:
                insert_sorted(
                    to_visit,
                    to_visit_keys,
                    (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike),
                    key_func=lambda x: distances[x],
                )
                to_visit_set.add(
                    (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)
                )

    def apply_constraint_1(
        self,
        direction_strike: int,
        nxt_point: tuple[int, int],
        d: tuple[int, int],
        current_distance: int,
        visited: set[int],
        distances: dict[tuple[int, int, int, int, int], int],
    ):
        if (
            direction_strike > 3
            or (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike) in visited
            or (
                distances.get(
                    (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike),
                    sys.maxsize,
                )
                < current_distance + self.heat_map[nxt_point[0]][nxt_point[1]]
            )
        ):
            return None, None
        distances[(nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)] = (
            current_distance + self.heat_map[nxt_point[0]][nxt_point[1]]
        )
        return nxt_point, direction_strike

    def apply_constraint_2(
        self,
        direction_strike: int,
        nxt_point: tuple[int, int],
        d: tuple[int, int],
        current_distance: int,
        visited: set[int],
        distances: dict[tuple[int, int, int, int, int], int],
    ):
        if direction_strike > 10:
            return None, None
        accumulated_heat = 0
        updated_nxt_point = nxt_point
        while (
            direction_strike < 4
            and 0 <= updated_nxt_point[0] + d[0] < self.height
            and 0 <= updated_nxt_point[1] + d[1] < self.width
        ):
            accumulated_heat += self.heat_map[updated_nxt_point[0]][
                updated_nxt_point[1]
            ]
            updated_nxt_point = (
                updated_nxt_point[0] + d[0],
                updated_nxt_point[1] + d[1],
            )
            direction_strike += 1
        if (
            direction_strike < 4
            or (
                updated_nxt_point[0],
                updated_nxt_point[1],
                d[0],
                d[1],
                direction_strike,
            )
            in visited
            or (
                distances.get(
                    (
                        updated_nxt_point[0],
                        updated_nxt_point[1],
                        d[0],
                        d[1],
                        direction_strike,
                    ),
                    sys.maxsize,
                )
                < current_distance
                + self.heat_map[updated_nxt_point[0]][updated_nxt_point[1]]
                + accumulated_heat
            )
        ):
            return None, None
        distances[
            (updated_nxt_point[0], updated_nxt_point[1], d[0], d[1], direction_strike)
        ] = (
            current_distance
            + self.heat_map[updated_nxt_point[0]][updated_nxt_point[1]]
            + accumulated_heat
        )
        return updated_nxt_point, direction_strike


class Day17(Day):
    FIRST_STAR_TEST_RESULT = 102
    SECOND_STAR_TEST_RESULT = 94

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(heat_map_str: Iterator[str]):
        heat_map = HeatMap(heat_map_str, Star.FIRST)
        return heat_map.find_shorted_path()

    @staticmethod
    def solve_2(heat_map_str: Iterator[str]):
        heat_map = HeatMap(heat_map_str, Star.SECOND)
        return heat_map.find_shorted_path()

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
