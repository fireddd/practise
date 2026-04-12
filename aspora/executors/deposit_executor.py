from executors.transfer_executor import TransferExecutor


class DepositExecutor(TransferExecutor):

    def execute(self, transfer, from_account, to_account):
        to_account.balance += transfer.amount
