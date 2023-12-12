from dataclasses import dataclass
from typing import Iterator, Tuple

from day_factory.day import Day
from utils.utils import extract_int


@dataclass
class Record:
    springs: str
    arrangements: list[int]

    @classmethod
    def build_from_str(cls, record_str: str, expansion: int = 1):
        split_record = record_str.split(" ")
        springs = "?".join([split_record[0]] * expansion)
        arrangements = extract_int(split_record[1]) * expansion
        return cls(springs, arrangements)

    def get_nb_arrangement(self):
        return Record.get_nb_arrangement_with_cache(self.springs, self.arrangements, {})

    @staticmethod
    def get_nb_arrangement_with_cache(
        springs: str,
        arrangements: list[int],
        cache: dict[str, dict[Tuple[int, ...], int]],
    ):
        # Check the cache
        if springs in cache and tuple(arrangements) in cache[springs]:
            return cache[springs][tuple(arrangements)]
        # Quick returns
        if len(springs) == 0:
            return 1 if len(arrangements) == 0 else 0
        if len(arrangements) == 0:
            return 1 if all(map(lambda s: s != "#", springs)) else 0
        if sum(arrangements) + len(arrangements) - 1 > len(springs):
            return 0
        # Dichotomy
        res = 0
        if springs[0] == ".":
            res = Record.get_nb_arrangement_with_cache(springs[1:], arrangements, cache)
        elif springs[0] == "#" and all(
            map(lambda s: s != ".", springs[: arrangements[0]])
        ):
            # All the next values cannot be a "."
            if len(springs) < arrangements[0]:
                res = 0
            elif arrangements[0] == len(springs):
                res = 1 if len(arrangements) == 1 else 0
            elif springs[arrangements[0]] != "#":
                res = Record.get_nb_arrangement_with_cache(
                    springs[arrangements[0] + 1 :], arrangements[1:], cache
                )
        elif springs[0] == "?":
            # It is a ?
            # Two choices: it could be a spring or not
            new_list = springs[1:] if len(springs) > 1 else ""
            res += Record.get_nb_arrangement_with_cache(
                "." + new_list, arrangements, cache
            )
            res += Record.get_nb_arrangement_with_cache(
                "#" + new_list, arrangements, cache
            )
        # Update the cache
        if springs not in cache:
            cache[springs] = {}
        cache[springs][tuple(arrangements)] = res
        return res


class Day12(Day):
    FIRST_STAR_TEST_RESULT = 21
    SECOND_STAR_TEST_RESULT = 525152

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(records_str: Iterator[str]):
        return sum(
            map(
                lambda record: Record.build_from_str(record).get_nb_arrangement(),
                records_str,
            )
        )

    @staticmethod
    def solve_2(records_str: Iterator[str]):
        return sum(
            map(
                lambda record: Record.build_from_str(record, 5).get_nb_arrangement(),
                records_str,
            )
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
