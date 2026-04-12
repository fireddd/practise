from validation.rule import Rule
from validation.rule_policy import RulePolicy
from validation.composite_policy import CompositePolicy
from exceptions import ValidationException


class ValidationService:
    def __init__(self):
        self._policies = {}
        self._global_policies = []
        self._tier_policies = {}

    def create_rule_policy(self, variable, value, comparison_operator, name=""):
        rule = Rule(variable, value, comparison_operator)
        policy = RulePolicy(rule, name=name)
        self._policies[policy.id] = policy
        return policy

    def create_composite_policy(self, p1, p2, binary_operator, name=""):
        policy = CompositePolicy(p1, p2, binary_operator, name=name)
        self._policies[policy.id] = policy
        return policy

    def register_global_policy(self, policy):
        self._global_policies.append(policy)

    def register_tier_policy(self, tier, policy):
        self._tier_policies[tier] = policy

    def evaluate(self, context):
        for policy in self._global_policies:
            if not policy.evaluate(context):
                return False, policy


        tier_policy = self._tier_policies.get(context.sender_tier)
        if tier_policy is not None:
            if not tier_policy.evaluate(context):
                return False, tier_policy

        return True, None
