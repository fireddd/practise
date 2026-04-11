import uuid

from coupon_system.enums import Comparator
from coupon_system.models.rule import Rule


class RuleService:
    def __init__(self):
        self._rules: dict[str, Rule] = {}

    def create_rule(self, variable: str, value, comparator: Comparator) -> Rule:
        rule_id = str(uuid.uuid4())[:8]
        rule = Rule(rule_id=rule_id, variable=variable, value=value, comparator=comparator)
        self._rules[rule_id] = rule
        return rule

    def get_rule(self, rule_id: str) -> Rule | None:
        return self._rules.get(rule_id)
