from insert_money_state import InsertMoneyState
from vending_machine_state import VendingMachineState


class ItemSelectedState(VendingMachineState):
    def display_items(self, vending_machine):
        vending_machine.display()

    def select_item(self, vending_machine, item_id, user_id):
        vending_machine.set_state(ItemSelectedState())

    def insert_money(self, vending_machine, amount, user_id):
        vending_machine.set_state(InsertMoneyState())
        vending_machine.insert_money(amount, user_id)

    def dispense(self, vending_machine, user_id):
        raise ValueError("Invalid operation")

    def cancel(self, vending_machine, item_id, user_id):
        raise ValueError("Invalid operation")

    def register_item(self, vending_machine, name, price, quantity):
        raise ValueError("Invalid operation")