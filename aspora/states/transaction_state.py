from abc import ABC, abstractmethod

from exceptions import InvalidStateTransitionException


class TransactionState(ABC):

    def on_completed(self, transaction):
        raise InvalidStateTransitionException(
            f"Cannot move to COMPLETED from {self.name}"
        )

    def on_failed(self, transaction):
        raise InvalidStateTransitionException(
            f"Cannot move to FAILED from {self.name}"
        )

    @property
    @abstractmethod
    def name(self):
        pass
