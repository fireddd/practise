from coupon_system.enums import CouponType
from coupon_system.calculators.discount_calculator import DiscountCalculator
from coupon_system.calculators.flat_discount_calculator import FlatDiscountCalculator
from coupon_system.calculators.percentage_discount_calculator import PercentageDiscountCalculator


class DiscountCalculatorFactory:

    _calculators: dict[CouponType, DiscountCalculator] = {
        CouponType.FLAT: FlatDiscountCalculator(),
        CouponType.PERCENTAGE: PercentageDiscountCalculator(),
    }

    @staticmethod
    def get_calculator(coupon_type: CouponType) -> DiscountCalculator:
        calculator = DiscountCalculatorFactory._calculators.get(coupon_type)
        if calculator is None:
            raise ValueError(f"No calculator for coupon type: {coupon_type}")
        return calculator
