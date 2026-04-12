import uuid

from validation.validation_expression import ValidationExpression


class RulePolicy(ValidationExpression):

    def __init__(self, rule, name=""):
        self.id = str(uuid.uuid4())[:8]
        self.rule = rule
        self.name = name

    def evaluate(self, context):
        return self.rule.evaluate(context)

    def __repr__(self):
        return f"RulePolicy({self.id}, {self.name})"
