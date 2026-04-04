from item_selected_state import ItemSelectedState
from vending_machine_state import VendingMachineState


class IdleState(VendingMachineState):
    def display_items(self, vending_machine):
        vending_machine.display()
        vending_machine.set_state(IdleState())

    def select_item(self, vending_machine, item_id, user_id):
        with vending_machine.userLock[user_id]:
            if item_id not in vending_machine.items:
                raise ValueError("Itemid not registered ")
            quantity = vending_machine.items[item_id].quantity
            if quantity <= 0:
                raise ValueError("Itemid is not present")
            print(vending_machine.items[item_id], "selected")
            vending_machine.user_item_selected[user_id] = item_id
            vending_machine.set_state(ItemSelectedState())

    def insert_money(self, vending_machine, amount, user_id):
        raise ValueError("Invalid operation")

    def dispense(self, vending_machine, user_id):
        raise ValueError("Invalid operation")

    def cancel(self, vending_machine, item_id, user_id):
        raise ValueError("Invalid operation")

    def register_item(self, vending_machine, name, price, quantity):
        vending_machine.register_item_in_machine(name, price, quantity)