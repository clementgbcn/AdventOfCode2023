import json
import sys
import os
import logging

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from day_factory.day_factory import DayFactory  # noqa: E402
from day_factory.day_utils import TestEnum, Star  # noqa: E402

logger = logging.getLogger(__name__)


def check_results(input_type: TestEnum) -> None:
    """Check the results of the simulation."""
    day_factory = DayFactory(25)
    file = f"results/{input_type.name.lower()}s.json"
    with open(file, "r") as f:
        data = json.load(f)
        for day_idx in data:
            for star, expected_result in data[day_idx].items():
                day = day_factory.get_day(int(day_idx))
                result = day.get_result(Star(int(star)), input_type).result
                assert (
                    result == expected_result
                ), f"Day{day_idx} for Star {star} with {input_type.name} input failed, {result} != {expected_result}"


def test_test_results():
    check_results(TestEnum.TEST)


def test_problem_results():
    if os.path.exists("inputs/problems"):
        check_results(TestEnum.PROBLEM)
    else:
        logger.info("No problem results to check")


if __name__ == "__main__":
    check_results(TestEnum.TEST)
    check_results(TestEnum.PROBLEM)
