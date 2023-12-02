from dataclasses import dataclass
from functools import reduce

from day_factory.day import Day

DICES_IN_BAG = {"blue": 14, "green": 13, "red": 12}


@dataclass
class Draw:
    nb_dices: dict[str, int]

    @classmethod
    def from_string(cls, draw):
        draw_data = draw.split(", ")
        draw = {}
        for dice in draw_data:
            dice_data = dice.split(" ")
            draw[dice_data[1]] = int(dice_data[0])
        return Draw(nb_dices=draw)

    def is_possible(self):
        for color, nb_dices in self.nb_dices.items():
            if nb_dices > DICES_IN_BAG[color]:
                return False
        return True


@dataclass
class Game:
    game_id: int
    draws: list[Draw]

    @classmethod
    def from_string(cls, game):
        data = game.split(": ")
        game_id = int(data[0].split(" ")[1])
        draws = list(map(lambda x: Draw.from_string(x), data[1].split("; ")))
        return cls(game_id=game_id, draws=draws)

    def is_possible(self):
        for draw in self.draws:
            if not draw.is_possible():
                return False
        return True

    def get_id_if_possible(self):
        return self.game_id if self.is_possible() else 0

    def get_power(self):
        power = {"blue": 0, "green": 0, "red": 0}
        for draw in self.draws:
            for color, nb_dices in draw.nb_dices.items():
                power[color] = max(power[color], nb_dices)
        return reduce(lambda x, y: x * y, power.values())


class Day02(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve_1(games: list[str]):
        return sum(map(lambda game: Game.from_string(game).get_id_if_possible(), games))

    @staticmethod
    def solve_2(games):
        return sum(map(lambda game: Game.from_string(game).get_power(), games))

    def solution_first_star(self, input_value, input_type):
        return self.solve_1(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
