from vending_machine_state import VendingMachineState


class InsertMoneyState(VendingMachineState):
    def display_items(self, vending_machine):
        vending_machine.display()

    def select_item(self, vending_machine, item_id, user_id):
        raise ValueError("Invalid operation, item already selected")

    def insert_money(self, vending_machine, amount, user_id):
        with vending_machine.userLock[user_id]:
            itemid = vending_machine.user_item_selected[user_id]
            price = vending_machine.items[itemid].price
            currentbalance = vending_machine.user_balance.get(user_id, 0)
            if(currentbalance + amount < price):
                vending_machine.user_balance[user_id] = currentbalance + amount
                print("balance updated to",vending_machine.user_balance[user_id], "for", user_id )
                vending_machine.set_state(InsertMoneyState())
            else:
                vending_machine.user_balance[user_id] = currentbalance + amount - price
                from product_dispense import ProductDispenseState
                vending_machine.set_state(ProductDispenseState())

    def dispense(self, vending_machine, user_id):
        raise ValueError("Invalid operation, not enough money")

    def cancel(self, vending_machine, item_id, user_id):
        with vending_machine.userLock[user_id]:
            currentbalance = vending_machine.user_balance[user_id]
            print("refunded ", currentbalance, "for ", user_id)
            vending_machine.user_balance[user_id] = 0
            del vending_machine.user_item_selected[user_id]
            from idle_state import IdleState
            vending_machine.set_state(IdleState())

    def register_item(self, vending_machine, name, price, quantity):
        raise ValueError("Invalid operation")