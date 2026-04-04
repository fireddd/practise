import uuid

from binary_operator_factory import BinaryOperatorFactory
from evaluation_expression import evlaution_express


class Policy(evlaution_express):

    def __init__(self, rule):
        self.id = uuid.uuid4()
        self.rule = rule

    # credit_score > 750 AND account_status == "active"
    # (age >= 18 AND country != "restricted") and  credit_score > 750
    # (kyc_verified == false)
    @classmethod
    def from_policies_with_operator(cls, p1, p2, binaryoperator):
        obj = object.__new__(cls)
        obj.id = uuid.uuid4()
        obj.rule = None
        obj.p1 = p1
        obj.p2 = p2
        obj.operator = binaryoperator
        obj.bof = BinaryOperatorFactory()
        return obj

    def evaluate(self, request):
        if(self.rule != None):
            return self.rule.evaluate(request)
        else:
            r1 = self.p1.evaluate(request)
            r2 = self.p2.evaluate(request)
            return self.bof.evaluate(r1, r2, self.operator)


