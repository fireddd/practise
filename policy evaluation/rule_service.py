from rule import Rule
class RuleService:
    def __init__(self):
        self.rules = []

    def create_rule(self, value, variable, comparison_operator):
        r = Rule(value=value, variable=variable, comparison_operator=comparison_operator)
        self.rules.append(r)
        return r