# This is a sample Python script.
from vending_machine import VendingMachine


# 🧾 Problem Statement: In-Memory Vending Machine System
#
# You are required to design and implement an in-memory Vending Machine System. Unlike a standard machine, this system must support concurrent access.
#
# Imagine a smart vending machine that can be accessed via a physical panel and a mobile app simultaneously. The machine should manage inventory, handle money transactions, and provide a user-friendly interface.
#
# The focus of this problem is to build a system that is scalable with modular code and all edge cases handled.
#
# 1. Core Functionalities Required
# 1. User Interaction
# Display a list of available items with their prices.
# Allow users to select an item by entering its code.
# 2. Payment Processing
# Calculate the total cost of the selected item.
# Accept payment incrementally and validate against item cost.
# Dispense the item if full payment is received and user selects dispense.
# Return change if payment exceeds the item price.
# 3. Inventory Management
# Keep track of stock for each item.
# Mark an item as unavailable if it is out of stock.
# Allow restocking by administrators.
# 4. Error Handling
# Insufficient payment → Notify users to pay the remaining amount.
# Invalid selection → Notify users if they select an unavailable or out-of-stock item.
# 2. Methods Expected
#
# The system must support the following operations via standard input:
#
# DISPLAY_ITEMS
# Show all items, prices, and current stock.
# SELECT_ITEM <item_code> <user>
# Start a transaction for a specific item.
# If the item is out of stock, return an error immediately.
# INSERT_MONEY <amount> <user>
# Add money to the current transaction.
# DISPENSE <user>
# If balance is sufficient: deduct inventory, return change, and complete the transaction.
# If insufficient: prompt for remaining balance.
# CANCEL <item_code> <user>
# Abort the current transaction and refund all inserted money.
# REGISTER_ITEM <name> <price> <initial_quantity>
# Add a new item and its stock to the system.
# 3. What Not to Focus On
# Adding different payment methods.
# Creating a separate user service layer (you can assume predefined users).
# 4. Sample Input
# DISPLAY_ITEMS
# SELECT_ITEM C01 U01
# INSERT_MONEY 10 U01
# INSERT_MONEY 20 U01
# DISPENSE
# 5. Sample Output (Illustrative)
# C01: Coke (25) [5 left], B02: Water (10) [2 left]
# Item C01 Selected. Current Balance: 0. Remaining: 25.
# Balance Updated: 10. Remaining: 15.
# Balance Updated: 30. Remaining: 0.
# Dispensed item. Change returned: 5.
#
# If you want, I can also help you with a clean LLD design or code implementation (Python/C++) for this.
def solve():
    vending_machine = VendingMachine()
    vending_machine.register_item("ab",2, 20)
    vending_machine.register_item("bc",1, 30)
    vending_machine.register_item("de",3, 34)
    vending_machine.display()
    vending_machine.select_item(1, 12)
    # vending_machine.insert_money(1, 12)
    vending_machine.insert_money(1, 12)
    vending_machine.dispense(12)
    vending_machine.display()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solve()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
