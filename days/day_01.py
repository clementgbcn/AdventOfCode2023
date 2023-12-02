from day_factory.day import Day

DIGIT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Day01(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def count_increment(weather):
        def get_digit_line(line):
            digits = list(filter(lambda y: y.isdigit(), line[::]))
            return int(f"{digits[0]}{digits[-1]}") if len(digits) > 0 else 0

        return sum(map(lambda x: get_digit_line(x), weather))

    @staticmethod
    def count_increment_2(weather):
        total = 0
        for line in weather:
            first, last = None, None
            idx = 0
            while idx < len(line[::]):
                c = line[::][idx]
                for k, v in DIGIT.items():
                    if c == k[0] and line[idx : idx + len(k)] == k:
                        c = v
                        break
                idx += 1
                if c.isdigit():
                    if first is None:
                        first = c
                    last = c
            total += int(f"{first}{last}")
        return total

    def solution_first_star(self, input_value, input_type):
        return self.count_increment(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.count_increment_2(input_value)
