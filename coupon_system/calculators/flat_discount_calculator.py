from coupon_system.calculators.discount_calculator import DiscountCalculator


class FlatDiscountCalculator(DiscountCalculator):

    def calculate(self, current_amount: float, discount_value: float) -> float:
        return max(0, current_amount - discount_value)
