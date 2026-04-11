from coupon_system.enums import Comparator
from coupon_system.models.evaluate_expression import EvaluateExpression
from coupon_system.models.rule_evaluation_context import RuleEvaluationContext
from coupon_system.factories.comparator_evaluator_factory import ComparatorEvaluatorFactory


class Rule(EvaluateExpression):
    def __init__(self, rule_id: str, variable: str, value: float, comparator: Comparator):
        self.rule_id = rule_id
        self.variable = variable
        self.value = value
        self.comparator = comparator

    def evaluate(self, context: RuleEvaluationContext) -> bool:
        actual_value = getattr(context, self.variable)
        return ComparatorEvaluatorFactory.evaluate(self.comparator, actual_value, self.value)

    def __repr__(self):
        return f"Rule(id={self.rule_id}, {self.variable} {self.comparator.value} {self.value})"
