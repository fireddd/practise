from validation.comparison_operator import ComparisonOperator


class ComparisonOperatorFactory:
    def evaluate(self, saved, current, operator):
        match operator:
            case ComparisonOperator.EQ:
                return current == saved
            case ComparisonOperator.NEQ:
                return current != saved
            case ComparisonOperator.GT:
                return current > saved
            case ComparisonOperator.GTE:
                return current >= saved
            case ComparisonOperator.LT:
                return current < saved
            case ComparisonOperator.LTE:
                return current <= saved
