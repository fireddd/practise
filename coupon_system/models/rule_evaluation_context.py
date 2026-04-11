class RuleEvaluationContext:
    def __init__(self, amount: float, user_id: str):
        self.amount = amount
        self.user_id = user_id

    def __repr__(self):
        return f"RuleEvaluationContext(amount={self.amount}, user_id={self.user_id})"
