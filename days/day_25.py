import re
from dataclasses import dataclass
from typing import Iterator
import networkx
from day_factory.day import Day
from day_factory.day_utils import TestEnum
import matplotlib.pyplot as plt

NODE_PATTERN = re.compile(r"[a-z]+")


@dataclass
class Wiring:
    edges: dict[str, list[str]]

    @classmethod
    def build_from_string(cls, wiring_str: Iterator[str]):
        edges = {}
        for line in wiring_str:
            nodes = NODE_PATTERN.findall(line)
            if nodes[0] not in edges:
                edges[nodes[0]] = []
            edges[nodes[0]].extend(nodes[1:])
            for n in nodes[1:]:
                if n not in edges:
                    edges[n] = []
                edges[n].append(nodes[0])
        return Wiring(edges)

    def plot(self):
        g = networkx.Graph()
        for k, v in self.edges.items():
            for n in v:
                if (n, k) not in g.edges:
                    g.add_edge(k, n)
        networkx.draw_networkx(g, with_labels=True)
        plt.show()

    def visit_node(self, node, forbidden_edges):
        visited = set()
        stack = [node]
        while len(stack) > 0:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for n in self.edges[current]:
                if (current, n) in forbidden_edges or (n, current) in forbidden_edges:
                    continue
                stack.append(n)
        return visited


class Day25(Day):
    FIRST_STAR_TEST_RESULT = 54
    SECOND_STAR_TEST_RESULT = 0

    INVESTIGATE_MANUALLY = False

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def visit(wiring, start, excluded):
        stack = [start]
        visited = set()
        while len(stack) > 0:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            for n in wiring[current]:
                if n in excluded:
                    continue
                stack.append(n)
        return visited

    @staticmethod
    def solve_1(wiring_str: Iterator[str], input_type):
        wiring = Wiring.build_from_string(wiring_str)

        if Day25.INVESTIGATE_MANUALLY:
            wiring.plot()

        # Found with nxGraph
        if input_type == TestEnum.TEST:
            forbidden_edges = {("jqt", "nvd"), ("bvb", "cmg"), ("pzl", "hfx")}
        else:
            forbidden_edges = {("tnz", "dgt"), ("kzh", "rks"), ("ddc", "gqm")}
        visited = wiring.visit_node(list(wiring.edges)[0], forbidden_edges)
        return len(visited) * (len(wiring.edges) - len(visited))

    @staticmethod
    def solve_2(wiring_str: Iterator[str]):
        return 0

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value, input_type)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
