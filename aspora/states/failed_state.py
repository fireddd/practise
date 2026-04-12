from states.transaction_state import TransactionState


class FailedState(TransactionState):

    @property
    def name(self):
        return "FAILED"
