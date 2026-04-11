import uuid

from coupon_system.enums import Comparator
from coupon_system.models.rule import Rule
from coupon_system.repositories.rule_repository import RuleRepository


class RuleService:
    def __init__(self, repository: RuleRepository):
        self._repository = repository

    def create_rule(self, variable: str, value, comparator: Comparator) -> Rule:
        rule_id = str(uuid.uuid4())[:8]
        rule = Rule(rule_id=rule_id, variable=variable, value=value, comparator=comparator)
        self._repository.save(rule)
        return rule

    def get_rule(self, rule_id: str) -> Rule | None:
        return self._repository.get(rule_id)
