from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import Iterator

from day_factory.day import Day

from utils.utils import extract_int


@dataclass
class Block:
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    @classmethod
    def build_from_string(cls, block_str: str):
        x1, y1, z1, x2, y2, z2 = extract_int(block_str)
        return cls(x1, y1, z1, x2, y2, z2)

    def copy(self):
        return Block(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

    def move_down(self, nb):
        self.z1 -= nb
        self.z2 -= nb

    def __repr__(self):
        return f"{self.x1},{self.y1},{self.z1}~{self.x2},{self.y2},{self.z2}"

    def intersect(self, other):
        x_min = max(self.x1, other.x1)
        x_max = min(self.x2, other.x2)
        y_min = max(self.y1, other.y1)
        y_max = min(self.y2, other.y2)
        z_min = max(self.z1, other.z1)
        z_max = min(self.z2, other.z2)
        return x_min <= x_max and y_min <= y_max and z_min <= z_max

    def get_nb_falling_heigh(self, j, blocks, i):
        decrease_z = self.z1 - 1
        for k in reversed(range(j)):
            if k == i:
                continue
            if decrease_z == 0:
                break
            b2 = blocks[k]
            x_min = max(self.x1, b2.x1)
            x_max = min(self.x2, b2.x2)
            y_min = max(self.y1, b2.y1)
            y_max = min(self.y2, b2.y2)
            if x_min <= x_max and y_min <= y_max and self.z1 > b2.z2:
                decrease_z = min(decrease_z, self.z1 - b2.z2 - 1)
        return decrease_z

    @staticmethod
    def could_block_be_removed(i, blocks):
        for j in range(i + 1, len(blocks)):
            b = blocks[j]
            if b.z1 == 1 or b.z2 < blocks[i].z1:
                continue
            decrease_z = b.get_nb_falling_heigh(j, blocks, i)
            if decrease_z > 0:
                return False
        return True

    @staticmethod
    def compute_nb_falling_brick(i, blocks):
        total = 0
        block_copy = [b.copy() for b in blocks]
        for j in range(i + 1, len(block_copy)):
            b = block_copy[j]
            if b.z1 == 1 or b.z2 < blocks[i].z1:
                continue
            decrease_z = b.get_nb_falling_heigh(j, block_copy, i)
            total += 1 if decrease_z > 0 else 0
            b.move_down(decrease_z)
        return total

    @staticmethod
    def make_blocks_fall(blocks):
        blocks = sorted(blocks, key=lambda b: b.z1)
        for i in range(len(blocks)):
            b = blocks[i]
            decrease_z = b.get_nb_falling_heigh(i, blocks, None)
            b.move_down(decrease_z)
        return sorted(blocks, key=lambda b: b.z1)


class Day22(Day):
    FIRST_STAR_TEST_RESULT = 5
    SECOND_STAR_TEST_RESULT = 7

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(blocks_str: Iterator[str]):
        blocks = list(map(Block.build_from_string, blocks_str))
        blocks = Block.make_blocks_fall(blocks)
        with ProcessPoolExecutor() as executor:
            running_tasks = [
                executor.submit(Block.could_block_be_removed, i, blocks)
                for i in range(len(blocks))
            ]
            return len(list(filter(lambda v: v.result(), running_tasks)))

    @staticmethod
    def solve_2(blocks_str: Iterator[str]):
        blocks = list(map(Block.build_from_string, blocks_str))
        blocks = Block.make_blocks_fall(blocks)
        with ProcessPoolExecutor() as executor:
            running_tasks = [
                executor.submit(Block.compute_nb_falling_brick, i, blocks)
                for i in range(len(blocks))
            ]
            return sum(map(lambda v: v.result(), running_tasks))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
