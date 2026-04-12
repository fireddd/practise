from enum import Enum, auto


class TransactionStatus(Enum):
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
