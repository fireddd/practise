import aerospike
from aerospike import predicates as p

from coupon_system.enums import CouponType
from coupon_system.models.coupon import Coupon


NAMESPACE = "coupon_system"
SET_NAME = "coupons"
CODE_INDEX = "coupon_code_idx"


class CouponRepository:
    def __init__(self, client: aerospike.Client):
        self._client = client
        self._ensure_index()

    def _ensure_index(self):
        try:
            self._client.index_string_create(
                NAMESPACE, SET_NAME, "coupon_code", CODE_INDEX,
            )
        except aerospike.exception.IndexFoundError:
            pass

    def save(self, coupon: Coupon) -> None:
        key = (NAMESPACE, SET_NAME, coupon.coupon_id)
        bins = {
            "coupon_id": coupon.coupon_id,
            "coupon_code": coupon.coupon_code,
            "value": coupon.value,
            "coupon_type": coupon.coupon_type.value,
            "min_cart_value": coupon.min_cart_value,
            "rule_id": coupon.rule_id,
        }
        self._client.put(key, bins)

    def get(self, coupon_id: str) -> Coupon | None:
        key = (NAMESPACE, SET_NAME, coupon_id)
        try:
            _, _, bins = self._client.get(key)
        except aerospike.exception.RecordNotFound:
            return None
        return self._to_model(bins)

    def get_by_code(self, coupon_code: str) -> Coupon | None:
        query = self._client.query(NAMESPACE, SET_NAME)
        query.where(p.equals("coupon_code", coupon_code))
        results = query.results()
        if not results:
            return None
        _, _, bins = results[0]
        return self._to_model(bins)

    def delete(self, coupon_id: str) -> bool:
        key = (NAMESPACE, SET_NAME, coupon_id)
        try:
            self._client.remove(key)
            return True
        except aerospike.exception.RecordNotFound:
            return False

    @staticmethod
    def _to_model(bins: dict) -> Coupon:
        return Coupon(
            coupon_id=bins["coupon_id"],
            coupon_code=bins["coupon_code"],
            value=bins["value"],
            coupon_type=CouponType(bins["coupon_type"]),
            min_cart_value=bins["min_cart_value"],
            rule_id=bins["rule_id"],
        )
