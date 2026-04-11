import requests

BASE = "http://localhost:8000"


def post(path, body):
    resp = requests.post(f"{BASE}{path}", json=body)
    resp.raise_for_status()
    return resp.json()


def get(path):
    resp = requests.get(f"{BASE}{path}")
    resp.raise_for_status()
    return resp.json()


def delete(path):
    resp = requests.delete(f"{BASE}{path}")
    resp.raise_for_status()
    return resp.json()


def put(path, body):
    resp = requests.put(f"{BASE}{path}", json=body)
    resp.raise_for_status()
    return resp.json()


def main():
    print("=== E2E API Test: Full Checkout Flow ===\n")

    # 1. Health check
    assert get("/health") == {"status": "ok"}
    print("[OK] Health check")

    # 2. Create rules
    rule_amt = post("/rules", {"variable": "amount", "value": 500, "comparator": "GTE"})
    rule_user = post("/rules", {"variable": "user_id", "value": "vip-user", "comparator": "EQ"})
    print(f"[OK] Created rules: {rule_amt['rule_id']}, {rule_user['rule_id']}")

    # 3. Fetch rules back
    fetched = get(f"/rules/{rule_amt['rule_id']}")
    assert fetched["variable"] == "amount"
    assert fetched["comparator"] == "GTE"
    print(f"[OK] Fetched rule: {fetched}")

    # 4. Create coupons
    c1 = post("/coupons", {
        "coupon_code": "SUMMER10", "value": 10, "coupon_type": "PERCENTAGE",
        "min_cart_value": 200, "rule_id": rule_amt["rule_id"],
    })
    c2 = post("/coupons", {
        "coupon_code": "FLAT100", "value": 100, "coupon_type": "FLAT",
        "min_cart_value": 100, "rule_id": rule_amt["rule_id"],
    })
    c3 = post("/coupons", {
        "coupon_code": "VIP25", "value": 25, "coupon_type": "PERCENTAGE",
        "min_cart_value": 0, "rule_id": rule_user["rule_id"],
    })
    print(f"[OK] Created coupons: SUMMER10, FLAT100, VIP25")

    # 5. Fetch coupon by code
    fetched_c = get("/coupons/SUMMER10")
    assert fetched_c["coupon_code"] == "SUMMER10"
    assert fetched_c["value"] == 10
    print(f"[OK] Fetched coupon: {fetched_c['coupon_code']}")

    # 6. Update coupon
    updated = put(f"/coupons/{c1['coupon_id']}", {"value": 15})
    assert updated["value"] == 15
    print(f"[OK] Updated SUMMER10 value: 10 -> 15")

    # 7. Create promotion
    promo = post("/promotions", {
        "name": "Chocolate Sale", "discount_type": "PERCENTAGE",
        "discount_value": 20, "rule_id": rule_amt["rule_id"],
    })
    promos = get("/promotions")
    assert len(promos) == 1
    print(f"[OK] Created promotion: {promo['name']}")

    # 8. Evaluate cart — single coupon
    result = post("/cart/evaluate", {
        "user_id": "u1", "amount": 1000, "coupon_codes": ["SUMMER10"],
    })
    assert result["original_amount"] == 1000
    assert result["final_amount"] == 850  # 15% off 1000 = 850
    assert result["applied_coupons"] == ["SUMMER10"]
    print(f"[OK] Single coupon: 1000 -> {result['final_amount']} (applied: {result['applied_coupons']})")

    # 9. Evaluate cart — stacked coupons (FIFO)
    # SUMMER10: 15% off 1000 = 850, then FLAT100: 850 - 100 = 750
    result = post("/cart/evaluate", {
        "user_id": "u1", "amount": 1000, "coupon_codes": ["SUMMER10", "FLAT100"],
    })
    assert result["final_amount"] == 750
    assert result["applied_coupons"] == ["SUMMER10", "FLAT100"]
    print(f"[OK] Stacked coupons: 1000 -> {result['final_amount']} (applied: {result['applied_coupons']})")

    # 10. Evaluate cart — rule fails (amount 200 < 500)
    result = post("/cart/evaluate", {
        "user_id": "u1", "amount": 200, "coupon_codes": ["SUMMER10"],
    })
    assert result["final_amount"] == 200
    assert result["applied_coupons"] == []
    print(f"[OK] Rule fails: 200 -> {result['final_amount']} (no coupons applied)")

    # 11. Evaluate cart — VIP coupon, wrong user
    result = post("/cart/evaluate", {
        "user_id": "u1", "amount": 1000, "coupon_codes": ["VIP25"],
    })
    assert result["final_amount"] == 1000
    assert result["applied_coupons"] == []
    print(f"[OK] VIP coupon wrong user: 1000 -> {result['final_amount']}")

    # 12. Evaluate cart — VIP coupon, correct user
    result = post("/cart/evaluate", {
        "user_id": "vip-user", "amount": 1000, "coupon_codes": ["VIP25"],
    })
    assert result["final_amount"] == 750  # 25% off
    assert result["applied_coupons"] == ["VIP25"]
    print(f"[OK] VIP coupon correct user: 1000 -> {result['final_amount']}")

    # 13. Delete coupon and verify
    delete(f"/coupons/{c1['coupon_id']}")
    result = post("/cart/evaluate", {
        "user_id": "u1", "amount": 1000, "coupon_codes": ["SUMMER10"],
    })
    assert result["final_amount"] == 1000
    assert result["applied_coupons"] == []
    print(f"[OK] Deleted coupon no longer applies: 1000 -> {result['final_amount']}")

    print("\n✅ All E2E tests passed!\n")


if __name__ == "__main__":
    main()
