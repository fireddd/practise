import unittest

from binary_operator_factory import BinaryOperatorFactory
from binary_operators import BinaryOperators


class TestBinaryOperator(unittest.TestCase):

    def setUp(self):
        self.bof = BinaryOperatorFactory()

    def test_and_true(self):
        self.assertTrue(self.bof.evaluate(True, True, BinaryOperators.AND))

    def test_and_false_first(self):
        self.assertFalse(self.bof.evaluate(False, True, BinaryOperators.AND))

    def test_and_false_second(self):
        self.assertFalse(self.bof.evaluate(True, False, BinaryOperators.AND))

    def test_and_both_false(self):
        self.assertFalse(self.bof.evaluate(False, False, BinaryOperators.AND))

    def test_or_true(self):
        self.assertTrue(self.bof.evaluate(True, True, BinaryOperators.OR))

    def test_or_one_true(self):
        self.assertTrue(self.bof.evaluate(False, True, BinaryOperators.OR))

    def test_or_both_false(self):
        self.assertFalse(self.bof.evaluate(False, False, BinaryOperators.OR))

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.bof.evaluate(True, True, "INVALID")


if __name__ == "__main__":
    unittest.main()
