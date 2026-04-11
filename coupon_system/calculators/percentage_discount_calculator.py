from coupon_system.calculators.discount_calculator import DiscountCalculator


class PercentageDiscountCalculator(DiscountCalculator):

    def calculate(self, current_amount: float, discount_value: float) -> float:
        return current_amount * (1 - discount_value / 100)
