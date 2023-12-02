import logging
import urllib.request
from pathlib import Path
from urllib.request import Request

COOKIE_PATH = Path(".config/aoc/cookie")
URL_PATTERN = "https://adventofcode.com/2023/day/{}/input"


def retrieve_input(day: int, input_folder: Path) -> None:
    with open(Path.home() / COOKIE_PATH) as f:
        cookie = f.read().splitlines()[0]
    req = Request(URL_PATTERN.format(day))
    req.add_header("cookie", cookie)
    contents = urllib.request.urlopen(req).read()
    # check file exist before writing and stop if it does
    input_file = f"{day}-1.txt"
    if (input_folder / input_file).exists():
        logging.warning("Input file already exists. Stop here.")
        return
    with open(input_folder / input_file, "xb") as f:
        # Do not write last carriage return
        f.write(contents[:-1])
