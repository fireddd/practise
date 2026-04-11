from fastapi import FastAPI

from coupon_system.api.routes import rules, coupons, promotions, cart

app = FastAPI(title="Coupon Management Service")

app.include_router(rules.router)
app.include_router(coupons.router)
app.include_router(promotions.router)
app.include_router(cart.router)


@app.get("/health")
def health():
    return {"status": "ok"}
