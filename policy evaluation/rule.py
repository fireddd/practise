from comparison_operator_factory import ComparisonOperatorFactory
from evaluation_expression import evlaution_express


class Rule(evlaution_express):
    def __init__(self, variable, value, comparison_operator):
        self.variable = variable
        self.value = value
        self.comparison_operator = comparison_operator
        self.cof = ComparisonOperatorFactory()

    def evaluate(self, request):
        currentvalue = getattr(request, self.variable)
        if(currentvalue is None):
            return True
        savedvalue = self.value
        self.cof.evaluate(savedvalue, currentvalue, self.comparison_operator)