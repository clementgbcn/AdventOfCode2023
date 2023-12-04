from dataclasses import dataclass

from day_factory.day import Day
from utils.utils import extract_int


@dataclass
class Card:
    card_id: int
    winning_nb: set[int]
    numbers: list[int]

    @classmethod
    def build_from_string(cls, line):
        data = line.split(":")
        card_id = extract_int(data[0])[0]
        all_numbers = data[1]
        split_numbers = all_numbers.split("|")
        winning_nb = set(extract_int(split_numbers[0]))
        numbers = list(extract_int(split_numbers[1]))
        return cls(card_id=card_id, winning_nb=winning_nb, numbers=numbers)

    def get_nb_matches(self) -> int:
        return len(list(filter(lambda x: x in self.winning_nb, self.numbers)))

    def compute_point(self) -> int:
        nb_matches = self.get_nb_matches()
        return pow(2, nb_matches - 1) if nb_matches > 0 else 0


class Day04(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(cards: list[str]):
        return sum(map(lambda x: Card.build_from_string(x).compute_point(), cards))

    @staticmethod
    def solve_2(cards: list[str]):
        stack = []
        total = 0
        for card_str in cards:
            nb_cards = stack.pop(0) if len(stack) > 0 else 1
            total += nb_cards
            nb_matches = Card.build_from_string(card_str).get_nb_matches()
            for i in range(nb_matches):
                if i < len(stack):
                    stack[i] += nb_cards
                else:
                    stack.append(1 + nb_cards)
        return total

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
