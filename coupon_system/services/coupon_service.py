import uuid

from coupon_system.enums import CouponType
from coupon_system.models.cart import Cart
from coupon_system.models.coupon import Coupon
from coupon_system.models.rule_evaluation_context import RuleEvaluationContext
from coupon_system.calculators.discount_calculator_factory import DiscountCalculatorFactory
from coupon_system.services.rule_service import RuleService


class CouponService:
    def __init__(self, rule_service: RuleService):
        self._coupons: dict[str, Coupon] = {}
        self._code_index: dict[str, str] = {}  # coupon_code -> coupon_id
        self._rule_service = rule_service

    def create_coupon(self, coupon_code: str, value: float, coupon_type: CouponType,
                      min_cart_value: float, rule_id: str) -> Coupon:
        coupon_id = str(uuid.uuid4())[:8]
        coupon = Coupon(
            coupon_id=coupon_id, coupon_code=coupon_code, value=value,
            coupon_type=coupon_type, min_cart_value=min_cart_value, rule_id=rule_id,
        )
        self._coupons[coupon_id] = coupon
        self._code_index[coupon_code] = coupon_id
        return coupon

    def get_coupon(self, coupon_code: str) -> Coupon | None:
        coupon_id = self._code_index.get(coupon_code)
        if coupon_id is None:
            return None
        return self._coupons.get(coupon_id)

    def update_coupon(self, coupon_id: str, **kwargs) -> Coupon | None:
        coupon = self._coupons.get(coupon_id)
        if coupon is None:
            return None
        for key, val in kwargs.items():
            if hasattr(coupon, key):
                setattr(coupon, key, val)
        return coupon

    def delete_coupon(self, coupon_id: str) -> bool:
        coupon = self._coupons.pop(coupon_id, None)
        if coupon is None:
            return False
        self._code_index.pop(coupon.coupon_code, None)
        return True

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
