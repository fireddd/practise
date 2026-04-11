import uuid

from coupon_system.enums import CouponType
from coupon_system.models.promotion import Promotion
from coupon_system.models.rule_evaluation_context import RuleEvaluationContext
from coupon_system.calculators.discount_calculator_factory import DiscountCalculatorFactory
from coupon_system.repositories.promotion_repository import PromotionRepository
from coupon_system.services.rule_service import RuleService


class PromotionService:
    def __init__(self, rule_service: RuleService, repository: PromotionRepository):
        self._rule_service = rule_service
        self._repository = repository

    def create_promotion(self, name: str, discount_type: CouponType,
                         discount_value: float, rule_id: str) -> Promotion:
        promotion_id = str(uuid.uuid4())[:8]
        promotion = Promotion(
            promotion_id=promotion_id, name=name,
            discount_type=discount_type, discount_value=discount_value,
            rule_id=rule_id,
        )
        self._repository.save(promotion)
        return promotion

    def get_promotions(self) -> list[Promotion]:
        return self._repository.get_all()

    def apply_promotions(self, context: RuleEvaluationContext, amount: float) -> float:
        running_total = amount
        for promotion in self._repository.get_all():
            rule = self._rule_service.get_rule(promotion.rule_id)
            if rule is None or not rule.evaluate(context):
                continue
            calculator = DiscountCalculatorFactory.get_calculator(promotion.discount_type)
            running_total = calculator.calculate(running_total, promotion.discount_value)
        return running_total
