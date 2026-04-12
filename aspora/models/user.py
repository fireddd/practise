class User:
    def __init__(self, user_id, name, tier):
        self.user_id = user_id
        self.name = name
        self.tier = tier

    def __repr__(self):
        return f"User({self.user_id}, {self.name}, {self.tier.value})"
