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
class Contraption:
    grid: list[str]

    def propagate_beam(self, beam: Beam):
        beams = [beam]
        tiles = {}
        while len(beams) > 0:
            b = beams.pop(0)
            if b.xy in tiles and b.dxdy in tiles[b.xy]:
                continue
            if b.xy not in tiles:
                tiles[b.xy] = set()
            tiles[b.xy].add(b.dxdy)
            b_nxt = b.get_nxt()
            if not 0 <= b_nxt.x < len(self.grid) or not 0 <= b_nxt.y < len(
                self.grid[0]
            ):
                # It is out of the grid
                continue
            nxt_tile = self.grid[b_nxt.x][b_nxt.y]
            if nxt_tile == ".":
                beams.append(b_nxt)
            elif nxt_tile == "/":
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
        return len(tiles) - 1


class Day16(Day):
    FIRST_STAR_TEST_RESULT = 46
    SECOND_STAR_TEST_RESULT = 51

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(contraption_str: Iterator[str]):
        contraption = Contraption(list(contraption_str))
        return contraption.propagate_beam(Beam(0, -1, 0, 1))

    @staticmethod
    def solve_2(contraption_str: Iterator[str]):
        contraption = Contraption(list(contraption_str))
        max_energy = 0
        for i in range(len(contraption.grid)):
            for j in [(-1, 1), (len(contraption.grid[0]), -1)]:
                max_energy = max(
                    max_energy, contraption.propagate_beam(Beam(i, j[0], 0, j[1]))
                )
        for j in range(len(contraption.grid[0])):
            for i in [(-1, 1), (len(contraption.grid), -1)]:
                max_energy = max(
                    max_energy, contraption.propagate_beam(Beam(i[0], j, i[1], 0))
                )
        return max_energy

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
