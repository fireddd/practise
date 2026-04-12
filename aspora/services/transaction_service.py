from enums import TransferType
from models import Transfer, Transaction
from validation import ValidationContext
from executors import ExecutorFactory
from exceptions import (
    AccountNotFoundException, InsufficientBalanceException, ValidationException,
)


class TransactionService:
    def __init__(self, account_service, user_service, validation_service):
        self._account_service = account_service
        self._user_service = user_service
        self._validation_service = validation_service
        self._executor_factory = ExecutorFactory()
        self._transactions = {}

    def execute_transfer(self, from_account_id, to_account_id, amount, transfer_type):
        from_account = self._account_service.get_account(from_account_id) if from_account_id else None
        to_account = self._account_service.get_account(to_account_id) if to_account_id else None

        if transfer_type == TransferType.ACCOUNT_TRANSFER:
            if from_account is None:
                raise AccountNotFoundException("from_account is required for account transfer")
            if to_account is None:
                raise AccountNotFoundException("to_account is required for account transfer")
        elif transfer_type == TransferType.WITHDRAWAL:
            if from_account is None:
                raise AccountNotFoundException("from_account is required for withdrawal")
        elif transfer_type == TransferType.DEPOSIT:
            if to_account is None:
                raise AccountNotFoundException("to_account is required for deposit")

        if transfer_type == TransferType.DEPOSIT:
            initiator_account = to_account
        else:
            initiator_account = from_account
        sender_user = self._user_service.get_user(initiator_account.user_id)

        transfer = Transfer(from_account_id, to_account_id, amount, transfer_type)
        txn = Transaction([transfer])
        self._transactions[txn.transaction_id] = txn

        locks = self._get_sorted_locks(from_account, to_account)
        for lock in locks:
            lock.acquire()

        try:
            self._validate(transfer, from_account, to_account, sender_user.tier)
            executor = self._executor_factory.get_executor(transfer_type)
            executor.execute(transfer, from_account, to_account)
            txn.complete()
        except Exception as e:
            txn.fail()
            txn.failure_reason = str(e)
        finally:
            for lock in locks:
                lock.release()

        return txn

    def get_status(self, transaction_id):
        txn = self._transactions.get(transaction_id)
        if txn is None:
            raise ValidationException(f"Transaction {transaction_id} not found")
        return txn.status

    def _validate(self, transfer, from_account, to_account, sender_tier):
        ctx = ValidationContext(
            transfer_amount=transfer.amount,
            sender_tier=sender_tier,
        )
        passed, failed_policy = self._validation_service.evaluate(ctx)
        if not passed:
            raise ValidationException(f"Validation failed: {failed_policy}")

        if from_account is not None and from_account.balance < transfer.amount:
            raise InsufficientBalanceException(
                f"Account {from_account.account_id} has balance {from_account.balance}, "
                f"need {transfer.amount}"
            )

        if (from_account is not None and to_account is not None
                and from_account.account_id == to_account.account_id):
            raise ValidationException("Cannot transfer to the same account")

    def _get_sorted_locks(self, from_account, to_account):
        accounts = {a.account_id: a for a in (from_account, to_account) if a is not None}
        return [accounts[aid]._lock for aid in sorted(accounts)]
