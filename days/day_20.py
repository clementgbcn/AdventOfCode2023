import math
from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional

from day_factory.day import Day
import matplotlib.pyplot as plt

import networkx as nx

from day_factory.day_utils import TestEnum


class FlipFlopState(Enum):
    ON = 1
    OFF = 2


class PulseState(Enum):
    LOW = 1
    HIGH = 2


@dataclass
class Pulse:
    source: Optional[str]
    destination: Optional[str]
    pulse_state: PulseState


class ModuleRouter:
    def __init__(self):
        self.modules = {}
        self.modules_connections = {}
        self.reverse_connections = {}
        self.sub_routers = []
        self.pulses = []
        self.nb_pulses = {PulseState.LOW: 0, PulseState.HIGH: 0}
        # Attributes for Part 2
        self.endpoint_triggered = False
        self.endpoint = "rx"
        self.monitor_state = PulseState.LOW

    def build_routing(self, routing_str: Iterator[str]):
        conjunctions = set()
        for line in routing_str:
            split = line.split(" -> ")
            module_name = split[0]
            connections = split[1].split(", ")
            if module_name.startswith(FlipFlop.PREFIX):
                self.add_module(FlipFlop(module_name[1:]), connections)
            elif module_name.startswith(Conjunction.PREFIX):
                self.add_module(Conjunction(module_name[1:]), connections)
                conjunctions.add(module_name[1:])
            elif module_name == Broadcaster.NAME:
                self.add_module(Broadcaster(), connections)
            else:
                self.add_module(BaseModule(module_name), connections)
        for k, connections in self.modules_connections.items():
            for connection in connections:
                if connection in conjunctions:
                    self.modules[connection].add_input(k)
        self.pulses = []

    def plot_graph(self):
        graph = nx.DiGraph(directed=True)
        edges = []
        for k, v in self.modules_connections.items():
            for connection in v:
                edges.append(
                    (
                        self.modules[k].get_full_name(),
                        self.modules[connection].get_full_name()
                        if connection in self.modules
                        else connection,
                    )
                )
        graph.add_edges_from(edges)
        options = {
            "node_color": "grey",
            "node_size": 100,
            "width": 1,
            "arrowstyle": "-|>",
            "arrowsize": 12,
        }
        nx.draw_networkx(graph, with_labels=True, arrows=True, **options)
        plt.show()

    def split_routing(self):
        for module_name in self.modules_connections[Broadcaster.NAME]:
            router = ModuleRouter()
            router.monitor_state = PulseState.HIGH
            visited = set()
            router.add_module(Broadcaster(), [module_name])
            stack = [module_name]
            while len(stack) > 0:
                current_module = stack.pop(0)
                if current_module in self.reverse_connections[self.endpoint]:
                    router.endpoint = current_module
                    continue
                if current_module in visited:
                    continue
                visited.add(current_module)
                module = self.modules[current_module]
                router.add_module(
                    module.copy(), self.modules_connections[current_module]
                )
                for connection in self.modules_connections[current_module]:
                    stack.append(connection)
            self.sub_routers.append(router)

    def add_module(self, module, connections):
        self.modules[module.name] = module
        self.modules_connections[module.name] = connections
        for connection in connections:
            self.reverse_connections.setdefault(connection, []).append(module.name)

    def push_button(self):
        self.pulses.append(Pulse(None, Broadcaster.NAME, PulseState.LOW))
        while len(self.pulses) > 0:
            pulse = self.pulses.pop(0)
            if pulse.destination is None:
                continue
            self.nb_pulses[pulse.pulse_state] += 1
            if (
                pulse.destination == self.endpoint
                and pulse.pulse_state == self.monitor_state
            ):
                self.endpoint_triggered = True
                continue
            if pulse.destination not in self.modules:
                continue
            output = self.modules[pulse.destination].consume(
                pulse.pulse_state, pulse.source
            )
            if output is None:
                continue
            for connection in self.modules_connections[pulse.destination]:
                self.pulses.append(Pulse(pulse.destination, connection, output))


class BaseModule:
    def __init__(self, name):
        self.name = name

    def copy(self):
        return BaseModule(self.name)

    def get_full_name(self):
        return self.name

    def consume(self, pulse: Pulse, from_module: str):
        return None


class FlipFlop(BaseModule):
    PREFIX = "%"

    def __init__(self, name):
        self.state = FlipFlopState.OFF
        super().__init__(name)

    def copy(self):
        return FlipFlop(self.name)

    def get_full_name(self):
        return f"{self.PREFIX}{self.name}"

    def consume(self, pulse: Pulse, from_module: str):
        if pulse == PulseState.LOW:
            if self.state == FlipFlopState.ON:
                self.state = FlipFlopState.OFF
                return PulseState.LOW
            else:
                self.state = FlipFlopState.ON
                return PulseState.HIGH


class Conjunction(BaseModule):
    PREFIX = "&"

    def __init__(self, name):
        self.states = {}
        super().__init__(name)

    def copy(self):
        c = Conjunction(self.name)
        c.states = {k: v for k, v in self.states.items()}
        return c

    def get_full_name(self):
        return f"{self.PREFIX}{self.name}"

    def add_input(self, module_name):
        self.states[module_name] = PulseState.LOW

    def consume(self, pulse: Pulse, from_module: str):
        self.states[from_module] = pulse
        if all(map(lambda s: s == PulseState.HIGH, self.states.values())):
            return PulseState.LOW
        else:
            return PulseState.HIGH


class Broadcaster(BaseModule):
    NAME = "broadcaster"

    def __init__(self):
        super().__init__(Broadcaster.NAME)

    def copy(self):
        return Broadcaster()

    def consume(self, pulse: Pulse, from_module: str):
        return pulse


class Day20(Day):
    FIRST_STAR_TEST_RESULT = 32000000
    SECOND_STAR_TEST_RESULT = 1

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(workflows_str: Iterator[str]):
        module_router = ModuleRouter()
        module_router.build_routing(workflows_str)
        for _ in range(1000):
            module_router.push_button()
        return (
            module_router.nb_pulses[PulseState.LOW]
            * module_router.nb_pulses[PulseState.HIGH]
        )

    @staticmethod
    def solve_2(workflows_str: Iterator[str], input_type):
        if input_type == TestEnum.TEST:
            return 1
        module_router = ModuleRouter()
        module_router.build_routing(workflows_str)
        module_router.split_routing()
        loop_indexes = []
        for router in module_router.sub_routers:
            i = 0
            while not router.endpoint_triggered:
                router.push_button()
                i += 1
            loop_indexes.append(i)
        return math.lcm(*loop_indexes)

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value, input_type)
