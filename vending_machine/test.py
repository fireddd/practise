import unittest

from idle_state import IdleState
from item_selected_state import ItemSelectedState
from vending_machine import VendingMachine


class TestIdleState(unittest.TestCase):

     def setUp(self):
         self.vendingmachine = VendingMachine()
         self.vendingmachine.register_item("abc",25, 5)

     def test_change_state(self):
         self.assertIsInstance(self.vendingmachine.state, IdleState)

     def test_item(self):
         self.vendingmachine.select_item(0, "abc")
         self.assertIsInstance(self.vendingmachine.state, ItemSelectedState)


     def test_out_of_stock_raises(self):
        self.vendingmachine.items[0].quantity = 0
        with self.assertRaises(ValueError):
            self.vendingmachine.select_item(0, "U01")

def test_change_state(self):
    self.assertIsInstance(self.vendingmachine.state, IdleState)
if __name__ == '__main__':
    unittest.main()