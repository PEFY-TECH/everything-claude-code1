from dataclasses import dataclass

from app.models import CashInput, LeadInput, Recommendation, RiskLevel


@dataclass(frozen=True)
class LeadAssessment:
    score: float
    risk_level: RiskLevel
    recommendations: list[Recommendation]


@dataclass(frozen=True)
class CashAssessment:
    runway_months: float
    gap_30d_xof: float
    risk_level: RiskLevel
    recommendations: list[Recommendation]


def assess_lead(lead: LeadInput) -> LeadAssessment:
    positive = (
        lead.strategic_fit * 0.25
        + lead.urgency * 0.15
        + lead.access_to_decision_maker * 0.20
        + lead.budget_confidence * 0.20
        + lead.payment_reliability * 0.20
    )
    complexity_penalty = max(0, lead.delivery_complexity - 3) * 0.25
    score = round(max(0, min(100, ((positive - complexity_penalty) / 5) * 100)), 1)

    if score >= 80:
        risk = RiskLevel.LOW
    elif score >= 65:
        risk = RiskLevel.MEDIUM
    elif score >= 45:
        risk = RiskLevel.HIGH
    else:
        risk = RiskLevel.CRITICAL

    actions: list[Recommendation] = []
    if lead.access_to_decision_maker < 4:
        actions.append(
            Recommendation(
                priority=5,
                action="Secure direct access to the economic decision-maker.",
                rationale="Conversion probability is constrained without sponsor and budget authority access.",
                owner_role="Business Development Lead",
                horizon="7 days",
                expected_impact="Higher win rate and shorter sales cycle",
            )
        )
    if lead.budget_confidence < 4:
        actions.append(
            Recommendation(
                priority=5,
                action="Validate budget source, procurement route and payment calendar before proposal effort.",
                rationale="This prevents non-funded pipeline and protects bid cost.",
                owner_role="Finance + Sales",
                horizon="Before proposal",
                expected_impact="Lower acquisition waste and cash risk",
            )
        )
    if lead.payment_reliability < 4:
        actions.append(
            Recommendation(
                priority=5,
                action="Use milestone billing, advance payment and suspension rights.",
                rationale="Commercial value without collectability does not create cash.",
                owner_role="Finance + Legal",
                horizon="Contracting",
                expected_impact="Improved DSO and downside protection",
            )
        )
    if lead.delivery_complexity >= 4:
        actions.append(
            Recommendation(
                priority=4,
                action="Price complexity explicitly and gate scope changes through formal change control.",
                rationale="High delivery complexity can destroy contribution margin.",
                owner_role="Project Director",
                horizon="Proposal and delivery",
                expected_impact="Protected gross margin",
            )
        )
    actions.append(
        Recommendation(
            priority=4,
            action="Build a three-option offer: diagnostic, core transformation and managed service.",
            rationale="Tiered packaging supports entry, upsell and recurring revenue.",
            owner_role="Offer & Pricing Council",
            horizon="10 days",
            expected_impact="Higher average contract value and lifetime value",
        )
    )
    return LeadAssessment(score=score, risk_level=risk, recommendations=actions)


def assess_cash(cash: CashInput) -> CashAssessment:
    monthly_burn = cash.monthly_fixed_cost_xof + cash.monthly_variable_cost_xof
    runway = round(cash.cash_available_xof / monthly_burn, 2)
    projected_30d = (
        cash.cash_available_xof
        + cash.expected_collections_30d_xof
        + cash.expected_sales_cash_30d_xof
        - cash.payables_due_30d_xof
        - monthly_burn
    )
    gap = round(min(0, projected_30d), 2)
    overdue_ratio = cash.overdue_receivables_xof / cash.receivables_xof if cash.receivables_xof else 0

    if runway < 1 or gap < 0:
        risk = RiskLevel.CRITICAL
    elif runway < 2 or overdue_ratio >= 0.50:
        risk = RiskLevel.HIGH
    elif runway < 4 or overdue_ratio >= 0.25:
        risk = RiskLevel.MEDIUM
    else:
        risk = RiskLevel.LOW

    actions = [
        Recommendation(
            priority=5,
            action="Run a 13-week rolling cash forecast with weekly owner sign-off.",
            rationale="Cash control requires visibility by date, payer, obligation and confidence level.",
            owner_role="CFO / Treasury Adviser",
            horizon="Immediate and weekly",
            expected_impact="Earlier cash-gap detection",
        )
    ]
    if cash.overdue_receivables_xof > 0:
        actions.append(
            Recommendation(
                priority=5,
                action="Launch a segmented collection sprint on overdue receivables.",
                rationale="Existing receivables are usually the fastest lower-cost cash source.",
                owner_role="Collections Cell",
                horizon="48 hours",
                expected_impact=f"Cash recovery pool up to {cash.overdue_receivables_xof:,.0f} XOF",
            )
        )
    if gap < 0:
        actions.append(
            Recommendation(
                priority=5,
                action="Close the 30-day funding gap through collections, deposits, rescheduling and cost freeze.",
                rationale="The projected outflow exceeds reliable available cash.",
                owner_role="Executive Cash War Room",
                horizon="72 hours",
                expected_impact=f"Close {-gap:,.0f} XOF gap",
            )
        )
    actions.append(
        Recommendation(
            priority=4,
            action="Require advance or milestone payments for new projects and recurring retainers.",
            rationale="Revenue quality improves when contractual cash timing funds delivery.",
            owner_role="Sales + Finance + Legal",
            horizon="All new contracts",
            expected_impact="Reduced working-capital requirement",
        )
    )
    return CashAssessment(
        runway_months=runway,
        gap_30d_xof=gap,
        risk_level=risk,
        recommendations=actions,
    )
