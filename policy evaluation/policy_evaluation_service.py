from policy import Policy
from policy_service import PolicyService


class PolicyEvalutaionService:
    def __init__(self):
        self.ps = PolicyService()

    def create_rule_policy(self, value, variable, comparison_operator):
        self.ps.create_rule_policy(value, variable, comparison_operator)
    def create_policy_via_rules(self, value, variable, comparison_operator):
        r1 = self.ps.create_rule(value=value, variable=variable, comparison_operator=comparison_operator)
        p1 = Policy(r1)
        self.ps.policies[p1.id] = p1
        return p1
    def create_policies_with_operator(self, p1, p2, operator):
        self.ps.create_policy_with_operator(p1, p2, operator)

    def evaluate(self, request):
        policies = self.ps.policies
        for policy in policies.values():
            if not policy.evaluate(request):
                return ("failed", policy.id)

        return ("success", "")