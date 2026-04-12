from states.transaction_state import TransactionState
from enums import TransactionStatus


class PendingState(TransactionState):

    @property
    def name(self):
        return "PENDING"

    def on_completed(self, transaction):
        from states.completed_state import CompletedState
        transaction._state = CompletedState()
        transaction.status = TransactionStatus.COMPLETED

    def on_failed(self, transaction):
        from states.failed_state import FailedState
        transaction._state = FailedState()
        transaction.status = TransactionStatus.FAILED
