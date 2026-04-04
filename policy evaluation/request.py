from dataclasses import dataclass

@dataclass()
class request:
    def __init__(self, creditscore=None, account_status=None, balance=None, pay=None, loans=None):
        self.pay = pay
        self.creditscore = creditscore
        self.account_status = account_status
        self.balance = balance
        self.loans = loans