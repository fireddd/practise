import unittest

from comparison_operators import ComparisonOperators
from request import request
from rule import Rule


class TestRule(unittest.TestCase):

    def test_gte_pass(self):
        rule = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r = request(pay=60)
        self.assertTrue(rule.evaluate(r))

    def test_gte_fail(self):
        rule = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r = request(pay=40)
        self.assertFalse(rule.evaluate(r))

    def test_lte_pass(self):
        rule = Rule(variable="loans", value=10, comparison_operator=ComparisonOperators.LTE)
        r = request(loans=5)
        self.assertTrue(rule.evaluate(r))

    def test_lte_fail(self):
        rule = Rule(variable="loans", value=10, comparison_operator=ComparisonOperators.LTE)
        r = request(loans=15)
        self.assertFalse(rule.evaluate(r))

    def test_eq_pass(self):
        rule = Rule(variable="account_status", value="ACTIVE", comparison_operator=ComparisonOperators.EQ)
        r = request(account_status="ACTIVE")
        self.assertTrue(rule.evaluate(r))

    def test_eq_fail(self):
        rule = Rule(variable="account_status", value="ACTIVE", comparison_operator=ComparisonOperators.EQ)
        r = request(account_status="INACTIVE")
        self.assertFalse(rule.evaluate(r))

    def test_none_field_returns_true(self):
        rule = Rule(variable="pay", value=50, comparison_operator=ComparisonOperators.GTE)
        r = request()
        self.assertTrue(rule.evaluate(r))


if __name__ == "__main__":
    unittest.main()
