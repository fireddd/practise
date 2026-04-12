from executors.transfer_executor import TransferExecutor


class WithdrawalExecutor(TransferExecutor):

    def execute(self, transfer, from_account, to_account):
        from_account.balance -= transfer.amount
