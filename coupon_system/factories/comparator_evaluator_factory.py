from coupon_system.enums import Comparator


class ComparatorEvaluatorFactory:

    @staticmethod
    def evaluate(comparator: Comparator, actual_value, expected_value) -> bool:
        if comparator == Comparator.EQ:
            return actual_value == expected_value
        elif comparator == Comparator.GTE:
            return actual_value >= expected_value
        elif comparator == Comparator.LTE:
            return actual_value <= expected_value
        else:
            raise ValueError(f"Unknown comparator: {comparator}")
