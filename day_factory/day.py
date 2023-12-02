import time
from abc import ABC, abstractmethod

from day_factory.day_utils import Star, TestEnum, UnknownStarException
from utils.input_parser import InputParser


class Day(ABC):
    def __init__(self, day_inst):
        self.day_value = int(day_inst.__class__.__name__[-2:])

    @abstractmethod
    def solution_first_star(self, input_value, input_type):
        return 0

    @abstractmethod
    def solution_second_star(self, input_value, input_type):
        return 0

    def process_first_star(self):
        self.process_star(Star.FIRST)

    def process_second_star(self):
        self.process_star(Star.SECOND)

    def solution_star(self, star, input_value, input_type):
        if star == Star.FIRST:
            return self.solution_first_star(input_value, input_type=input_type)
        elif star == Star.SECOND:
            return self.solution_second_star(input_value, input_type=input_type)
        else:
            raise UnknownStarException(star)

    def process_star(self, star):
        start_test_time = time.time_ns()
        test_case = InputParser(
            self.day_value, TestEnum.TEST.value, star
        ).get_iterator()
        test_result = self.solution_star(star, test_case, TestEnum.TEST)
        end_test_time = (time.time_ns() - start_test_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tExample\t\t{test_result:>16}\t|\t{end_test_time:>6}ms"
        )
        start_input_time = time.time_ns()
        input_case = InputParser(
            self.day_value, TestEnum.INPUT.value, star
        ).get_iterator()
        input_result = self.solution_star(star, input_case, TestEnum.INPUT)
        end_input_time = (time.time_ns() - start_input_time) / 1000000
        print(
            f"{self.day_value:>3}\t\t{star}\t\tProblem\t\t{input_result:>16}\t|\t{end_input_time:>6}ms"
        )
