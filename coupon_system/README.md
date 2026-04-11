# Coupon Management Service

A rule-based coupon and promotion system with REST APIs.

## Features

- Create rules with configurable comparators (EQ, GTE, LTE)
- Create coupons (flat / percentage) linked to rules
- Create promotions with auto-applied discounts
- Evaluate cart with multiple stacked coupons (FIFO order)
- Min cart value enforcement per coupon

## Setup

```bash
pip install fastapi uvicorn requests
```

## Run the server

```bash
# From the project root (parent of coupon_system/)
uvicorn coupon_system.api.app:app --port 8000
```

Swagger docs: http://localhost:8000/docs

## Run unit tests

```bash
python -m coupon_system.main
```

## Run E2E API tests

Start the server first, then in another terminal:

```bash
python -m coupon_system.test_api
```

## API Endpoints

### Rules
- `POST /rules` — Create a rule
- `GET /rules/{rule_id}` — Get a rule

### Coupons
- `POST /coupons` — Create a coupon
- `GET /coupons/{coupon_code}` — Get coupon by code
- `PUT /coupons/{coupon_id}` — Update a coupon
- `DELETE /coupons/{coupon_id}` — Delete a coupon

### Promotions
- `POST /promotions` — Create a promotion
- `GET /promotions` — List all promotions

### Cart
- `POST /cart/evaluate` — Evaluate cart with coupon codes

## Example: Full checkout flow

```bash
# 1. Create a rule (amount >= 500)
curl -X POST http://localhost:8000/rules \
  -H "Content-Type: application/json" \
  -d '{"variable": "amount", "value": 500, "comparator": "GTE"}'
# Returns: {"rule_id": "<id>", ...}

# 2. Create a coupon (10% off, min cart 200)
curl -X POST http://localhost:8000/coupons \
  -H "Content-Type: application/json" \
  -d '{"coupon_code": "SAVE10", "value": 10, "coupon_type": "PERCENTAGE", "min_cart_value": 200, "rule_id": "<rule_id>"}'

# 3. Evaluate cart
curl -X POST http://localhost:8000/cart/evaluate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "amount": 1000, "coupon_codes": ["SAVE10"]}'
# Returns: {"original_amount": 1000, "final_amount": 900, "applied_coupons": ["SAVE10"]}
```
