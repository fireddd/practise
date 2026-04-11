import uuid

from coupon_system.enums import CouponType
from coupon_system.models.cart import Cart
from coupon_system.models.coupon import Coupon
from coupon_system.models.rule_evaluation_context import RuleEvaluationContext
from coupon_system.calculators.discount_calculator_factory import DiscountCalculatorFactory
from coupon_system.repositories.coupon_repository import CouponRepository
from coupon_system.services.rule_service import RuleService


class CouponService:
    def __init__(self, rule_service: RuleService, repository: CouponRepository):
        self._rule_service = rule_service
        self._repository = repository

    def create_coupon(self, coupon_code: str, value: float, coupon_type: CouponType,
                      min_cart_value: float, rule_id: str) -> Coupon:
        coupon_id = str(uuid.uuid4())[:8]
        coupon = Coupon(
            coupon_id=coupon_id, coupon_code=coupon_code, value=value,
            coupon_type=coupon_type, min_cart_value=min_cart_value, rule_id=rule_id,
        )
        self._repository.save(coupon)
        return coupon

    def get_coupon(self, coupon_code: str) -> Coupon | None:
        return self._repository.get_by_code(coupon_code)

    def update_coupon(self, coupon_id: str, **kwargs) -> Coupon | None:
        coupon = self._repository.get(coupon_id)
        if coupon is None:
            return None
        for key, val in kwargs.items():
            if hasattr(coupon, key):
                setattr(coupon, key, val)
        self._repository.save(coupon)
        return coupon

    def delete_coupon(self, coupon_id: str) -> bool:
        return self._repository.delete(coupon_id)

    def evaluate_cart(self, cart: Cart, coupon_codes: list[str]) -> tuple[float, list[str]]:
        context = RuleEvaluationContext(amount=cart.amount, user_id=cart.user_id)
        running_total = cart.amount
        applied_coupons: list[str] = []

        for code in coupon_codes:
            coupon = self.get_coupon(code)
            if coupon is None:
                continue

            if running_total < coupon.min_cart_value:
                continue

            rule = self._rule_service.get_rule(coupon.rule_id)
            if rule is None or not rule.evaluate(context):
                continue

            calculator = DiscountCalculatorFactory.get_calculator(coupon.coupon_type)
            running_total = calculator.calculate(running_total, coupon.value)
            applied_coupons.append(code)

        return running_total, applied_coupons
