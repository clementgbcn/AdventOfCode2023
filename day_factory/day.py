import time
from abc import ABC, abstractmethod

from day_factory.day_utils import Star, TestEnum, UnknownStarException, Result
from utils.input_parser import InputParser


class Day(ABC):
    FIRST_STAR_TEST_RESULT = None
    SECOND_STAR_TEST_RESULT = None

    def __init__(self, day_inst):
        self.day_value = int(day_inst.__class__.__name__[-2:])

    @abstractmethod
    def solution_first_star(self, input_value, input_type):
        return 0

    @abstractmethod
    def solution_second_star(self, input_value, input_type):
        return 0

    def process_first_star(self):
        return self.process_star(Star.FIRST)

    def process_second_star(self):
        return self.process_star(Star.SECOND)

    def solution_star(self, star, input_value, input_type):
        if star == Star.FIRST:
            return self.solution_first_star(input_value, input_type=input_type)
        elif star == Star.SECOND:
            return self.solution_second_star(input_value, input_type=input_type)
        else:
            raise UnknownStarException(star)

    def process_star(self, star):
        # Run the test
        test_case = InputParser(self.day_value, TestEnum.TEST, star).get_iterator()
        test_result = self.solution_star(star, test_case, TestEnum.TEST)
        expected_result = (
            self.FIRST_STAR_TEST_RESULT
            if star == Star.FIRST
            else self.SECOND_STAR_TEST_RESULT
        )
        assert (
            expected_result == test_result
        ), f"Test failed for {star} star at Day {self.day_value}: {test_result} != {expected_result}"
        # Compute the result
        start_input_time = time.time_ns()
        input_case = InputParser(self.day_value, TestEnum.PROBLEM, star).get_iterator()
        input_result = self.solution_star(star, input_case, TestEnum.PROBLEM)
        end_input_time = (time.time_ns() - start_input_time) / 1000000
        return [
            [self.day_value, star, input_result, end_input_time],
        ]

    def get_result(self, star, input_type) -> Result:
        # Run the test
        test_case = InputParser(self.day_value, input_type, star).get_iterator()
        test_result = self.solution_star(star, test_case, input_type)
        return Result(self.day_value, input_type, star, test_result)
