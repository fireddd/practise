from coupon_system.enums import CouponType, Comparator
from coupon_system.models import Rule, Coupon, Cart, RuleEvaluationContext, Promotion
from coupon_system.calculators import DiscountCalculatorFactory
from coupon_system.services import RuleService, CouponService, PromotionService


def test_phase_1():
    print("=== Phase 1: Enums + Models ===\n")

    # Enums
    print(f"CouponType.FLAT = {CouponType.FLAT.value}")
    print(f"CouponType.PERCENTAGE = {CouponType.PERCENTAGE.value}")
    print(f"Comparator.EQ = {Comparator.EQ.value}")
    print(f"Comparator.GTE = {Comparator.GTE.value}")
    print(f"Comparator.LTE = {Comparator.LTE.value}")

    # Rule
    rule = Rule(rule_id="r1", variable="amount", value=500, comparator=Comparator.GTE)
    print(f"\n{rule}")
    assert rule.rule_id == "r1"
    assert rule.variable == "amount"
    assert rule.value == 500
    assert rule.comparator == Comparator.GTE

    # Coupon
    coupon = Coupon(
        coupon_id="c1", coupon_code="SAVE10", value=10,
        coupon_type=CouponType.PERCENTAGE, min_cart_value=200, rule_id="r1"
    )
    print(coupon)
    assert coupon.coupon_code == "SAVE10"
    assert coupon.coupon_type == CouponType.PERCENTAGE
    assert coupon.min_cart_value == 200
    assert coupon.rule_id == "r1"

    # Cart
    cart = Cart(user_id="u1", amount=1000)
    print(cart)
    assert cart.user_id == "u1"
    assert cart.amount == 1000

    # RuleEvaluationContext
    ctx = RuleEvaluationContext(amount=1000, user_id="u1")
    print(ctx)
    assert ctx.amount == 1000
    assert ctx.user_id == "u1"

    # Promotion
    promo = Promotion(
        promotion_id="p1", name="Chocolate Sale",
        discount_type=CouponType.PERCENTAGE, discount_value=20, rule_id="r1"
    )
    print(promo)
    assert promo.name == "Chocolate Sale"
    assert promo.discount_type == CouponType.PERCENTAGE
    assert promo.discount_value == 20

    print("\n✅ Phase 1 passed!\n")


def test_phase_2():
    print("=== Phase 2: Comparator + Rule Evaluation ===\n")

    # Rule: amount >= 500
    rule_gte = Rule(rule_id="r1", variable="amount", value=500, comparator=Comparator.GTE)

    ctx_pass = RuleEvaluationContext(amount=1000, user_id="u1")
    ctx_exact = RuleEvaluationContext(amount=500, user_id="u1")
    ctx_fail = RuleEvaluationContext(amount=200, user_id="u1")

    assert rule_gte.evaluate(ctx_pass) is True, "1000 >= 500 should pass"
    assert rule_gte.evaluate(ctx_exact) is True, "500 >= 500 should pass"
    assert rule_gte.evaluate(ctx_fail) is False, "200 >= 500 should fail"
    print(f"{rule_gte} | amount=1000 -> {rule_gte.evaluate(ctx_pass)}")
    print(f"{rule_gte} | amount=500  -> {rule_gte.evaluate(ctx_exact)}")
    print(f"{rule_gte} | amount=200  -> {rule_gte.evaluate(ctx_fail)}")

    # Rule: user_id == "u1"
    rule_eq = Rule(rule_id="r2", variable="user_id", value="u1", comparator=Comparator.EQ)
    ctx_match = RuleEvaluationContext(amount=100, user_id="u1")
    ctx_no_match = RuleEvaluationContext(amount=100, user_id="u2")

    assert rule_eq.evaluate(ctx_match) is True, "u1 == u1 should pass"
    assert rule_eq.evaluate(ctx_no_match) is False, "u2 == u1 should fail"
    print(f"{rule_eq} | user_id=u1 -> {rule_eq.evaluate(ctx_match)}")
    print(f"{rule_eq} | user_id=u2 -> {rule_eq.evaluate(ctx_no_match)}")

    # Rule: amount <= 300
    rule_lte = Rule(rule_id="r3", variable="amount", value=300, comparator=Comparator.LTE)
    ctx_below = RuleEvaluationContext(amount=100, user_id="u1")
    ctx_above = RuleEvaluationContext(amount=500, user_id="u1")

    assert rule_lte.evaluate(ctx_below) is True, "100 <= 300 should pass"
    assert rule_lte.evaluate(ctx_above) is False, "500 <= 300 should fail"
    print(f"{rule_lte} | amount=100 -> {rule_lte.evaluate(ctx_below)}")
    print(f"{rule_lte} | amount=500 -> {rule_lte.evaluate(ctx_above)}")

    print("\n✅ Phase 2 passed!\n")


