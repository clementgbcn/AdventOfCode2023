from dataclasses import dataclass

from day_factory.day import Day
from utils.utils import extract_int


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length


class Day05(Day):
    FIRST_STAR_TEST_RESULT = 35
    SECOND_STAR_TEST_RESULT = 46

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(almanac: list[str]):
        seeds = extract_int(next(almanac))
        next(almanac)
        map_names = []
        maps = {}
        current_map = {}
        for line in almanac:
            if "map" in line:
                map_names.append(line.split(" ")[0])
                continue
            elif line == "":
                maps[map_names[-1]] = current_map
                current_map = {}
                continue
            else:
                positions = extract_int(line)
                current_map[positions[1]] = (positions[0], positions[2])
        maps[map_names[-1]] = current_map
        next_values = []
        current_values = seeds
        for map_name in map_names:
            current_map = maps[map_name]
            for value in current_values:
                for k, v in current_map.items():
                    if k <= value < k + v[1]:
                        next_values.append(value - k + v[0])
                        break
                else:
                    next_values.append(value)
            current_values = next_values.copy()
            next_values = []
        return min(current_values)

    @staticmethod
    def solve_2(almanac: list[str]):
        seeds = extract_int(next(almanac))
        ranges = []
        for i in range(len(seeds) // 2):
            ranges.append(Range(seeds[2 * i], seeds[2 * i + 1]))
        _ = next(almanac)
        map_names = []
        maps = {}
        current_map = {}
        for line in almanac:
            if "map" in line:
                map_names.append(line.split(" ")[0])
                continue
            elif line == "":
                maps[map_names[-1]] = current_map
                current_map = {}
                continue
            else:
                positions = extract_int(line)
                current_map[positions[1]] = (positions[0], positions[2])
        maps[map_names[-1]] = current_map
        next_values = []
        current_values = ranges
        for map_name in map_names:
            current_map = maps[map_name]
            while len(current_values) > 0:
                current_range = current_values.pop(0)
                for k, v in current_map.items():
                    if k <= current_range.start < k + v[1]:
                        if current_range.end <= k + v[1]:
                            # Everything is in the same current_range
                            next_values.append(
                                Range(
                                    current_range.start - k + v[0], current_range.length
                                )
                            )
                        else:
                            next_values.append(
                                Range(
                                    current_range.start - k + v[0],
                                    k + v[1] - current_range.start,
                                )
                            )
                            current_values.append(
                                Range(
                                    k + v[1],
                                    current_range.length
                                    - (k + v[1] - current_range.start),
                                )
                            )
                        break
                    elif current_range.start < k < current_range.end:
                        if current_range.end <= k + v[1]:
                            next_values.append(Range(v[0], current_range.end - k))
                            current_values.append(
                                Range(current_range.start, k - current_range.start)
                            )
                        else:
                            next_values.append(Range(v[0], v[1]))
                            current_values.append(
                                Range(current_range.start, k - current_range.start)
                            )
                            current_values.append(
                                Range(current_range.end, current_range.end - k - v[1])
                            )
                        break
                else:
                    next_values.append(current_range)
            current_values = next_values.copy()
            next_values = []
        return min(map(lambda x: x.start, current_values))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
