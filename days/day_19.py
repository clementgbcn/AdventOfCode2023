import bisect
import re
import sys
from dataclasses import dataclass
from functools import reduce
from typing import Iterator

from day_factory.day import Day


class Day19(Day):
    FIRST_STAR_TEST_RESULT = 19114
    SECOND_STAR_TEST_RESULT = 167409079868000

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(workflows_str: Iterator[str]):
        pattern = re.compile(r"([a-z]+){(.+)}")
        step_pattern = re.compile(r"([a-z])([<>])(-?\d+):([a-zAR]+)")
        data_pattern = re.compile(r"([a-z])=(-?\d+)")
        workflows = {}
        while (l := next(workflows_str)) != "":
            data = pattern.findall(l)[0]
            name = data[0]
            workflows[name] = []
            for d in data[1].split(","):
                if "<" in d or ">" in d:
                    workflows[name].append(step_pattern.findall(d)[0])
                else:
                    workflows[name].append((d,))
        data = []
        while (l := next(workflows_str, None)) is not None:
            data.append({k[0]: int(k[1]) for k in data_pattern.findall(l)})
        count = 0
        for d in data:
            current_workflow = "in"
            while current_workflow not in ["A", "R"]:
                for step in workflows[current_workflow]:
                    if len(step) == 1:
                        current_workflow = step[0]
                        break
                    elif step[1] == ">":
                        if d[step[0]] > int(step[2]):
                            current_workflow = step[3]
                            break
                    elif step[1] == "<":
                        if d[step[0]] < int(step[2]):
                            current_workflow = step[3]
                            break
            if current_workflow == "A":
                count += sum(d.values())
        return count

    @staticmethod
    def solve_2(workflows_str: Iterator[str]):
        pattern = re.compile(r"([a-z]+){(.+)}")
        step_pattern = re.compile(r"([a-z])([<>])(-?\d+):([a-zAR]+)")
        workflows = {}
        while (l := next(workflows_str)) != "":
            data = pattern.findall(l)[0]
            name = data[0]
            workflows[name] = []
            for d in data[1].split(","):
                if "<" in d or ">" in d:
                    workflows[name].append(step_pattern.findall(d)[0])
                else:
                    workflows[name].append((d,))
        data = [({k: [(1, 4000)] for k in ["x", "m", "a", "s"]}, "in")]

        result = []
        while len(data) > 0:
            tuple_d = data.pop(0)
            d = tuple_d[0]
            current_workflow = tuple_d[1]
            if current_workflow == "R":
                continue
            if current_workflow == "A":
                result.append(d)
                continue
            for step in workflows[current_workflow]:
                if len(step) == 1:
                    data.append((d, step[0]))
                    break
                elif step[1] == ">":
                    greater_ranges = []
                    smaller_ranges = []
                    for r in d[step[0]]:
                        if r[0] > int(step[2]):
                            greater_ranges.append(r)
                        elif r[1] <= int(step[2]):
                            smaller_ranges.append(d)
                        else:
                            smaller_ranges.append((r[0], int(step[2])))
                            greater_ranges.append((int(step[2]) + 1, r[1]))
                            break
                    copy_d = d.copy()
                    copy_d[step[0]] = greater_ranges
                    data.append((copy_d, step[3]))
                    d[step[0]] = smaller_ranges
                elif step[1] == "<":
                    greater_ranges = []
                    smaller_ranges = []
                    for r in d[step[0]]:
                        if r[0] >= int(step[2]):
                            greater_ranges.append(r)
                        elif r[1] < int(step[2]):
                            smaller_ranges.append(d)
                        else:
                            smaller_ranges.append((r[0], int(step[2]) - 1))
                            greater_ranges.append((int(step[2]), r[1]))
                            break
                    copy_d = d.copy()
                    copy_d[step[0]] = smaller_ranges
                    data.append((copy_d, step[3]))
                    d[step[0]] = greater_ranges
        return sum(
            map(
                lambda d: reduce(
                    lambda x, y: x * y,
                    map(lambda k: sum(map(lambda r: r[1] - r[0] + 1, d[k])), d),
                ),
                result,
            )
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
