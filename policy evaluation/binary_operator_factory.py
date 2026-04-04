from binary_operators import *
class BinaryOperatorFactory:
    def __init__(self):
        pass

    def evaluate(self, r1, r2, operator):
        match operator:
            case BinaryOperators.AND: return r1 and r2
            case BinaryOperators.OR: return r1 or r2
            case _ : raise ValueError("Invalid type of operator")