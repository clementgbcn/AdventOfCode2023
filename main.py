import argparse
import importlib
from pathlib import Path

from ddtrace import patch

from utils.input_retriever import retrieve_input

patch(logging=True)
import logging
from day_factory.day_factory import DayFactory

FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
    "- %(message)s"
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

NB_MAX_DAY = 24


# Get the number of Day implemented
def process_days(star: int, all_days: bool = False, download_input: bool = False):
    nb_day = 0
    for d in range(1, NB_MAX_DAY + 1):
        day_name = f"Day{d:02}"
        day_file_name = f"days.day_{d:02}"
        try:
            getattr(importlib.import_module(day_file_name), day_name)
            nb_day = d
        except ModuleNotFoundError:
            break
    if nb_day == 0:
        raise Exception("No Day implemented")

    if download_input:
        retrieve_input(nb_day, Path("inputs"))
        return

    # Print Header
    result_title = "Result"
    time_title = "Elapsed Time"
    print(f"Day\t\tStar\tTest Type\t{result_title:>16}\t|\t{time_title:>6}")
    separator = "-" * 70

    day_factory = DayFactory(nb_day)
    if not all_days:
        day = day_factory.get_day(nb_day)
        day.process_first_star() if star == 1 else day.process_second_star()
    else:
        for i in range(1, nb_day + 1):
            print(separator)
            day = day_factory.get_day(i)
            day.process_first_star()
            day = day_factory.get_day(i)
            day.process_second_star()
        print(separator)


if __name__ == "__main__":
    # Add arguments
    parser = argparse.ArgumentParser(description="Run Advent of Code 2023")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display debug log"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--star", type=int, help="Star to process", default=1, choices=[1, 2]
    )
    group.add_argument(
        "-a", "--all", action="store_true", help="Process all days", default=False
    )
    group.add_argument(
        "-i", "--input", action="store_true", help="Retrieve inputs", default=False
    )
    args = parser.parse_args()

    # Define logger
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    process_days(star=args.star, all_days=args.all, download_input=args.input)
