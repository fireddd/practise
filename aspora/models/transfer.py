import uuid


class Transfer:
    def __init__(self, from_account_id, to_account_id, amount, transfer_type):
        self.transfer_id = str(uuid.uuid4())[:8]
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = amount
        self.transfer_type = transfer_type

    def __repr__(self):
        return (
            f"Transfer({self.transfer_id}, from={self.from_account_id}, "
            f"to={self.to_account_id}, amount={self.amount}, type={self.transfer_type.name})"
        )
