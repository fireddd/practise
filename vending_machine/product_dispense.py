from vending_machine_state import VendingMachineState


class ProductDispenseState(VendingMachineState):
    def display_items(self, vending_machine):
        vending_machine.display()

    def select_item(self, vending_machine, item_id, user_id):
        raise ValueError("Invalid operation")

    def insert_money(self, vending_machine, amount, user_id):
        raise ValueError("Invalid operation")

    def dispense(self, vending_machine, user_id):
        from idle_state import IdleState
        with vending_machine.userLock[user_id]:
            itemid = vending_machine.user_item_selected[user_id]
            del vending_machine.user_item_selected[user_id]
            vending_machine.items[itemid].quantity = vending_machine.items[itemid].quantity - 1
            print(itemid, "dispensed for", user_id)
            change = vending_machine.user_balance[user_id]
            print("Change returned:", change)
            vending_machine.user_balance[user_id] = 0
            vending_machine.set_state(IdleState())

    def cancel(self, vending_machine, item_id, user_id):
        raise ValueError("Invalid operation")

    def register_item(self, vending_machine, name, price, quantity):
        raise ValueError("Invalid operation")