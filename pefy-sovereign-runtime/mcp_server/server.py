from mcp.server.fastmcp import FastMCP

from app.models import CashInput, LeadInput
from app.revenue import assess_cash, assess_lead

mcp = FastMCP("PEFY-GG Universal AI Sovereign Runtime")


@mcp.tool()
def score_client_opportunity(
    company: str,
    sector: str,
    country: str,
    estimated_value_xof: float,
    strategic_fit: int,
    urgency: int,
    access_to_decision_maker: int,
    budget_confidence: int,
    payment_reliability: int,
    delivery_complexity: int,
    notes: str = "",
) -> dict[str, object]:
    """Score a potential client opportunity and return cash-protective next actions."""
    result = assess_lead(
        LeadInput(
            company=company,
            sector=sector,
            country=country,
            estimated_value_xof=estimated_value_xof,
            strategic_fit=strategic_fit,
            urgency=urgency,
            access_to_decision_maker=access_to_decision_maker,
            budget_confidence=budget_confidence,
            payment_reliability=payment_reliability,
            delivery_complexity=delivery_complexity,
            notes=notes,
        )
    )
    return {
        "score": result.score,
        "risk_level": result.risk_level,
        "recommendations": [item.model_dump() for item in result.recommendations],
    }


@mcp.tool()
def diagnose_cash_position(
    cash_available_xof: float,
    monthly_fixed_cost_xof: float,
    monthly_variable_cost_xof: float,
    receivables_xof: float,
    overdue_receivables_xof: float,
    payables_due_30d_xof: float,
    expected_collections_30d_xof: float,
    expected_sales_cash_30d_xof: float,
) -> dict[str, object]:
    """Calculate runway, 30-day cash gap and prioritized cash actions."""
    result = assess_cash(
        CashInput(
            cash_available_xof=cash_available_xof,
            monthly_fixed_cost_xof=monthly_fixed_cost_xof,
            monthly_variable_cost_xof=monthly_variable_cost_xof,
            receivables_xof=receivables_xof,
            overdue_receivables_xof=overdue_receivables_xof,
            payables_due_30d_xof=payables_due_30d_xof,
            expected_collections_30d_xof=expected_collections_30d_xof,
            expected_sales_cash_30d_xof=expected_sales_cash_30d_xof,
        )
    )
    return {
        "runway_months": result.runway_months,
        "gap_30d_xof": result.gap_30d_xof,
        "risk_level": result.risk_level,
        "recommendations": [item.model_dump() for item in result.recommendations],
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