def test_phase_3():
    print("=== Phase 3: Discount Calculators ===\n")

    flat_calc = DiscountCalculatorFactory.get_calculator(CouponType.FLAT)
    pct_calc = DiscountCalculatorFactory.get_calculator(CouponType.PERCENTAGE)

    # Flat: 500 - 50 = 450
    result = flat_calc.calculate(500, 50)
    assert result == 450, f"Expected 450, got {result}"
    print(f"Flat: 500 - 50 = {result}")

    # Flat: 30 - 50 = 0 (floor at 0)
    result = flat_calc.calculate(30, 50)
    assert result == 0, f"Expected 0, got {result}"
    print(f"Flat: 30 - 50 = {result} (floored at 0)")

    # Percentage: 500 - 10% = 450
    result = pct_calc.calculate(500, 10)
    assert result == 450, f"Expected 450, got {result}"
    print(f"Percentage: 500 - 10% = {result}")

    # Percentage: 1000 - 25% = 750
    result = pct_calc.calculate(1000, 25)
    assert result == 750, f"Expected 750, got {result}"
    print(f"Percentage: 1000 - 25% = {result}")

    # Factory returns same type
    assert type(flat_calc).__name__ == "FlatDiscountCalculator"
    assert type(pct_calc).__name__ == "PercentageDiscountCalculator"

    print("\n✅ Phase 3 passed!\n")


def test_phase_4():
    print("=== Phase 4: RuleService + CouponService CRUD ===\n")

    rule_service = RuleService()
    coupon_service = CouponService(rule_service)

    # Create rule
    rule = rule_service.create_rule("amount", 500, Comparator.GTE)
    print(f"Created: {rule}")
    assert rule_service.get_rule(rule.rule_id) is rule

    # Create coupon
    coupon = coupon_service.create_coupon(
        coupon_code="SAVE10", value=10, coupon_type=CouponType.PERCENTAGE,
        min_cart_value=200, rule_id=rule.rule_id,
    )
    print(f"Created: {coupon}")

    # Fetch by code
    fetched = coupon_service.get_coupon("SAVE10")
    assert fetched is coupon
    print(f"Fetched by code: {fetched}")

    # Fetch unknown code
    assert coupon_service.get_coupon("UNKNOWN") is None
    print("Fetched 'UNKNOWN' -> None")

    # Update value
    updated = coupon_service.update_coupon(coupon.coupon_id, value=15)
    assert updated.value == 15
    print(f"Updated value to 15: {updated}")

    # Delete
    deleted = coupon_service.delete_coupon(coupon.coupon_id)
    assert deleted is True
    assert coupon_service.get_coupon("SAVE10") is None
    print(f"Deleted coupon, fetch returns None")

    # Delete non-existent
    assert coupon_service.delete_coupon("nonexistent") is False
    print("Delete non-existent -> False")

    print("\n✅ Phase 4 passed!\n")


