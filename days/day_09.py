from dataclasses import dataclass
from functools import reduce
from typing import Iterator

from day_factory.day import Day
from utils.utils import extract_int


@dataclass
class Sequence:
    seq: list[int]
    history: list[list[int]]

    @classmethod
    def build_from_string(cls, seq_str: str):
        seq = extract_int(seq_str)
        history = [seq]
        while any(map(lambda v: v != 0, history[-1])):
            history.append(
                [
                    history[-1][i + 1] - history[-1][i]
                    for i in range(len(history[-1]) - 1)
                ]
            )
        return cls(seq, history)


class Day09(Day):
    FIRST_STAR_TEST_RESULT = 114
    SECOND_STAR_TEST_RESULT = 2

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(sequences: Iterator[str]):
        return sum(
            map(
                lambda sequence: reduce(
                    lambda a, b: a + b, map(lambda h: h[-1], sequence.history[::-1])
                ),
                map(lambda seq_str: Sequence.build_from_string(seq_str), sequences),
            )
        )

    @staticmethod
    def solve_2(sequences: Iterator[str]):
        return sum(
            map(
                lambda sequence: reduce(
                    lambda a, b: b - a, map(lambda h: h[0], sequence.history[::-1])
                ),
                map(lambda seq_str: Sequence.build_from_string(seq_str), sequences),
            )
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
