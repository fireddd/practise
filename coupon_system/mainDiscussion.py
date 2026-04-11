

# We run an e-commerce platform.
# We want to build a Coupon and Promotion system.
# Users should be able to apply coupons at checkout and get discounts.
# NFR
# 1L RPS per day.
# Type of coupon-> bogo, flat 10%, percentage based.
# promotion-> campaign for chocolates have 20% off.
# Entities, db integeration,
# create api for the end, testing with that.

# FR
# Create coupon, based on a rule.
# delete coupon,
# fetch coupon,
# update coupon,
# create Promotion will be single rule based.
# you need to apply multiple coupons at a time.

#Entities
'''
Need to have coupon evaulator engine:

Need calculate_cost():

class couponType(Enum):
    special:
    flat
    percentage
class Coupon:
    value = None
    type = None
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Comparator(Enum)
    EQ = 0
    GTE = 1
    LTE = 2
class ComparatorEvaulatorFactory():
    based on Comparator,
    have a switch case on the compraator nad return whether the expression satfied or not.

class EvaluateExpression(ABC):
    @abstractmethod
    def evaluate(self):
        pass
class Rule(EvaluateExpression):
    variable
    value
    Comparator:
    def evaluate(self):
        use ComparatorEvaulatorFactory and return the result.

class RuleService:
    create_rule
    update_rule

class Cart(Rule):
    amount
    user_id
class RuleEvaluationContext:
    amount
    user_id

class RuleEvaulationService:
    def __init__(self, rule_service):
        self.rule_service = rule_service
    create_rule
    update_rule
    evaulate(RuleEvaluationContext): returns a list of valid rules,

CouponService:
    create_coupon
    update_coupon
    add a method mapping for coupon and rule()
    evaulate_cart()// construct the RuleEvaluationContext using cart class, and get the relevant rules are applicable,
'''

if __name__ == "__main__":
    print("Hello world")