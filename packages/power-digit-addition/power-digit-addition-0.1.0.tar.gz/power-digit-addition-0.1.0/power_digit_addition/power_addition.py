class PowerNumDigitsAddition:

    def solve_expression(self, base: int, exp: int):
        return pow(base, exp)

    def digit_addition(self, result: int):
        digits_addition = 0
        if result > 0:
            while result != 0:
                mod = result % 10
                digits_addition += mod
                result = result // 10

            if digits_addition > 9:
                return self.digit_addition(digits_addition)
            else:
                return digits_addition
        else:
            return result
