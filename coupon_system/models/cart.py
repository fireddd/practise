class Cart:
    def __init__(self, user_id: str, amount: float):
        self.user_id = user_id
        self.amount = amount

    def __repr__(self):
        return f"Cart(user_id={self.user_id}, amount={self.amount})"
