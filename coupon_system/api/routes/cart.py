from fastapi import APIRouter

from coupon_system.models.cart import Cart
from coupon_system.api.dependencies import coupon_service
from coupon_system.api.schemas import EvaluateCartRequest, EvaluateCartResponse

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/evaluate", response_model=EvaluateCartResponse)
def evaluate_cart(req: EvaluateCartRequest):
    cart = Cart(user_id=req.user_id, amount=req.amount)
    final_amount, applied_coupons = coupon_service.evaluate_cart(cart, req.coupon_codes)
    return EvaluateCartResponse(
        original_amount=req.amount,
        final_amount=final_amount,
        applied_coupons=applied_coupons,
    )
