from pydantic import BaseModel


# --- Rules ---

class CreateRuleRequest(BaseModel):
    variable: str
    value: float | str
    comparator: str  # "EQ", "GTE", "LTE"


class RuleResponse(BaseModel):
    rule_id: str
    variable: str
    value: float | str
    comparator: str


# --- Coupons ---

class CreateCouponRequest(BaseModel):
    coupon_code: str
    value: float
    coupon_type: str  # "FLAT", "PERCENTAGE"
    min_cart_value: float
    rule_id: str


class UpdateCouponRequest(BaseModel):
    value: float | None = None
    min_cart_value: float | None = None


class CouponResponse(BaseModel):
    coupon_id: str
    coupon_code: str
    value: float
    coupon_type: str
    min_cart_value: float
    rule_id: str


# --- Promotions ---

class CreatePromotionRequest(BaseModel):
    name: str
    discount_type: str  # "FLAT", "PERCENTAGE"
    discount_value: float
    rule_id: str


class PromotionResponse(BaseModel):
    promotion_id: str
    name: str
    discount_type: str
    discount_value: float
    rule_id: str


# --- Cart ---

class EvaluateCartRequest(BaseModel):
    user_id: str
    amount: float
    coupon_codes: list[str]


class EvaluateCartResponse(BaseModel):
    original_amount: float
    final_amount: float
    applied_coupons: list[str]
