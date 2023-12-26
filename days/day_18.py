from typing import Iterator

from day_factory.day import Day


class Day18(Day):
    FIRST_STAR_TEST_RESULT = 62
    SECOND_STAR_TEST_RESULT = 952408144115

    def __init__(self):
        super().__init__(self)

    DIRECTION = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    HEX_DIR = ["R", "D", "L", "U"]

    @staticmethod
    def solve_1_old(dig_plans_str: Iterator[str]):
        current_point = (0, 0)
        digged = {current_point}
        for line in dig_plans_str:
            split_line = line.split(" ")
            nb = int(split_line[1])
            d = Day18.DIRECTION[split_line[0]]
            for i in range(nb):
                current_point = (current_point[0] + d[0], current_point[1] + d[1])
                digged.add(current_point)
        visited = set()
        stack = [(1, 1)]
        while len(stack) > 0:
            current_point = stack.pop()
            if current_point in visited:
                continue
            visited.add(current_point)
            for d in Day18.DIRECTION.values():
                next_point = (current_point[0] + d[0], current_point[1] + d[1])
                if next_point not in digged and next_point not in visited:
                    stack.append(next_point)
        return len(visited) + len(digged)

    @staticmethod
    def solve_1(dig_plans_str: Iterator[str]):
        current_point = (0, 0)
        rows = {0: {(0, 0, None, None)}}
        orders = []
        for line in dig_plans_str:
            split_line = line.split(" ")
            nb = int(split_line[1])
            d = Day18.DIRECTION[split_line[0]]
            orders.append((nb, d))
        for i, order in enumerate(orders):
            nb = order[0]
            d = order[1]
            if d[0] == 0:
                prev_dir = orders[i - 1][1] if i - 1 >= 0 else None
                next_dir = orders[i + 1][1] if i + 1 < len(orders) else None
                rows[current_point[0]].remove(
                    (current_point[1], current_point[1], None, None)
                )
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
                for i in range(nb):
                    current_point = (current_point[0] + d[0], current_point[1] + d[1])
                    if current_point[0] not in rows:
                        rows[current_point[0]] = set()
                    rows[current_point[0]].add(
                        (current_point[1], current_point[1], None, None)
                    )
        count = 0
        rows[0].remove((0, 0, None, None))
        for row in sorted(rows.keys()):
            indexes = sorted(rows[row], key=lambda x: x[0])
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
        return count

    @staticmethod
    def solve_2(dig_plans_str: Iterator[str]):
        current_point = (0, 0)
        rows = {0: {(0, 0, None, None)}}
        orders = []
        for line in dig_plans_str:
            hex_code = line.split(" ")[2]
            nb = int(hex_code[2:7], 16)
            d = Day18.DIRECTION[Day18.HEX_DIR[int(hex_code[7])]]
            orders.append((nb, d))
        for i, order in enumerate(orders):
            nb = order[0]
            d = order[1]
            if d[0] == 0:
                prev_dir = orders[i - 1][1] if i - 1 >= 0 else None
                next_dir = orders[i + 1][1] if i + 1 < len(orders) else None
                rows[current_point[0]].remove(
                    (current_point[1], current_point[1], None, None)
                )
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
                for i in range(nb):
                    current_point = (current_point[0] + d[0], current_point[1] + d[1])
                    if current_point[0] not in rows:
                        rows[current_point[0]] = set()
                    rows[current_point[0]].add(
                        (current_point[1], current_point[1], None, None)
                    )
        count = 0
        rows[0].remove((0, 0, None, None))
        for row in sorted(rows.keys()):
            indexes = sorted(rows[row], key=lambda x: x[0])
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
        return count

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
