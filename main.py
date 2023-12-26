import argparse
import importlib
from pathlib import Path
from typing import Optional

from ddtrace import patch
from tabulate import tabulate

from day_factory.day_factory import DayFactory
from utils.input_retriever import retrieve_input

patch(logging=True)
import logging  # noqa: E402

FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s "
    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
    "- %(message)s"
)
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

NB_MAX_DAY = 25


# Get the number of Day implemented
def process_days(
    star: int,
    day: Optional[int],
    all_days: bool = False,
    download_input: bool = False,
    update_readme: bool = False,
):
    nb_day = 0
    if day is not None:
        nb_day = day
    else:
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
        retrieve_input(nb_day, Path("inputs/problems"))
        return

    # Print Header
    result_title = "Result"
    time_title = "Elapsed Time"
    headers = ["Day", "Star", result_title, f"{time_title}, ms"]
    table = []
    day_factory = DayFactory(nb_day)
    if not all_days and not update_readme:
        day = day_factory.get_day(nb_day)
        if star == 1 or star is None:
            table.extend(day.process_first_star())
        if star == 2 or star is None:
            table.extend(day.process_second_star())

    else:
        for i in range(1, nb_day + 1):
            day = day_factory.get_day(i)
            table.extend(day.process_first_star())
            day = day_factory.get_day(i)
            table.extend(day.process_second_star())
            if i < nb_day:
                table.append("")

    result_str = tabulate(table, tablefmt="github", headers=headers)
    # Display results in the console
    print(result_str)
    if update_readme:
        update_results_in_readme(result_str)


def update_results_in_readme(results: str):
    new_results_section_started = False
    with open("README.md", "r+") as file:
        lines = file.readlines()
        file.seek(0)  # Go back to the start of the file
        file.truncate(0)  # Clear the file
        for line in lines:
            if line.strip() == "## Results":
                new_results_section_started = True
                file.write(line)
                file.write(results + "\n")
            elif new_results_section_started and line.startswith("## "):
                new_results_section_started = False
            if not new_results_section_started:
                file.write(line)


if __name__ == "__main__":
    # Add arguments
    parser = argparse.ArgumentParser(description="Run Advent of Code 2023")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display debug log"
    )
    parser.add_argument(
        "-s", "--star", type=int, help="Star to process", default=None, choices=[1, 2]
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-a", "--all", action="store_true", help="Process all days", default=False
    )
    group.add_argument(
        "-i", "--input", action="store_true", help="Retrieve inputs", default=False
    )
    group.add_argument(
        "-r", "--readme", action="store_true", help="Retrieve inputs", default=False
    )
    group.add_argument("-d", "--day", type=int, help="Day to proceed", default=None)
    args = parser.parse_args()

    # Define logger
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)

    logger.info("Starting Advent of Code 2023")

    process_days(
        star=args.star,
        day=args.day,
        all_days=args.all,
        download_input=args.input,
        update_readme=args.readme,
    )
