from abc import ABC, abstractmethod

from coupon_system.models.rule_evaluation_context import RuleEvaluationContext


class EvaluateExpression(ABC):

    @abstractmethod
    def evaluate(self, context: RuleEvaluationContext) -> bool:
        pass
