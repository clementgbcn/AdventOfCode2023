from dataclasses import dataclass
from enum import Enum
from functools import reduce, cmp_to_key
from typing import Iterator

from day_factory.day import Day


class HandType(Enum):
    FIVE = 5
    FOUR = 4
    FULL = 3.5
    THREE = 3
    TWO_PAIRS = 2.5
    PAIR = 2
    HIGH_CARD = 1

    @staticmethod
    def wildcard_hand(hand_type, nb_j: int):
        return HandType(hand_type.value + nb_j)

    @staticmethod
    def get_hand_type(values: dict[str, int], joker=False):
        nb_j = 0
        if joker and "J" in values:
            nb_j = values["J"]
            del values["J"]
        if len(values) == 0:
            return HandType.FIVE
        max_nb_occurrence = max(values.values())
        nb_distinct_values = len(values.keys())
        if max_nb_occurrence == 3 and nb_distinct_values == 2 and nb_j == 0:
            return HandType.FULL
        elif max_nb_occurrence == 2 and nb_distinct_values == 3 and nb_j == 0:
            return HandType.TWO_PAIRS
        elif max_nb_occurrence == 2 and nb_distinct_values == 2 and nb_j == 1:
            return HandType.FULL
        else:
            return HandType.wildcard_hand(HandType(max_nb_occurrence), nb_j)


@dataclass
class Hand:
    bet: int
    hand_type: HandType
    cards: str
    joker: bool = False

    def get_card_value(self, card: str):
        if card == "A":
            return 14
        elif card == "K":
            return 13
        elif card == "Q":
            return 12
        elif card == "T":
            return 10
        elif card == "J":
            return 1 if self.joker else 11
        else:
            return int(card)

    @classmethod
    def build_from_string(cls, hand_str, joker=False):
        hand_split = hand_str.split(" ")
        cards, bet = hand_split[0], int(hand_split[1])
        values = {}
        for c in cards:
            values[c] = values.get(c, 0) + 1
        hand_type = HandType.get_hand_type(values, joker)
        return cls(bet=bet, hand_type=hand_type, cards=cards, joker=joker)

    def compare_high_card(self, other_hand):
        for i in range(len(self.cards)):
            card_value_1 = self.get_card_value(self.cards[i])
            card_value_2 = self.get_card_value(other_hand.cards[i])
            if card_value_1 < card_value_2:
                return -1
            elif card_value_1 > card_value_2:
                return 1
        return 0

    @staticmethod
    def compare(hand_1, hand_2):
        if hand_1.hand_type.value < hand_2.hand_type.value:
            return -1
        elif hand_1.hand_type.value > hand_2.hand_type.value:
            return 1
        else:
            return hand_1.compare_high_card(hand_2)


class Day07(Day):
    FIRST_STAR_TEST_RESULT = 6440
    SECOND_STAR_TEST_RESULT = 5905

    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(hands_str: Iterator[str]):
        hands = sorted(
            map(lambda x: Hand.build_from_string(x, False), hands_str),
            key=cmp_to_key(Hand.compare),
        )
        return sum(map(lambda x: (x[0] + 1) * x[1].bet, enumerate(hands)))

    @staticmethod
    def solve_2(hands_str: Iterator[str]):
        hands = sorted(
            map(lambda x: Hand.build_from_string(x, True), hands_str),
            key=cmp_to_key(Hand.compare),
        )
        return sum(map(lambda x: (x[0] + 1) * x[1].bet, enumerate(hands)))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
