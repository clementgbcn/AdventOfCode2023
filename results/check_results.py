import json

from day_factory.day_factory import DayFactory
from day_factory.day_utils import Star, TestEnum


def check_results(input_type: TestEnum) -> None:
    """Check the results of the simulation."""
    day_factory = DayFactory(24)
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


if __name__ == "__main__":
    check_results(TestEnum.TEST)
    check_results(TestEnum.PROBLEM)
