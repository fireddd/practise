from states.transaction_state import TransactionState


class CompletedState(TransactionState):

    @property
    def name(self):
        return "COMPLETED"
