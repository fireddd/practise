import uuid

from enums import TransactionStatus
from states.pending_state import PendingState


class Transaction:
    def __init__(self, transfers):
        self.transaction_id = str(uuid.uuid4())[:8]
        self.transfers = transfers
        self.status = TransactionStatus.PENDING
        self._state = PendingState()
        self.failure_reason = None

    def complete(self):
        self._state.on_completed(self)

    def fail(self):
        self._state.on_failed(self)

    def __repr__(self):
        return f"Transaction({self.transaction_id}, status={self.status.name}, transfers={len(self.transfers)})"
