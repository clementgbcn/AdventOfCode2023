import os
from pathlib import Path

from day_factory.day_utils import TestEnum


class InputParser:
    FOLDER = Path("inputs")

    def __init__(self, day, input_type, star):
        self.day = day
        self.input_type = input_type
        self.star = star
        self.filename = None
        self.filepath = None
        self.build_file_path()

    def build_file_path(self):
        input_type_folder = InputParser.FOLDER / Path(
            f"{self.input_type.name.lower()}s"
        )
        if self.input_type == TestEnum.TEST:
            self.filename = f"{self.day}-{self.star.value}.txt"
            self.filepath = input_type_folder / Path(self.filename)
            if os.path.exists(self.filepath):
                return
        self.filename = f"{self.day}.txt"
        self.filepath = input_type_folder / Path(self.filename)

    def get_iterator(self):
        with open(self.filepath, "r") as f:
            for line in f:
                yield line[:-1] if line[-1] == "\n" else line

    def get_table(self):
        res = []
        with open(self.filepath, "r") as f:
            for line in f:
                res.append(line[:-1] if line[-1] == "\n" else line)
        return res
