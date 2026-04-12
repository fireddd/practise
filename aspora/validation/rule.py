from validation.validation_expression import ValidationExpression
from validation.comparison_operator_factory import ComparisonOperatorFactory


class Rule(ValidationExpression):

    def __init__(self, variable, value, comparison_operator):
        self.variable = variable
        self.value = value
        self.comparison_operator = comparison_operator
        self._cof = ComparisonOperatorFactory()

    def evaluate(self, context):
        current_value = getattr(context, self.variable, None)
        if current_value is None:
            return True
        return self._cof.evaluate(self.value, current_value, self.comparison_operator)
