from abc import ABC, abstractmethod


class TransferExecutor(ABC):
    @abstractmethod
    def execute(self, transfer, from_account, to_account):
        pass
