from fastapi import APIRouter, HTTPException

from coupon_system.enums import CouponType
from coupon_system.api.dependencies import promotion_service
from coupon_system.api.schemas import CreatePromotionRequest, PromotionResponse

router = APIRouter(prefix="/promotions", tags=["Promotions"])


def _to_response(promo) -> PromotionResponse:
    return PromotionResponse(
        promotion_id=promo.promotion_id, name=promo.name,
        discount_type=promo.discount_type.value,
        discount_value=promo.discount_value, rule_id=promo.rule_id,
    )


@router.post("", response_model=PromotionResponse)
def create_promotion(req: CreatePromotionRequest):
    try:
        discount_type = CouponType(req.discount_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid discount type: {req.discount_type}")

    promo = promotion_service.create_promotion(
        name=req.name, discount_type=discount_type,
        discount_value=req.discount_value, rule_id=req.rule_id,
    )
    return _to_response(promo)


@router.get("", response_model=list[PromotionResponse])
def list_promotions():
    return [_to_response(p) for p in promotion_service.get_promotions()]
