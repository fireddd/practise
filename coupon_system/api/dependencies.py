from coupon_system.services import RuleService, CouponService, PromotionService

rule_service = RuleService()
coupon_service = CouponService(rule_service)
promotion_service = PromotionService(rule_service)
