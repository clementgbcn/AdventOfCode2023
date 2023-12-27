from typing import Iterator

from day_factory.day import Day


class Day23(Day):
    FIRST_STAR_TEST_RESULT = 94
    SECOND_STAR_TEST_RESULT = 154

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(forest_str: Iterator[str]):
        start = (0, 1)
        forest = set()
        slopes = {}
        height, width = 0, 0
        for i, line in enumerate(forest_str):
            height += 1
            width = len(line)
            for j, c in enumerate(line):
                if c == "#":
                    forest.add((i, j))
                elif c in ["^", "v", "<", ">"]:
                    slopes[(i, j)] = c
        stack = [([start], {start})]
        max_distance = 0
        while len(stack) > 0:
            current_path, current_visited = stack.pop()
            current_point = current_path[-1]
            if current_point in slopes:
                slope = slopes[current_point]
                next_point = current_point
                if slope == "^":
                    next_point = (current_point[0] - 1, current_point[1])
                elif slope == "v":
                    next_point = (current_point[0] + 1, current_point[1])
                elif slope == "<":
                    next_point = (current_point[0], current_point[1] - 1)
                elif slope == ">":
                    next_point = (current_point[0], current_point[1] + 1)
                if (
                    not (0 <= next_point[0] < height and 0 <= next_point[1] < width)
                    or next_point in forest
                    or next_point in current_visited
                ):
                    continue
                new_path = current_path + [next_point]
                new_visited = current_visited.union({next_point})
                stack.append((new_path, new_visited))
                continue
            if current_point == (height - 1, width - 2):
                max_distance = max(max_distance, len(current_path) - 1)
                continue
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_point = (current_point[0] + d[0], current_point[1] + d[1])
                if (
                    not (0 <= next_point[0] < height and 0 <= next_point[1] < width)
                    or next_point in forest
                    or next_point in current_visited
                ):
                    continue
                new_path = current_path + [next_point]
                new_visited = current_visited.union({next_point})
                stack.append((new_path, new_visited))
        return max_distance

    @staticmethod
    def solve_2(forest_str: Iterator[str]):
        start = (0, 1)
        forest = set()
        slopes = {}
        height, width = 0, 0
        for i, line in enumerate(forest_str):
            height += 1
            width = len(line)
            for j, c in enumerate(line):
                if c == "#":
                    forest.add((i, j))
                elif c in ["^", "v", "<", ">"]:
                    slopes[(i, j)] = c
        split = set()
        for i in range(height):
            for j in range(width):
                if (i, j) in forest:
                    continue
                nb = 0
                for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    p = (i + d[0], j + d[1])
                    if not (0 <= p[0] < height and 0 <= p[1] < width) or p in forest:
                        continue
                    nb += 1
                if nb > 2:
                    split.add((i, j))
        edges = {}
        end = (height - 1, width - 2)
        start_neighbor, target = None, None
        start_distance, end_distance = 0, 0
        for s in split:
            stack = [(s, 0)]
            visited = set()
            edges[s] = []
            while len(stack) > 0:
                top = stack.pop()
                current_point = top[0]
                visited.add(current_point)
                distance = top[1]
                if current_point != s and current_point in split:
                    edges[s].append((current_point, distance))
                    continue
                if current_point == start:
                    start_neighbor = s
                    start_distance = distance
                    continue
                if current_point == end:
                    target = s
                    end_distance = distance
                    continue
                for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    next_point = (current_point[0] + d[0], current_point[1] + d[1])
                    if (
                        not (0 <= next_point[0] < height and 0 <= next_point[1] < width)
                        or next_point in forest
                        or next_point in visited
                    ):
                        continue
                    stack.append((next_point, distance + 1))
        stack = [(start_neighbor, {start_neighbor}, start_distance)]
        max_distance = 0
        while len(stack) > 0:
            current_point, current_visited, distance = stack.pop()
            if current_point == target:
                max_distance = max(max_distance, distance + end_distance)
                continue
            for next_point in edges[current_point]:
                if next_point[0] in current_visited:
                    continue
                new_visited = current_visited.union({next_point[0]})
                stack.append((next_point[0], new_visited, distance + next_point[1]))
        return max_distance

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
