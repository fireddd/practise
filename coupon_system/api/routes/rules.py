from fastapi import APIRouter, HTTPException

from coupon_system.enums import Comparator
from coupon_system.api.dependencies import rule_service
from coupon_system.api.schemas import CreateRuleRequest, RuleResponse

router = APIRouter(prefix="/rules", tags=["Rules"])


@router.post("", response_model=RuleResponse)
def create_rule(req: CreateRuleRequest):
    try:
        comparator = Comparator(req.comparator)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid comparator: {req.comparator}")

    rule = rule_service.create_rule(req.variable, req.value, comparator)
    return RuleResponse(
        rule_id=rule.rule_id, variable=rule.variable,
        value=rule.value, comparator=rule.comparator.value,
    )


@router.get("/{rule_id}", response_model=RuleResponse)
def get_rule(rule_id: str):
    rule = rule_service.get_rule(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return RuleResponse(
        rule_id=rule.rule_id, variable=rule.variable,
        value=rule.value, comparator=rule.comparator.value,
    )
