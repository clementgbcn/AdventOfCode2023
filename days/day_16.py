import bisect
from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day


@dataclass
class Beam:
    x: int
    y: int
    dx: int
    dy: int

    @property
    def xy(self):
        return self.x, self.y

    @property
    def dxdy(self):
        return self.dx, self.dy

    def get_nxt(self):
        return Beam(self.x + self.dx, self.y + self.dy, self.dx, self.dy)

    def get_nxt_redirected(self, dx: int, dy: int):
        return Beam(self.x + self.dx, self.y + self.dy, dx, dy)


@dataclass
class SparseContraption:
    grid: dict[int, dict[int, str]]
    grid_t: dict[int, dict[int, str]]
    height: int
    width: int

    @classmethod
    def build_from_string(cls, contraption_str: Iterator[str]):
        full_grid = list(contraption_str)
        grid = {}
        for i in range(len(full_grid)):
            grid[i] = {}
            for j in range(len(full_grid[0])):
                if full_grid[i][j] != ".":
                    grid[i][j] = full_grid[i][j]
        grid_t = {}
        for j in range(len(full_grid[0])):
            grid_t[j] = {}
            for i in range(len(full_grid)):
                if full_grid[i][j] != ".":
                    grid_t[j][i] = grid[i][j] = full_grid[i][j]
        return cls(grid, grid_t, len(full_grid), len(full_grid[0]))

    def propagate_beam(self, beam: Beam):
        beams = [beam]
        bars = {}
        encountered = set()
        while len(beams) > 0:
            b = beams.pop(0)
            if b.xy in bars and b.dxdy in bars[b.xy]:
                continue
            if (
                b.x in self.grid
                and b.y in self.grid[b.x]
                and self.grid[b.x][b.y] in ["|", "-"]
            ):
                bars.setdefault(b.xy, set()).add(b.dxdy)
            else:
                encountered.add(b.xy)
            b_nxt = b.get_nxt()
            if not 0 <= b_nxt.x < self.height or not 0 <= b_nxt.y < self.width:
                # It is out of the grid
                continue
            if b_nxt.x not in self.grid or b_nxt.y not in self.grid[b_nxt.x]:
                if b.dx == 0 and b.dy == 1:
                    keys = list(self.grid[b.x].keys())
                    idx = bisect.bisect_right(keys, b.y)
                    high = keys[idx] if 0 <= idx < len(keys) else self.width
                    for j in range(b_nxt.y, high - 1):
                        encountered.add((b.x, j))
                    if high < self.width:
                        beams.append(Beam(b.x, high - 1, b.dx, b.dy))
                    else:
                        encountered.add((b.x, high - 1))
                if b.dx == 0 and b.dy == -1:
                    keys = list(self.grid[b.x].keys())
                    idx = bisect.bisect_left(keys, b.y) - 1
                    low = keys[idx] if 0 <= idx < len(keys) else -1
                    for j in range(b_nxt.y, low + 1, -1):
                        encountered.add((b.x, j))
                    if low > -1:
                        beams.append(Beam(b.x, low + 1, b.dx, b.dy))
                    else:
                        encountered.add((b.x, low + 1))
                if b.dx == 1 and b.dy == 0:
                    keys = list(self.grid_t[b.y].keys())
                    idx = bisect.bisect_right(keys, b.x)
                    high = keys[idx] if 0 <= idx < len(keys) else self.height
                    for i in range(b_nxt.x, high - 1):
                        encountered.add((i, b.y))
                    if high < self.height:
                        beams.append(Beam(high - 1, b.y, b.dx, b.dy))
                    else:
                        encountered.add((high - 1, b.y))
                if b.dx == -1 and b.dy == 0:
                    keys = list(self.grid_t[b.y].keys())
                    idx = bisect.bisect_left(keys, b.x) - 1
                    low = keys[idx] if 0 <= idx < len(keys) else -1
                    for i in range(b_nxt.x, low + 1, -1):
                        encountered.add((i, b.y))
                    if low > -1:
                        beams.append(Beam(low + 1, b.y, b.dx, b.dy))
                    else:
                        encountered.add((low + 1, b.y))
                continue
            nxt_tile = self.grid[b_nxt.x][b_nxt.y]
            if nxt_tile == "/":
                beams.append(b.get_nxt_redirected(-b.dy, -b.dx))
            elif nxt_tile == "\\":
                beams.append(b.get_nxt_redirected(b.dy, b.dx))
            elif nxt_tile == "|":
                beams += (
                    [b_nxt]
                    if b.dy == 0
                    else [b.get_nxt_redirected(k, 0) for k in [-1, 1]]
                )
            elif nxt_tile == "-":
                beams += (
                    [b_nxt]
                    if b.dx == 0
                    else [b.get_nxt_redirected(0, k) for k in [-1, 1]]
                )
        return len(bars) + len(encountered) - 1


class Day16(Day):
    FIRST_STAR_TEST_RESULT = 46
    SECOND_STAR_TEST_RESULT = 51

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(contraption_str: Iterator[str]):
        contraption = SparseContraption.build_from_string(contraption_str)
        return contraption.propagate_beam(Beam(0, -1, 0, 1))

    @staticmethod
    def solve_2(contraption_str: Iterator[str]):
        contraption = SparseContraption.build_from_string(contraption_str)
        max_energy = 0
        for i in range(contraption.height):
            for j in [(-1, 1), (contraption.height, -1)]:
                max_energy = max(
                    max_energy, contraption.propagate_beam(Beam(i, j[0], 0, j[1]))
                )
        for j in range(contraption.width):
            for i in [(-1, 1), (contraption.height, -1)]:
                max_energy = max(
                    max_energy, contraption.propagate_beam(Beam(i[0], j, i[1], 0))
                )
        return max_energy

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
