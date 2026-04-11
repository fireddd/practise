# Coupon Management Service

A rule-based coupon and promotion system with REST APIs.

## Features

- Create rules with configurable comparators (EQ, GTE, LTE)
- Create coupons (flat / percentage) linked to rules
- Create promotions with auto-applied discounts
- Evaluate cart with multiple stacked coupons (FIFO order)
- Min cart value enforcement per coupon

## Run with Docker (recommended)

Requires Docker Desktop.

```bash
cd coupon_system
docker compose up --build -d
```

This starts:
- **Aerospike** (database) on port 3000
- **FastAPI app** on port 8000

Swagger docs: http://localhost:8000/docs

To stop:

```bash
docker compose down
```

## Run locally (without Docker)

```bash
pip install fastapi uvicorn requests aerospike
```

Requires a running Aerospike instance with a `coupon_system` namespace.

```bash
# Set Aerospike host (defaults to localhost:3000)
export AEROSPIKE_HOST=localhost
export AEROSPIKE_PORT=3000

# From the project root (parent of coupon_system/)
uvicorn coupon_system.api.app:app --port 8000
```

Swagger docs: http://localhost:8000/docs

## Testing

### Unit tests (no server needed)

```bash
python -m coupon_system.main
```

This runs 6 phases of tests:

| Phase | What it tests |
|-------|--------------|
| 1 | Enums + Models — instantiate all entities, verify fields |
| 2 | Comparator + Rule Evaluation — EQ, GTE, LTE with passing/failing contexts |
| 3 | Discount Calculators — flat (with floor at 0), percentage, factory lookup |
| 4 | RuleService + CouponService CRUD — create, fetch, update, delete |
| 5 | Cart Evaluation — single coupon, stacked coupons (FIFO), rule failure, min_cart_value check, unknown codes |
| 6 | PromotionService — create, list, apply, rule failure, stacked promotions |

### E2E API tests (requires running server)

Start the server in one terminal:

```bash
uvicorn coupon_system.api.app:app --port 8000
```

Run the test script in another terminal:

```bash
python -m coupon_system.test_api
```

This tests the full API flow:

| Test | Scenario | Expected |
|------|----------|----------|
| Health check | `GET /health` | `{"status": "ok"}` |
| Create + fetch rules | Amount rule (GTE) and user_id rule (EQ) | Rules returned with correct fields |
| Coupon CRUD | Create, fetch by code, update value, delete | All operations succeed, deleted coupon returns 404 |
| Promotions | Create "Chocolate Sale", list all | Promotion persisted and listed |
| Single coupon | Cart 1000, apply SUMMER10 (15% off) | Final: 850 |
| Stacked coupons | Cart 1000, apply SUMMER10 then FLAT100 | Final: 750 (FIFO order) |
| Rule fails | Cart 200, rule requires >= 500 | No discount, final: 200 |
| VIP coupon, wrong user | user_id doesn't match rule | No discount, final: 1000 |
| VIP coupon, correct user | user_id matches | 25% off, final: 750 |
| Deleted coupon | Apply coupon after deletion | No discount, final: 1000 |

### Manual curl testing

After starting the server, you can test individual endpoints:

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

## curl examples for every endpoint

```bash
# --- Rules ---

# Create a rule (amount >= 500)
curl -X POST http://localhost:8000/rules \
  -H "Content-Type: application/json" \
  -d '{"variable": "amount", "value": 500, "comparator": "GTE"}'
# -> {"rule_id": "<id>", "variable": "amount", "value": 500, "comparator": "GTE"}

# Create a user-based rule (user_id == "vip-user")
curl -X POST http://localhost:8000/rules \
  -H "Content-Type: application/json" \
  -d '{"variable": "user_id", "value": "vip-user", "comparator": "EQ"}'

# Get a rule
curl http://localhost:8000/rules/<rule_id>

# --- Coupons ---

# Create a percentage coupon
curl -X POST http://localhost:8000/coupons \
  -H "Content-Type: application/json" \
  -d '{"coupon_code": "SAVE10", "value": 10, "coupon_type": "PERCENTAGE", "min_cart_value": 200, "rule_id": "<rule_id>"}'

# Create a flat coupon
curl -X POST http://localhost:8000/coupons \
  -H "Content-Type: application/json" \
  -d '{"coupon_code": "FLAT50", "value": 50, "coupon_type": "FLAT", "min_cart_value": 100, "rule_id": "<rule_id>"}'

# Get coupon by code
curl http://localhost:8000/coupons/SAVE10

# Update coupon value
curl -X PUT http://localhost:8000/coupons/<coupon_id> \
  -H "Content-Type: application/json" \
  -d '{"value": 15}'

# Delete a coupon
curl -X DELETE http://localhost:8000/coupons/<coupon_id>

# --- Promotions ---

# Create a promotion
curl -X POST http://localhost:8000/promotions \
  -H "Content-Type: application/json" \
  -d '{"name": "Chocolate Sale", "discount_type": "PERCENTAGE", "discount_value": 20, "rule_id": "<rule_id>"}'

# List all promotions
curl http://localhost:8000/promotions

# --- Cart Evaluation ---

# Single coupon
curl -X POST http://localhost:8000/cart/evaluate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "amount": 1000, "coupon_codes": ["SAVE10"]}'
# -> {"original_amount": 1000, "final_amount": 900, "applied_coupons": ["SAVE10"]}

# Multiple coupons (FIFO: SAVE10 applied first, then FLAT50)
curl -X POST http://localhost:8000/cart/evaluate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "amount": 1000, "coupon_codes": ["SAVE10", "FLAT50"]}'
# -> {"original_amount": 1000, "final_amount": 850, "applied_coupons": ["SAVE10", "FLAT50"]}
```
