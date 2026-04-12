from validation.binary_operator import BinaryOperator


class BinaryOperatorFactory:
    def evaluate(self, r1, r2, operator):
        match operator:
            case BinaryOperator.AND:
                return r1 and r2
            case BinaryOperator.OR:
                return r1 or r2
