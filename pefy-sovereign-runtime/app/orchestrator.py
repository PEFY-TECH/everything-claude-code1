from uuid import uuid4

from app.advisory import convene_council
from app.config import Settings
from app.models import Recommendation, RiskLevel, RuntimeRequest, RuntimeResponse
from app.provider import build_provider
from app.revenue import assess_cash, assess_lead

RISK_ORDER = {
    RiskLevel.VERY_LOW: 1,
    RiskLevel.LOW: 2,
    RiskLevel.MEDIUM: 3,
    RiskLevel.HIGH: 4,
    RiskLevel.CRITICAL: 5,
}


async def execute_runtime(request: RuntimeRequest, settings: Settings) -> RuntimeResponse:
    recommendations: list[Recommendation] = []
    risks: list[RiskLevel] = []
    assumptions = [
        "Inputs are user-provided and have not been independently audited.",
        "Financial projections exclude taxes, financing costs and unreported obligations unless supplied.",
    ]
    unverified_claims: list[str] = []
    lead_score = None
    runway = None
    gap = None

    if request.lead:
        lead = assess_lead(request.lead)
        lead_score = lead.score
        risks.append(lead.risk_level)
        recommendations.extend(lead.recommendations)
        unverified_claims.append("Lead budget, authority and payment reliability require documentary confirmation.")

    if request.cash:
        cash = assess_cash(request.cash)
        runway = cash.runway_months
        gap = cash.gap_30d_xof
        risks.append(cash.risk_level)
        recommendations.extend(cash.recommendations)
        unverified_claims.append("Receivables and 30-day cash expectations require ledger and bank reconciliation.")

    if not recommendations:
        recommendations.extend(
            [
                Recommendation(
                    priority=5,
                    action="Define a measurable baseline for pipeline, margin, collections and cash.",
                    rationale="The runtime cannot optimize what is not instrumented.",
                    owner_role="Executive PMO + Finance + Sales",
                    horizon="10 business days",
                    expected_impact="Decision-grade baseline and accountable execution",
                ),
                Recommendation(
                    priority=4,
                    action="Select three priority client segments and create sector-specific offers.",
                    rationale="Concentration improves acquisition efficiency and proof reuse.",
                    owner_role="Strategy + Marketing + Sales",
                    horizon="30 days",
                    expected_impact="Higher qualified pipeline density",
                ),
            ]
        )
        risks.append(RiskLevel.MEDIUM)

    council = convene_council(
        request.objective,
        request.lead,
        request.cash,
        request.requested_advisers,
    )
    provider = build_provider(settings, request.use_ai_synthesis)
    synthesis = await provider.synthesize(
        objective=request.objective,
        recommendations=recommendations,
        council=council,
        assumptions=assumptions,
    )
    risk = max(risks, key=lambda item: RISK_ORDER[item])
    trace_id = str(uuid4())
    return RuntimeResponse(
        runtime_version="0.1.0",
        provider=provider.name,
        objective=request.objective,
        lead_score=lead_score,
        cash_runway_months=runway,
        cash_gap_30d_xof=gap,
        risk_level=risk,
        recommendations=sorted(recommendations, key=lambda item: item.priority, reverse=True),
        council=council,
        executive_synthesis=synthesis,
        human_approval_required=settings.pefy_require_human_approval,
        assumptions=assumptions,
        unverified_claims=unverified_claims,
        trace={
            "trace_id": trace_id,
            "runtime": "PEFY-GG Universal AI Sovereign Runtime",
            "mode": "RETRO-NOW-FUTURE",
            "controls": [
                "evidence-register",
                "assumption-register",
                "unverified-claim-log",
                "human-approval-gate",
            ],
        },
    )
