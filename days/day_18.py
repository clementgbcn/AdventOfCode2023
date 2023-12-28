from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day

DIRECTION = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
HEX_DIR = ["R", "D", "L", "U"]


@dataclass
class DigPlan:
    orders: list[tuple[int, tuple[int, int]]]

    @classmethod
    def build_from_string(cls, dig_plan_str: Iterator[str], use_hexa: bool = False):
        orders = []
        for line in dig_plan_str:
            if use_hexa:
                hex_code = line.split(" ")[2]
                nb = int(hex_code[2:7], 16)
                d = DIRECTION[HEX_DIR[int(hex_code[7])]]
            else:
                split_line = line.split(" ")
                nb = int(split_line[1])
                d = DIRECTION[split_line[0]]
            orders.append((nb, d))
        return cls(orders)


@dataclass
class Trench:
    rows: dict[int, set[tuple[int, int, str, str]]]
    cols: dict[int, set[tuple[int, int, str, str]]]

    @classmethod
    def build_from_string(cls, dig_plan_str: Iterator[str], use_hexa: bool = False):
        orders = DigPlan.build_from_string(dig_plan_str, use_hexa).orders
        current_point = (0, 0)
        rows = {0: {(0, 0, None, None)}}
        cols = {0: {(0, 0, None, None)}}
        for i, order in enumerate(orders):
            nb = order[0]
            d = order[1]
            if d[0] == 0:
                prev_dir = orders[i - 1][1] if i - 1 >= 0 else None
                next_dir = orders[i + 1][1] if i + 1 < len(orders) else None
                if current_point[0] not in rows:
                    rows[current_point[0]] = set()
                if d[1] > 0:
                    rows[current_point[0]].add(
                        (
                            current_point[1],
                            current_point[1] + nb * d[1],
                            prev_dir,
                            next_dir,
                        )
                    )
                else:
                    rows[current_point[0]].add(
                        (
                            current_point[1] + nb * d[1],
                            current_point[1],
                            prev_dir,
                            next_dir,
                        )
                    )
                current_point = (current_point[0], current_point[1] + nb * d[1])
            else:
                prev_dir = orders[i - 1][1] if i - 1 >= 0 else None
                next_dir = orders[i + 1][1] if i + 1 < len(orders) else None
                if current_point[1] not in cols:
                    cols[current_point[1]] = set()
                if d[0] > 0:
                    cols[current_point[1]].add(
                        (
                            current_point[0],
                            current_point[0] + nb * d[0],
                            prev_dir,
                            next_dir,
                        )
                    )
                else:
                    cols[current_point[1]].add(
                        (
                            current_point[0] + nb * d[0],
                            current_point[0],
                            prev_dir,
                            next_dir,
                        )
                    )
                current_point = (current_point[0] + nb * d[0], current_point[1])
        rows[0].remove((0, 0, None, None))
        cols[0].remove((0, 0, None, None))
        # Add missing point in cols
        for row in rows:
            for col, values in cols.items():
                for elt in values:
                    if elt[0] <= row <= elt[1]:
                        for e in rows[row]:
                            if e[0] <= col <= e[1]:
                                break
                        else:
                            rows[row].add((col, col, None, None))
        return cls(rows, cols)

    def compute_volume(self):
        count = 0
        sorted_keys = sorted(self.rows.keys())
        sorted_cols_keys = sorted(self.cols.keys())
        for idx, row in enumerate(sorted_keys):
            indexes = sorted(self.rows[row], key=lambda x: x[0])
            count += indexes[0][1] - indexes[0][0] + 1
            is_in = True
            if (
                indexes[0][2] is not None
                and indexes[0][3] is not None
                and indexes[0][2] != indexes[0][3]
            ):
                is_in = False
            for i in range(len(indexes) - 1):
                if is_in:
                    count += indexes[i + 1][0] - indexes[i][1] - 1
                is_in = not is_in
                count += indexes[i + 1][1] - indexes[i + 1][0] + 1
                if (
                    indexes[i + 1][2] is not None
                    and indexes[i + 1][3] is not None
                    and indexes[i + 1][2] != indexes[i + 1][3]
                ):
                    is_in = not is_in
            if row + 1 in self.rows or idx == len(sorted_keys) - 1:
                continue
            nb_elem = 0
            previous = None
            for col in sorted_cols_keys:
                for elt in self.cols[col]:
                    if elt[0] <= row + 1 <= elt[1]:
                        if previous is None:
                            previous = col
                        else:
                            nb_elem += col - previous + 1
                            previous = None
                continue
            count += nb_elem * (sorted_keys[idx + 1] - row - 1)
        return count


class Day18(Day):
    FIRST_STAR_TEST_RESULT = 62
    SECOND_STAR_TEST_RESULT = 952408144115

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(dig_plan_str: Iterator[str]):
        trench = Trench.build_from_string(dig_plan_str)
        return trench.compute_volume()

    @staticmethod
    def solve_2(dig_plan_str: Iterator[str]):
        trench = Trench.build_from_string(dig_plan_str, use_hexa=True)
        return trench.compute_volume()

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
