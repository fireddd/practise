from coupon_system.enums import CouponType


class Promotion:
    def __init__(self, promotion_id: str, name: str, discount_type: CouponType,
                 discount_value: float, rule_id: str):
        self.promotion_id = promotion_id
        self.name = name
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.rule_id = rule_id

    def __repr__(self):
        return (f"Promotion(id={self.promotion_id}, name={self.name}, "
                f"type={self.discount_type.value}, value={self.discount_value}, "
                f"rule={self.rule_id})")
