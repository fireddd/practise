from Item import Item
from idle_state import IdleState
from collections import defaultdict
from threading import RLock, Lock
class VendingMachine:
    def __init__(self):
        self.state = IdleState()
        self.items = {}
        self.item_count = 0
        self.user_balance = {}
        self.user_item_selected = {}
        self.userLock = defaultdict(lambda: Lock())

    def set_state(self, state):
        self.state = state

    def display_items(self):
        self.state.display_items(self)

    def select_item(self, item_id, user_id):
        self.state.select_item(self, item_id, user_id)

    def insert_money(self, amount, user_id):
        self.state.insert_money(self, amount, user_id)

    def dispense(self, user_id):
        self.state.dispense(self, user_id)

    def cancel(self, item_id, user_id):
        self.state.cancel(self, item_id, user_id)

    def register_item(self, name, price, quantity):
        self.state.register_item(self, name, price, quantity)

    def display(self):
        print(self.items)

    def register_item_in_machine(self, name, price, quantity):
        item = Item(name=name, price=price, quantity=quantity, id=self.item_count)
        self.item_count = self.item_count + 1
        self.items[item.id] = item
        print("Registered", item)