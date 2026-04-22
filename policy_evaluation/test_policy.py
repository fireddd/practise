import unittest

from binary_operators import BinaryOperators
from comparison_operators import ComparisonOperators
from policy import RulePolicy, CompositePolicy
from request import request
from rule import Rule


class TestRulePolicy(unittest.TestCase):

    def test_rule_policy_pass(self):
        rule = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        policy = RulePolicy(rule)
        r = request(pay=60)
        self.assertTrue(policy.evaluate(r))

    def test_rule_policy_fail(self):
        rule = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        policy = RulePolicy(rule)
        r = request(pay=40)
        self.assertFalse(policy.evaluate(r))


class TestCompositePolicy(unittest.TestCase):

    def test_and_both_pass(self):
        r1 = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r2 = Rule(variable="account_status", value="ACTIVE", comparison_operator=ComparisonOperators.EQ)
        p1 = RulePolicy(r1)
        p2 = RulePolicy(r2)
        composite = CompositePolicy(p1, p2, BinaryOperators.AND)
        r = request(pay=60, account_status="ACTIVE")
        self.assertTrue(composite.evaluate(r))

    def test_and_one_fails(self):
        r1 = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r2 = Rule(variable="account_status", value="ACTIVE", comparison_operator=ComparisonOperators.EQ)
        p1 = RulePolicy(r1)
        p2 = RulePolicy(r2)
        composite = CompositePolicy(p1, p2, BinaryOperators.AND)
        r = request(pay=60, account_status="INACTIVE")
        self.assertFalse(composite.evaluate(r))

    def test_or_one_passes(self):
        r1 = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r2 = Rule(variable="loans", value=0, comparison_operator=ComparisonOperators.LTE)
        p1 = RulePolicy(r1)
        p2 = RulePolicy(r2)
        composite = CompositePolicy(p1, p2, BinaryOperators.OR)
        r = request(pay=60, loans=5)
        self.assertTrue(composite.evaluate(r))

    def test_or_both_fail(self):
        r1 = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r2 = Rule(variable="loans", value=0, comparison_operator=ComparisonOperators.LTE)
        p1 = RulePolicy(r1)
        p2 = RulePolicy(r2)
        composite = CompositePolicy(p1, p2, BinaryOperators.OR)
        r = request(pay=40, loans=5)
        self.assertFalse(composite.evaluate(r))

    def test_nested_composite(self):
        # (pay >= 50 AND status == ACTIVE) OR loans <= 0
        r1 = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r2 = Rule(variable="account_status", value="ACTIVE", comparison_operator=ComparisonOperators.EQ)
        r3 = Rule(variable="loans", value=0, comparison_operator=ComparisonOperators.LTE)
        left = CompositePolicy(RulePolicy(r1), RulePolicy(r2), BinaryOperators.AND)
        root = CompositePolicy(left, RulePolicy(r3), BinaryOperators.OR)

        # left fails (pay too low), but right passes (loans=0)
        r = request(pay=40, account_status="ACTIVE", loans=0)
        self.assertTrue(root.evaluate(r))

        # both fail
        r = request(pay=40, account_status="INACTIVE", loans=5)
        self.assertFalse(root.evaluate(r))


if __name__ == "__main__":
    unittest.main()
