from day import Day


class DayTemplate(Day):
    def __init__(self):
        super().__init__(self)

    @staticmethod
    def solve(input_value):
        return input_value

    @staticmethod
    def solve_2(input_value):
        return input_value

    def solution_first_star(self, input_value, input_type):
        return self.solve(input_value)

    def solution_second_star(self, input_value, input_type):
        return self.solve_2(input_value)
