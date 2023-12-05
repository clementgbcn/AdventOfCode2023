from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day
from utils.utils import extract_int


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        return self.start + self.length


@dataclass
class Almanac:
    map_names: list[str]
    maps: dict[str, dict[int, Range]]

    @classmethod
    def build_from_string(cls, almanac: Iterator[str]):
        map_names = []
        maps = {}
        current_map = {}
        for line in almanac:
            if "map" in line:
                map_names.append(line.split(" ")[0])
                continue
            elif line == "":
                if len(current_map) == 0:
                    continue
                maps[map_names[-1]] = current_map
                current_map = {}
            else:
                positions = extract_int(line)
                current_map[positions[1]] = Range(positions[0], positions[2])
        maps[map_names[-1]] = current_map
        return cls(map_names=map_names, maps=maps)


class Day05(Day):
    FIRST_STAR_TEST_RESULT = 35
    SECOND_STAR_TEST_RESULT = 46

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(almanac_str: Iterator[str]):
        seeds = extract_int(next(almanac_str))
        almanac = Almanac.build_from_string(almanac_str)
        next_values = []
        current_values = seeds
        for map_name in almanac.map_names:
            current_map = almanac.maps[map_name]
            for value in current_values:
                for source, dest_range in current_map.items():
                    if source <= value < source + dest_range.length:
                        next_values.append(value - source + dest_range.start)
                        break
                else:
                    next_values.append(value)
            current_values = next_values.copy()
            next_values = []
        return min(current_values)

    @staticmethod
    def solve_2(almanac_str: Iterator[str]):
        seeds = extract_int(next(almanac_str))
        seeds = list(map(lambda x: Range(x[0], x[1]), zip(seeds[::2], seeds[1::2])))
        almanac = Almanac.build_from_string(almanac_str)
        next_values = []
        current_values = seeds
        for map_name in almanac.map_names:
            current_map = almanac.maps[map_name]
            while len(current_values) > 0:
                current_range = current_values.pop(0)
                for source, dest_range in current_map.items():
                    if source <= current_range.start < source + dest_range.length:
                        if current_range.end <= source + dest_range.length:
                            # Everything is in the same current_range
                            next_values.append(
                                Range(
                                    current_range.start - source + dest_range.start,
                                    current_range.length,
                                )
                            )
                        else:
                            next_values.append(
                                Range(
                                    current_range.start - source + dest_range.start,
                                    source + dest_range.length - current_range.start,
                                )
                            )
                            current_values.append(
                                Range(
                                    source + dest_range.length,
                                    current_range.length
                                    - (
                                        source + dest_range.length - current_range.start
                                    ),
                                )
                            )
                        break
                    elif current_range.start < source < current_range.end:
                        if current_range.end <= source + dest_range.length:
                            next_values.append(
                                Range(dest_range.start, current_range.end - source)
                            )
                            current_values.append(
                                Range(current_range.start, source - current_range.start)
                            )
                        else:
                            next_values.append(
                                Range(dest_range.start, dest_range.length)
                            )
                            current_values.append(
                                Range(current_range.start, source - current_range.start)
                            )
                            current_values.append(
                                Range(
                                    current_range.end,
                                    current_range.end - source - dest_range.length,
                                )
                            )
                        break
                else:
                    next_values.append(current_range)
            current_values = next_values.copy()
            next_values = []
        # Get the minimum start value
        return min(map(lambda x: x.start, current_values))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
