import uuid

from validation.validation_expression import ValidationExpression
from validation.binary_operator_factory import BinaryOperatorFactory


class CompositePolicy(ValidationExpression):

    def __init__(self, p1, p2, operator, name=""):
        self.id = str(uuid.uuid4())[:8]
        self.p1 = p1
        self.p2 = p2
        self.operator = operator
        self.name = name
        self._bof = BinaryOperatorFactory()

    def evaluate(self, context):
        r1 = self.p1.evaluate(context)
        r2 = self.p2.evaluate(context)
        return self._bof.evaluate(r1, r2, self.operator)

    def __repr__(self):
        return f"CompositePolicy({self.id}, {self.name}, {self.operator.name})"
