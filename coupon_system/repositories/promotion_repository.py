import aerospike

from coupon_system.enums import CouponType
from coupon_system.models.promotion import Promotion


NAMESPACE = "coupon_system"
SET_NAME = "promotions"


class PromotionRepository:
    def __init__(self, client: aerospike.Client):
        self._client = client

    def save(self, promotion: Promotion) -> None:
        key = (NAMESPACE, SET_NAME, promotion.promotion_id)
        bins = {
            "promotion_id": promotion.promotion_id,
            "name": promotion.name,
            "discount_type": promotion.discount_type.value,
            "discount_value": promotion.discount_value,
            "rule_id": promotion.rule_id,
        }
        self._client.put(key, bins)

    def get(self, promotion_id: str) -> Promotion | None:
        key = (NAMESPACE, SET_NAME, promotion_id)
        try:
            _, _, bins = self._client.get(key)
        except aerospike.exception.RecordNotFound:
            return None
        return self._to_model(bins)

    def get_all(self) -> list[Promotion]:
        results = []
        scan = self._client.scan(NAMESPACE, SET_NAME)
        scan.foreach(lambda record: results.append(self._to_model(record[2])))
        return results

    @staticmethod
    def _to_model(bins: dict) -> Promotion:
        return Promotion(
            promotion_id=bins["promotion_id"],
            name=bins["name"],
            discount_type=CouponType(bins["discount_type"]),
            discount_value=bins["discount_value"],
            rule_id=bins["rule_id"],
        )
