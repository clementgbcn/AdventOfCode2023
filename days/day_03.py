from dataclasses import dataclass

from day_factory.day import Day


@dataclass
class Engine:
    symbols: dict
    numbers: dict
    line_length: int

    SPACE_SYMBOL = "."
    GEAR_SYMBOL = "*"

    @classmethod
    def build_from_map(cls, engine_map, only_gear):
        symbols = {}
        numbers = {}
        line_length = None
        for i, line in enumerate(engine_map):
            line_length = len(line)
            current_nb = None
            for j, char in enumerate(line):
                if char.isdigit():
                    current_nb = char if current_nb is None else current_nb + char
                else:
                    if current_nb is not None:
                        numbers[(i, j - 1)] = int(current_nb)
                        current_nb = None
                    if (not only_gear and char != cls.SPACE_SYMBOL) or (
                        only_gear and char == cls.GEAR_SYMBOL
                    ):
                        symbols[(i, j)] = []
            if current_nb is not None:
                numbers[(i, line_length - 1)] = int(current_nb)
        return cls(symbols, numbers, line_length)

    def get_part_numbers(self):
        for pos, number in self.numbers.items():
            number_length = len(str(number))
            value_added = False
            # Do not skip the position of the numbers since it adds complexity for a
            # small gain in performance
            for j in range(
                max(pos[1] - number_length, 0), min(pos[1] + 2, self.line_length)
            ):
                for i in range(pos[0] - 1, pos[0] + 2):
                    if (i, j) in self.symbols:
                        # There is only one value per symbol
                        value_added = True
                        self.symbols[(i, j)].append(number)
                        break
                if value_added:
                    break
        return self.symbols


class Day03(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(engine_map: list[str]):
        engine = Engine.build_from_map(engine_map, False)
        symbols = engine.get_part_numbers()
        return sum(map(sum, symbols.values()))

    @staticmethod
    def solve_2(engine_map: list[str]):
        engine = Engine.build_from_map(engine_map, True)
        symbols = engine.get_part_numbers()
        return sum(
            map(lambda x: x[0] * x[1], filter(lambda x: len(x) == 2, symbols.values()))
        )

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
