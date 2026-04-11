import os
import aerospike

from coupon_system.repositories import RuleRepository, CouponRepository, PromotionRepository
from coupon_system.services import RuleService, CouponService, PromotionService

AEROSPIKE_HOST = os.environ.get("AEROSPIKE_HOST", "localhost")
AEROSPIKE_PORT = int(os.environ.get("AEROSPIKE_PORT", "3000"))

config = {"hosts": [(AEROSPIKE_HOST, AEROSPIKE_PORT)]}
as_client = aerospike.client(config).connect()

rule_repo = RuleRepository(as_client)
coupon_repo = CouponRepository(as_client)
promotion_repo = PromotionRepository(as_client)

rule_service = RuleService(rule_repo)
coupon_service = CouponService(rule_service, coupon_repo)
promotion_service = PromotionService(rule_service, promotion_repo)
