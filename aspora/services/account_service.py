import uuid

from models import Account
from exceptions import AccountNotFoundException


class AccountService:
    def __init__(self, user_service):
        self._accounts = {}
        self._user_service = user_service

    def create_account(self, user_id, balance, account_type):
        self._user_service.get_user(user_id)
        account_id = str(uuid.uuid4())[:8]
        account = Account(account_id, user_id, balance, account_type)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise AccountNotFoundException(f"Account '{account_id}' not found")
        return self._accounts[account_id]
