from enums import TransferType
from executors.account_transfer_executor import AccountTransferExecutor
from executors.deposit_executor import DepositExecutor
from executors.withdrawal_executor import WithdrawalExecutor
from exceptions import ValidationException


class ExecutorFactory:

    @staticmethod
    def get_executor(transfer_type):
        match transfer_type:
            case TransferType.ACCOUNT_TRANSFER:
                return AccountTransferExecutor()
            case TransferType.DEPOSIT:
                return DepositExecutor()
            case TransferType.WITHDRAWAL:
                return WithdrawalExecutor()
            case _:
                raise ValidationException(f"No executor for {transfer_type}")
