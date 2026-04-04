from policy import Policy
from rule import Rule
from rule_service import RuleService


class PolicyService:
    def __init__(self):
        self.policies = {}
        self.rs = RuleService()

    def create_rule_policy(self, value, variable, comparison_operator):
        r1 = self.rs.create_rule(value, variable, comparison_operator)
        p1 = Policy(r1)
        self.policies[p1.id] = p1
        return p1.id

    def create_rule(self, value, variable, comparison_operator):
        return self.rs.create_rule(value, variable, comparison_operator)

    def create_policy_with_operator(self, p1, p2, binary_operator):
        p3 = Policy.from_policies_with_operator(p1, p2, binary_operator)
        self.policies[p3.id] = p3
        return p3.id

