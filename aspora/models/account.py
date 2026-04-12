import threading


class Account:
    def __init__(self, account_id, user_id, balance, account_type):
        self.account_id = account_id
        self.user_id = user_id
        self.balance = balance
        self.account_type = account_type
        self._lock = threading.Lock()

    def __repr__(self):
        return f"Account({self.account_id}, user={self.user_id}, balance={self.balance}, type={self.account_type.value})"
