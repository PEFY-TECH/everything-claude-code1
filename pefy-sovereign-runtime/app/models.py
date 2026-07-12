from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class RiskLevel(StrEnum):
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LeadInput(BaseModel):
    company: str = Field(min_length=2, max_length=200)
    sector: str = Field(min_length=2, max_length=120)
    country: str = Field(min_length=2, max_length=120)
    estimated_value_xof: float = Field(ge=0)
    strategic_fit: int = Field(ge=1, le=5)
    urgency: int = Field(ge=1, le=5)
    access_to_decision_maker: int = Field(ge=1, le=5)
    budget_confidence: int = Field(ge=1, le=5)
    payment_reliability: int = Field(ge=1, le=5)
    delivery_complexity: int = Field(ge=1, le=5)
    notes: str = Field(default="", max_length=4000)


class CashInput(BaseModel):
    cash_available_xof: float = Field(ge=0)
    monthly_fixed_cost_xof: float = Field(gt=0)
    monthly_variable_cost_xof: float = Field(ge=0)
    receivables_xof: float = Field(ge=0)
    overdue_receivables_xof: float = Field(ge=0)
    payables_due_30d_xof: float = Field(ge=0)
    expected_collections_30d_xof: float = Field(ge=0)
    expected_sales_cash_30d_xof: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_overdue_receivables(self) -> "CashInput":
        if self.overdue_receivables_xof > self.receivables_xof:
            raise ValueError("overdue_receivables_xof cannot exceed receivables_xof")
        return self


class RuntimeRequest(BaseModel):
    objective: str = Field(min_length=10, max_length=5000)
    lead: LeadInput | None = None
    cash: CashInput | None = None
    constraints: list[str] = Field(default_factory=list, max_length=20)
    requested_advisers: list[str] = Field(default_factory=list, max_length=20)
    use_ai_synthesis: bool = False


class Recommendation(BaseModel):
    priority: int = Field(ge=1, le=5)
    action: str
    rationale: str
    owner_role: str
    horizon: str
    expected_impact: str
    evidence_status: str = "rule-derived"


class AdviserOpinion(BaseModel):
    adviser: str
    position: str
    key_risk: str
    recommendation: str
    confidence: float = Field(ge=0, le=1)


class RuntimeResponse(BaseModel):
    runtime_version: str
    provider: str
    objective: str
    lead_score: float | None = None
    cash_runway_months: float | None = None
    cash_gap_30d_xof: float | None = None
    risk_level: RiskLevel
    recommendations: list[Recommendation]
    council: list[AdviserOpinion]
    executive_synthesis: str
    human_approval_required: bool
    assumptions: list[str]
    unverified_claims: list[str]
    trace: dict[str, Any]
