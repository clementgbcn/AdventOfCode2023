from functools import reduce
from typing import Iterator

from day_factory.day import Day


def compute_hash(step: str):
    return reduce(lambda x, y: (x + ord(y)) * 17 % 256, step, 0)


def find_lens_index(lenses, label):
    for i, kv in enumerate(lenses):
        if kv[0] == label:
            return i
    return None


class Day15(Day):
    FIRST_STAR_TEST_RESULT = 1320
    SECOND_STAR_TEST_RESULT = 145

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(sequences_str: Iterator[str]):
        sequences = next(sequences_str).split(",")
        return sum(map(lambda s: compute_hash(s), sequences))

    @staticmethod
    def solve_2(sequences_str: Iterator[str]):
        boxes = {}
        sequences = next(sequences_str).split(",")
        for step in sequences:
            if step[-1] == "-":
                label = step[:-1]
                h = compute_hash(label)
                lens_index = find_lens_index(boxes.get(h, []), label)
                if lens_index is not None:
                    del boxes[h][lens_index]
            else:
                split_step = step.split("=")
                label = split_step[0]
                value = int(split_step[1])
                h = compute_hash(label)
                lens_index = find_lens_index(boxes.get(h, []), label)
                if lens_index is not None:
                    boxes[h][lens_index] = (label, value)
                else:
                    boxes[h] = boxes.get(h, []) + [(label, value)]
        total = 0
        for box_idx, lenses in boxes.items():
            for lens_idx, kv in enumerate(lenses):
                total += (1 + box_idx) * (1 + lens_idx) * kv[1]
        return total

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
