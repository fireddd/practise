from coupon_system.enums import CouponType


class Coupon:
    def __init__(self, coupon_id: str, coupon_code: str, value: float,
                 coupon_type: CouponType, min_cart_value: float, rule_id: str):
        self.coupon_id = coupon_id
        self.coupon_code = coupon_code
        self.value = value
        self.coupon_type = coupon_type
        self.min_cart_value = min_cart_value
        self.rule_id = rule_id

    def __repr__(self):
        return (f"Coupon(id={self.coupon_id}, code={self.coupon_code}, "
                f"value={self.value}, type={self.coupon_type.value}, "
                f"min_cart={self.min_cart_value}, rule={self.rule_id})")
