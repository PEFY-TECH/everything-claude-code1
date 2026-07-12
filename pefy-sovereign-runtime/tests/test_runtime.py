import asyncio

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.advisory import convene_council
from app.config import Settings
from app.main import app
from app.models import CashInput, LeadInput, Recommendation, RuntimeRequest
from app.orchestrator import execute_runtime
from app.provider import RulesProvider, build_provider


def make_lead() -> LeadInput:
    return LeadInput(
        company="Priority Client",
        sector="Infrastructure",
        country="Côte d'Ivoire",
        estimated_value_xof=80_000_000,
        strategic_fit=4,
        urgency=4,
        access_to_decision_maker=3,
        budget_confidence=3,
        payment_reliability=3,
        delivery_complexity=4,
    )


def make_cash() -> CashInput:
    return CashInput(
        cash_available_xof=20_000_000,
        monthly_fixed_cost_xof=7_000_000,
        monthly_variable_cost_xof=3_000_000,
        receivables_xof=45_000_000,
        overdue_receivables_xof=15_000_000,
        payables_due_30d_xof=8_000_000,
        expected_collections_30d_xof=12_000_000,
        expected_sales_cash_30d_xof=6_000_000,
    )


def test_cash_rejects_inconsistent_overdue_amount() -> None:
    with pytest.raises(ValidationError):
        CashInput(
            cash_available_xof=1,
            monthly_fixed_cost_xof=1,
            monthly_variable_cost_xof=0,
            receivables_xof=10,
            overdue_receivables_xof=11,
            payables_due_30d_xof=0,
            expected_collections_30d_xof=0,
            expected_sales_cash_30d_xof=0,
        )


def test_council_default_and_specialist_selection() -> None:
    default = convene_council("Improve cash", make_lead(), make_cash(), [])
    assert len(default) == 5
    specialist = convene_council(
        "Secure the runtime", None, None, ["cybersecurity", "data", "unknown"]
    )
    assert [item.adviser for item in specialist] == [
        "Cybersecurity & Sovereignty Adviser",
        "Data, BI & Forecasting Adviser",
    ]
    assert all(item.confidence == 0.72 for item in specialist)


def test_rules_provider_and_provider_fallback() -> None:
    settings = Settings(pefy_default_provider="openai", openai_api_key=None)
    provider = build_provider(settings, requested_ai=True)
    assert isinstance(provider, RulesProvider)
    text = asyncio.run(
        provider.synthesize(
            objective="Improve collectible revenue",
            recommendations=[
                Recommendation(
                    priority=5,
                    action="Collect overdue invoices",
                    rationale="Cash first",
                    owner_role="Finance",
                    horizon="48 hours",
                    expected_impact="Improved liquidity",
                )
            ],
            council=[],
            assumptions=[],
        )
    )
    assert "human approval" in text


def test_runtime_executes_full_controlled_flow() -> None:
    settings = Settings(pefy_default_provider="rules", pefy_require_human_approval=True)
    response = asyncio.run(
        execute_runtime(
            RuntimeRequest(
                objective="Increase qualified revenue and protect 90-day cash conversion.",
                lead=make_lead(),
                cash=make_cash(),
                requested_advisers=["strategy", "finance", "legal", "risk"],
            ),
            settings,
        )
    )
    assert response.provider == "rules"
    assert response.lead_score is not None
    assert response.cash_runway_months == 2
    assert response.human_approval_required is True
    assert response.trace["trace_id"]
    assert response.unverified_claims


def test_runtime_without_financial_inputs_builds_baseline_actions() -> None:
    response = asyncio.run(
        execute_runtime(
            RuntimeRequest(objective="Create a disciplined PEFY-GG client acquisition baseline."),
            Settings(),
        )
    )
    assert response.risk_level == "medium"
    assert len(response.recommendations) == 2


def test_http_health_scoring_and_agent_card() -> None:
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    card = client.get("/.well-known/agent-card.json")
    assert card.status_code == 200
    assert len(card.json()["skills"]) == 3
    scored = client.post("/v1/lead/score", json=make_lead().model_dump())
    assert scored.status_code == 200
    assert scored.json()["score"] > 0
    cash = client.post("/v1/cash/diagnose", json=make_cash().model_dump())
    assert cash.status_code == 200
    assert cash.json()["runway_months"] == 2
