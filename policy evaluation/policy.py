import uuid

from binary_operator_factory import BinaryOperatorFactory
from evaluation_expression import evlaution_express


class Policy(evlaution_express):
    pass


class RulePolicy(Policy):
    def __init__(self, rule):
        self.id = uuid.uuid4()
        self.rule = rule

    def evaluate(self, request):
        return self.rule.evaluate(request)


class CompositePolicy(Policy):
    def __init__(self, p1, p2, operator):
        self.id = uuid.uuid4()
        self.p1 = p1
        self.p2 = p2
        self.operator = operator
        self.bof = BinaryOperatorFactory()

    def evaluate(self, request):
        r1 = self.p1.evaluate(request)
        r2 = self.p2.evaluate(request)
        return self.bof.evaluate(r1, r2, self.operator)
