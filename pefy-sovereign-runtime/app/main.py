from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import CashInput, LeadInput, RuntimeRequest, RuntimeResponse
from app.orchestrator import execute_runtime
from app.revenue import assess_cash, assess_lead

settings = get_settings()
app = FastAPI(
    title="PEFY-GG Universal AI Sovereign Runtime",
    version="0.1.0",
    description="Sovereign multi-provider orchestration for revenue, ROI, cash and advisory intelligence.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "PEFY-GG Universal AI Sovereign Runtime",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "environment": settings.pefy_env,
        "default_provider": settings.pefy_default_provider,
        "ai_enabled": settings.ai_enabled,
    }


@app.get("/.well-known/agent-card.json")
async def agent_card() -> dict[str, object]:
    return {
        "name": "PEFY-GG Revenue & Cash Sovereign Adviser",
        "description": "Qualifies opportunities, diagnoses cash, convenes advisers and produces controlled recommendations.",
        "url": "/v1/runtime/execute",
        "version": "0.1.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "skills": [
            {"id": "lead-qualification", "name": "Lead qualification and opportunity scoring"},
            {"id": "cash-diagnostic", "name": "Cash runway and 30-day gap diagnostic"},
            {"id": "advisory-council", "name": "Cross-functional advisory council"},
        ],
        "securitySchemes": {"bearer": {"type": "http", "scheme": "bearer"}},
    }


@app.post("/v1/lead/score")
async def lead_score(lead: LeadInput) -> dict[str, object]:
    result = assess_lead(lead)
    return {
        "score": result.score,
        "risk_level": result.risk_level,
        "recommendations": [item.model_dump() for item in result.recommendations],
    }


@app.post("/v1/cash/diagnose")
async def cash_diagnostic(cash: CashInput) -> dict[str, object]:
    result = assess_cash(cash)
    return {
        "runway_months": result.runway_months,
        "gap_30d_xof": result.gap_30d_xof,
        "risk_level": result.risk_level,
        "recommendations": [item.model_dump() for item in result.recommendations],
    }


@app.post("/v1/runtime/execute", response_model=RuntimeResponse)
async def runtime_execute(request: RuntimeRequest) -> RuntimeResponse:
    return await execute_runtime(request, settings)
