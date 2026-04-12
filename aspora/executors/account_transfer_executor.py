from executors.transfer_executor import TransferExecutor


class AccountTransferExecutor(TransferExecutor):

    def execute(self, transfer, from_account, to_account):
        from_account.balance -= transfer.amount
        to_account.balance += transfer.amount
