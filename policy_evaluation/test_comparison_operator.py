import unittest

from comparison_operator_factory import ComparisonOperatorFactory
from comparison_operators import ComparisonOperators


class TestComparisonOperator(unittest.TestCase):

    def setUp(self):
        self.cof = ComparisonOperatorFactory()

    def test_eq_true(self):
        self.assertTrue(self.cof.evaluate(50, 50, ComparisonOperators.EQ))

    def test_eq_false(self):
        self.assertFalse(self.cof.evaluate(50, 40, ComparisonOperators.EQ))

    def test_eq_string(self):
        self.assertTrue(self.cof.evaluate("ACTIVE", "ACTIVE", ComparisonOperators.EQ))

    def test_eq_string_false(self):
        self.assertFalse(self.cof.evaluate("ACTIVE", "INACTIVE", ComparisonOperators.EQ))

    def test_lte_true(self):
        self.assertTrue(self.cof.evaluate(50, 30, ComparisonOperators.LTE))

    def test_lte_equal(self):
        self.assertTrue(self.cof.evaluate(50, 50, ComparisonOperators.LTE))

    def test_lte_false(self):
        self.assertFalse(self.cof.evaluate(50, 60, ComparisonOperators.LTE))

    def test_gte_true(self):
        self.assertTrue(self.cof.evaluate(50, 60, ComparisonOperators.GTE))

    def test_gte_equal(self):
        self.assertTrue(self.cof.evaluate(50, 50, ComparisonOperators.GTE))

    def test_gte_false(self):
        self.assertFalse(self.cof.evaluate(50, 40, ComparisonOperators.GTE))

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.cof.evaluate(50, 50, "INVALID")


if __name__ == "__main__":
    unittest.main()
