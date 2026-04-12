from enum import Enum, auto


class TransferType(Enum):
    DEPOSIT = auto()
    WITHDRAWAL = auto()
    ACCOUNT_TRANSFER = auto()
