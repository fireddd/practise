import aerospike

from coupon_system.enums import Comparator
from coupon_system.models.rule import Rule


NAMESPACE = "coupon_system"
SET_NAME = "rules"


class RuleRepository:
    def __init__(self, client: aerospike.Client):
        self._client = client

    def save(self, rule: Rule) -> None:
        key = (NAMESPACE, SET_NAME, rule.rule_id)
        bins = {
            "rule_id": rule.rule_id,
            "variable": rule.variable,
            "value": rule.value,
            "comparator": rule.comparator.value,
        }
        self._client.put(key, bins)

    def get(self, rule_id: str) -> Rule | None:
        key = (NAMESPACE, SET_NAME, rule_id)
        try:
            _, _, bins = self._client.get(key)
        except aerospike.exception.RecordNotFound:
            return None
        return self._to_model(bins)

    @staticmethod
    def _to_model(bins: dict) -> Rule:
        return Rule(
            rule_id=bins["rule_id"],
            variable=bins["variable"],
            value=bins["value"],
            comparator=Comparator(bins["comparator"]),
        )
