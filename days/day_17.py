import bisect
import sys
from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day


class Day17(Day):
    FIRST_STAR_TEST_RESULT = 102
    SECOND_STAR_TEST_RESULT = 94

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(heat_map_str: Iterator[str]):
        heat_map = [[int(c) for c in line] for line in heat_map_str]
        visited = set()
        distances = {(0, 0, 0, 0, 0): 0}
        to_visit = {(0, 0, 0, 0, 0)}
        end = 0
        while end < 6:
            current_point = None
            current_distance = None
            # Find the smallest distance in the border
            for k in to_visit:
                if current_distance is None or distances[k] < current_distance:
                    current_point = k
                    current_distance = distances[k]
            if current_point is None:
                break
            if (
                current_point[0] == len(heat_map) - 1
                and current_point[1] == len(heat_map[0]) - 1
            ):
                print("hit end", end)
                end += 1
            if len(visited) % 1000 == 0:
                print(len(visited), len(distances))
            visited.add(current_point)
            to_visit.remove(current_point)
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if d[0] == -current_point[2] and d[1] == -current_point[3]:
                    continue
                nxt_point = (current_point[0] + d[0], current_point[1] + d[1])
                if 0 <= nxt_point[0] < len(heat_map) and 0 <= nxt_point[1] < len(
                    heat_map[0]
                ):
                    direction_strike = (
                        1
                        if d != (current_point[2], current_point[3])
                        else 1 + current_point[4]
                    )
                    if direction_strike > 3:
                        continue
                    if (nxt_point, d, direction_strike) in visited:
                        continue
                    if (
                        distances.get(
                            (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike),
                            sys.maxsize,
                        )
                        < current_distance + heat_map[nxt_point[0]][nxt_point[1]]
                    ):
                        continue
                    distances[
                        (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)
                    ] = (current_distance + heat_map[nxt_point[0]][nxt_point[1]])
                    to_visit.add(
                        (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)
                    )
        minimal_distance = sys.maxsize
        for d in [(0, 1), (1, 0)]:
            for k in range(1, 4):
                minimal_distance = min(
                    minimal_distance,
                    distances.get(
                        (len(heat_map) - 1, len(heat_map[0]) - 1, d[0], d[1], k),
                        sys.maxsize,
                    ),
                )
        return minimal_distance

    @staticmethod
    def solve_2(heat_map_str: Iterator[str]):
        heat_map = [[int(c) for c in line] for line in heat_map_str]
        visited = set()
        distances = {(0, 0, 0, 0, 0): 0}
        to_visit = {(0, 0, 0, 0, 0)}
        end = 0
        while end < 20:
            current_point = None
            current_distance = None
            # Find the smallest distance in the border
            for k in to_visit:
                if current_distance is None or distances[k] < current_distance:
                    current_point = k
                    current_distance = distances[k]
            if current_point is None:
                break
            if (
                current_point[0] == len(heat_map) - 1
                and current_point[1] == len(heat_map[0]) - 1
            ):
                print("hit end", end)
                end += 1
            if len(visited) % 1000 == 0:
                print(len(visited), len(distances))
            visited.add(current_point)
            to_visit.remove(current_point)
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if d[0] == -current_point[2] and d[1] == -current_point[3]:
                    continue
                nxt_point = (current_point[0] + d[0], current_point[1] + d[1])
                if 0 <= nxt_point[0] < len(heat_map) and 0 <= nxt_point[1] < len(
                    heat_map[0]
                ):
                    direction_strike = (
                        1
                        if d != (current_point[2], current_point[3])
                        else 1 + current_point[4]
                    )
                    if direction_strike > 10:
                        continue
                    accumulated_heat = 0
                    while (
                        direction_strike < 4
                        and 0 <= nxt_point[0] + d[0] < len(heat_map)
                        and 0 <= nxt_point[1] + d[1] < len(heat_map[0])
                    ):
                        accumulated_heat += heat_map[nxt_point[0]][nxt_point[1]]
                        nxt_point = (nxt_point[0] + d[0], nxt_point[1] + d[1])
                        direction_strike += 1
                    if direction_strike < 4:
                        continue
                    if (nxt_point, d, direction_strike) in visited:
                        continue
                    if (
                        distances.get(
                            (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike),
                            sys.maxsize,
                        )
                        < current_distance
                        + heat_map[nxt_point[0]][nxt_point[1]]
                        + accumulated_heat
                    ):
                        continue
                    distances[
                        (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)
                    ] = (
                        current_distance
                        + heat_map[nxt_point[0]][nxt_point[1]]
                        + accumulated_heat
                    )
                    to_visit.add(
                        (nxt_point[0], nxt_point[1], d[0], d[1], direction_strike)
                    )
        minimal_distance = sys.maxsize
        for d in [(0, 1), (1, 0)]:
            for k in range(4, 11):
                minimal_distance = min(
                    minimal_distance,
                    distances.get(
                        (len(heat_map) - 1, len(heat_map[0]) - 1, d[0], d[1], k),
                        sys.maxsize,
                    ),
                )
        return minimal_distance

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
