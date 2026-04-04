from comparison_operators import *
class ComparisonOperatorFactory:
    def __init__(self):
        pass

    def evaluate(self, saved, current, operator):
        match operator:
            case ComparisonOperators.EQ: return current == saved
            case ComparisonOperators.LTE: return current <= saved
            case ComparisonOperators.GTE: return current >= saved
            case _ : raise ValueError("Invalid type of operator")
