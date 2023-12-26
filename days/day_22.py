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
    blocks: set[tuple[int, int, int]]

    @classmethod
    def build_from_string(cls, block_str: str):
        x1, y1, z1, x2, y2, z2 = extract_int(block_str)
        blocks = set(
            [
                (i, j, k)
                for i in range(x1, x2 + 1)
                for j in range(y1, y2 + 1)
                for k in range(z1, z2 + 1)
            ]
        )
        return cls(x1, y1, z1, x2, y2, z2, blocks)

    def copy(self):
        return Block(
            self.x1, self.y1, self.z1, self.x2, self.y2, self.z2, self.blocks.copy()
        )

    def move_down(self):
        self.z1 -= 1
        self.z2 -= 1
        self.blocks = set(
            map(lambda line: (line[0], line[1], line[2] - 1), list(self.blocks))
        )

    def __repr__(self):
        return f"{self.x1},{self.y1},{self.z1}~{self.x2},{self.y2},{self.z2}"


class Day22(Day):
    FIRST_STAR_TEST_RESULT = 5
    SECOND_STAR_TEST_RESULT = 7

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(blocks_str: Iterator[str]):
        blocks = list(map(Block.build_from_string, blocks_str))
        blocks = sorted(blocks, key=lambda b: b.z1)
        for i in range(len(blocks)):
            b = blocks[i]
            current_z = None
            while b.z1 > 1 and b.z1 != current_z:
                current_z = b.z1
                b_copy = b.copy()
                b_copy.move_down()
                for j, b2 in enumerate(blocks):
                    if i == j or b_copy.z2 < b2.z1:
                        continue
                    if len(b_copy.blocks.intersection(b2.blocks)) != 0:
                        break
                else:
                    b.move_down()
        block_removable = []
        blocks = sorted(blocks, key=lambda b: b.z1)
        for i in range(len(blocks)):
            can_be_remove = True
            for j in range(len(blocks)):
                if j == i:
                    continue
                b = blocks[j]
                if b.z1 == 1 or b.z2 < blocks[i].z1:
                    continue
                b_copy = b.copy()
                b_copy.move_down()
                for k, b2 in enumerate(blocks):
                    if k == j or k == i:
                        continue
                    if len(b_copy.blocks.intersection(b2.blocks)) != 0:
                        break
                else:
                    can_be_remove = False
                if not can_be_remove:
                    break
            if can_be_remove:
                block_removable.append(i)
        return len(block_removable)

    @staticmethod
    def solve_2(blocks_str: Iterator[str]):
        blocks = list(map(Block.build_from_string, blocks_str))
        blocks = sorted(blocks, key=lambda b: b.z1)
        for i in range(len(blocks)):
            b = blocks[i]
            current_z = None
            while b.z1 > 1 and b.z1 != current_z:
                current_z = b.z1
                b_copy = b.copy()
                b_copy.move_down()
                for j, b2 in enumerate(blocks):
                    if i == j or b_copy.z2 < b2.z1:
                        continue
                    if len(b_copy.blocks.intersection(b2.blocks)) != 0:
                        break
                else:
                    b.move_down()
        block_removable = []
        blocks = sorted(blocks, key=lambda b: b.z1)
        total = 0
        for i in range(len(blocks)):
            count = 0
            block_copy = [b.copy() for b in blocks]
            for j in range(len(block_copy)):
                if j == i:
                    continue
                b = block_copy[j]
                if b.z1 == 1 or b.z2 < blocks[i].z1:
                    continue
                b_copy = b.copy()
                b_copy.move_down()
                for k, b2 in enumerate(block_copy):
                    if j == k or k == i:
                        continue
                    if len(b_copy.blocks.intersection(b2.blocks)) != 0:
                        break
                else:
                    count += 1
                    block_copy[j] = b_copy
            if count > 0:
                block_removable.append(i)
                total += count
        return total

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
