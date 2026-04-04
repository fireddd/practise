# This is a sample Python script.
from binary_operators import BinaryOperators
from policy_evaluation_service import PolicyEvalutaionService


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from comparison_operators import *
from request import request

#
# Problem Statement: Policy Evaluation Engine
#
# Design and build a Policy Evaluation Engine that allows dynamic definition and execution of business rules (policies) against incoming data records to determine whether they should be allowed or blocked.
#
# Background
#
# In many systems (e.g., lending, payments, compliance), decisions are driven by configurable policies such as:
#
# ((credit_score > 750 and account_status == "active") or (transaction_amount < 1,00,000)) and account_status == "active"
# account_status == "active"
# country != "blacklisted"
# transaction_amount < 1,00,000
#
# These policies may evolve frequently and should be configurable without requiring code changes.

def solve():
    # Use a breakpoint in the code line below to debug your script.
    ps = PolicyEvalutaionService()
    # def __init__(self, creditscore, account_status, balance, pay, loans):
    #     self.pay = pay
    #     self.creditscore = creditscore
    #     self.account_status = account_status
    #     self.balance = balance
    #     self.loans = loans //40
    ps.create_rule_policy(value=50,variable="pay", comparison_operator=ComparisonOperators.GTE)
    ps.create_rule_policy(variable="account_status",value= "ACTIVE", comparison_operator= ComparisonOperators.EQ)
    ps.create_rule_policy(variable="loans",value= 0, comparison_operator= ComparisonOperators.LTE)
    ps1 = ps.create_policy_via_rules(variable="loans",value= 0, comparison_operator= ComparisonOperators.LTE)
    ps2 = ps.create_policy_via_rules(variable="account_status",value= "ACTIVE", comparison_operator= ComparisonOperators.EQ)
    ps.create_policies_with_operator(ps1, ps2, BinaryOperators.AND)
    r12 = request(loans=4)
    r14 = request(pay=40)
    print(ps.evaluate(r12))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    solve()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
