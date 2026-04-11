from fastapi import APIRouter, HTTPException

from coupon_system.enums import CouponType
from coupon_system.api.dependencies import coupon_service
from coupon_system.api.schemas import CreateCouponRequest, UpdateCouponRequest, CouponResponse

router = APIRouter(prefix="/coupons", tags=["Coupons"])


def _to_response(coupon) -> CouponResponse:
    return CouponResponse(
        coupon_id=coupon.coupon_id, coupon_code=coupon.coupon_code,
        value=coupon.value, coupon_type=coupon.coupon_type.value,
        min_cart_value=coupon.min_cart_value, rule_id=coupon.rule_id,
    )


@router.post("", response_model=CouponResponse)
def create_coupon(req: CreateCouponRequest):
    try:
        coupon_type = CouponType(req.coupon_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid coupon type: {req.coupon_type}")

    coupon = coupon_service.create_coupon(
        coupon_code=req.coupon_code, value=req.value,
        coupon_type=coupon_type, min_cart_value=req.min_cart_value,
        rule_id=req.rule_id,
    )
    return _to_response(coupon)


@router.get("/{coupon_code}", response_model=CouponResponse)
def get_coupon(coupon_code: str):
    coupon = coupon_service.get_coupon(coupon_code)
    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return _to_response(coupon)


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(coupon_id: str, req: UpdateCouponRequest):
    updates = req.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    coupon = coupon_service.update_coupon(coupon_id, **updates)
    if coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return _to_response(coupon)


@router.delete("/{coupon_id}")
def delete_coupon(coupon_id: str):
    deleted = coupon_service.delete_coupon(coupon_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return {"detail": "Coupon deleted"}
