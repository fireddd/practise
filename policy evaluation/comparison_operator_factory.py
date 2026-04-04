from comparison_operators import *
class ComparisonOperatorFactory:
    def __init__(self):
        pass

    def evaluate(self, saved, current, operator):
        match operator:
            case ComparisonOperators.EQ: return saved == current
            case ComparisonOperators.LTE: return saved <= current
            case ComparisonOperators.GTE: return saved >= current
            case _ : raise ValueError("Invalid type of operator")