def test_phase_5():
    print("=== Phase 5: CouponService.evaluate_cart ===\n")

    rule_service = RuleService()
    coupon_service = CouponService(rule_service)

    # Setup: rule requiring amount >= 500
    rule = rule_service.create_rule("amount", 500, Comparator.GTE)

    # SAVE10: 10% off, min cart 200, rule amount >= 500
    coupon_service.create_coupon(
        coupon_code="SAVE10", value=10, coupon_type=CouponType.PERCENTAGE,
        min_cart_value=200, rule_id=rule.rule_id,
    )
    # FLAT50: flat 50 off, min cart 100, rule amount >= 500
    coupon_service.create_coupon(
        coupon_code="FLAT50", value=50, coupon_type=CouponType.FLAT,
        min_cart_value=100, rule_id=rule.rule_id,
    )

    # Test 1: Single coupon — 1000 - 10% = 900
    cart = Cart(user_id="u1", amount=1000)
    result, applied = coupon_service.evaluate_cart(cart, ["SAVE10"])
    assert result == 900, f"Expected 900, got {result}"
    assert applied == ["SAVE10"]
    print(f"Test 1 - Single pct coupon: 1000 -> {result}, applied={applied}")

    # Test 2: Multiple coupons FIFO — 1000 - 10% = 900, then 900 - 50 = 850
    result, applied = coupon_service.evaluate_cart(cart, ["SAVE10", "FLAT50"])
    assert result == 850, f"Expected 850, got {result}"
    assert applied == ["SAVE10", "FLAT50"]
    print(f"Test 2 - Multiple coupons: 1000 -> {result}, applied={applied}")

    # Test 3: Rule fails — cart 200, rule requires >= 500, no discount
    small_cart = Cart(user_id="u1", amount=200)
    result, applied = coupon_service.evaluate_cart(small_cart, ["SAVE10"])
    assert result == 200, f"Expected 200, got {result}"
    assert applied == []
    print(f"Test 3 - Rule fails: 200 -> {result}, applied={applied}")

    # Test 4: Below min_cart_value
    # Create coupon with min_cart_value=800, same rule
    coupon_service.create_coupon(
        coupon_code="BIG20", value=20, coupon_type=CouponType.PERCENTAGE,
        min_cart_value=800, rule_id=rule.rule_id,
    )
    cart_600 = Cart(user_id="u1", amount=600)
    result, applied = coupon_service.evaluate_cart(cart_600, ["BIG20"])
    assert result == 600, f"Expected 600, got {result}"
    assert applied == []
    print(f"Test 4 - Below min_cart_value: 600 -> {result}, applied={applied}")

    # Test 5: Unknown coupon code ignored
    result, applied = coupon_service.evaluate_cart(cart, ["DOESNOTEXIST"])
    assert result == 1000, f"Expected 1000, got {result}"
    assert applied == []
    print(f"Test 5 - Unknown code: 1000 -> {result}, applied={applied}")

    print("\n✅ Phase 5 passed!\n")


def test_phase_6():
    print("=== Phase 6: PromotionService ===\n")

    rule_service = RuleService()
    promotion_service = PromotionService(rule_service)

    # Rule: amount >= 100
    rule = rule_service.create_rule("amount", 100, Comparator.GTE)

    # Create promotion: "Chocolate Sale" 20% off
    promo = promotion_service.create_promotion(
        name="Chocolate Sale", discount_type=CouponType.PERCENTAGE,
        discount_value=20, rule_id=rule.rule_id,
    )
    print(f"Created: {promo}")

    # List promotions
    promos = promotion_service.get_promotions()
    assert len(promos) == 1
    assert promos[0].name == "Chocolate Sale"
    print(f"All promotions: {promos}")

    # Apply promotion — 500 - 20% = 400
    ctx = RuleEvaluationContext(amount=500, user_id="u1")
    result = promotion_service.apply_promotions(ctx, 500)
    assert result == 400, f"Expected 400, got {result}"
    print(f"Test 1 - Apply 20% promo to 500: {result}")

    # Rule fails — amount 50 < 100
    ctx_small = RuleEvaluationContext(amount=50, user_id="u1")
    result = promotion_service.apply_promotions(ctx_small, 50)
    assert result == 50, f"Expected 50, got {result}"
    print(f"Test 2 - Rule fails (50 < 100): {result}")

    # Multiple promotions stack
    rule2 = rule_service.create_rule("amount", 200, Comparator.GTE)
    promotion_service.create_promotion(
        name="Summer Sale", discount_type=CouponType.FLAT,
        discount_value=30, rule_id=rule2.rule_id,
    )
    ctx_big = RuleEvaluationContext(amount=1000, user_id="u1")
    result = promotion_service.apply_promotions(ctx_big, 1000)
    # 1000 - 20% = 800, then 800 - 30 = 770
    assert result == 770, f"Expected 770, got {result}"
    print(f"Test 3 - Stacked promos (20% + flat 30): 1000 -> {result}")

    print("\n✅ Phase 6 passed!\n")


if __name__ == "__main__":
    test_phase_1()
    test_phase_2()
    test_phase_3()
    test_phase_4()
    test_phase_5()
    test_phase_6()
