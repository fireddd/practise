from abc import ABC, abstractmethod

class VendingMachineState(ABC):
    @abstractmethod
    def display_items(self, vending_machine):
        pass

    @abstractmethod
    def select_item(self, vending_machine, item_id, user_id):
        pass

    @abstractmethod
    def insert_money(self, vending_machine, amount, user_id):
        pass

    @abstractmethod
    def dispense(self, vending_machine, user_id):
        pass

    @abstractmethod
    def cancel(self, vending_machine, item_id, user_id):
        pass

    @abstractmethod
    def register_item(self, vending_machine, name, price, quantity):
        pass

    def set_state(self, state):
        pass