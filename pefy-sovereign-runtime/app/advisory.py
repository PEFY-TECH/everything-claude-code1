from app.models import AdviserOpinion, CashInput, LeadInput

ADVISERS = {
    "strategy": "Strategy & Portfolio Adviser",
    "finance": "Finance, Treasury & ROI Adviser",
    "sales": "Enterprise Sales & Negotiation Adviser",
    "marketing": "Market Intelligence & Acquisition Adviser",
    "legal": "Legal, Contract & IP Adviser",
    "risk": "Risk, Compliance & Audit Adviser",
    "operations": "Operations & Delivery Adviser",
    "cybersecurity": "Cybersecurity & Sovereignty Adviser",
    "data": "Data, BI & Forecasting Adviser",
}


def convene_council(
    objective: str,
    lead: LeadInput | None,
    cash: CashInput | None,
    requested: list[str],
) -> list[AdviserOpinion]:
    selected = [key for key in requested if key in ADVISERS] or [
        "strategy",
        "finance",
        "sales",
        "legal",
        "risk",
    ]
    opinions: list[AdviserOpinion] = []
    for key in selected:
        if key == "finance":
            position = "Prioritize collectible cash, contribution margin and funded delivery over nominal revenue."
            risk = "Growth can consume cash when payment terms and delivery costs are misaligned."
            recommendation = "Apply cash-adjusted ROI and milestone billing to every opportunity."
        elif key == "sales":
            position = "Focus effort on decision access, funded urgency and a quantified business case."
            risk = "Large but unqualified opportunities can crowd out executable deals."
            recommendation = "Use a gated pipeline and next-action discipline with economic buyers."
        elif key == "legal":
            position = "Commercial acceleration must preserve IP, payment rights and scope boundaries."
            risk = "Weak contracts transfer financing and delivery risk to PEFY-GG."
            recommendation = "Standardize deposits, acceptance criteria, change control and suspension clauses."
        elif key == "risk":
            position = "No major recommendation should pass without evidence, assumptions and residual-risk review."
            risk = "False-positive readiness may create financial, legal or reputational loss."
            recommendation = "Maintain evidence and assumption registers with mandatory human approval."
        elif key == "strategy":
            position = "Concentrate resources on offers where PEFY-GG has differentiated proof and repeatability."
            risk = "Portfolio dispersion dilutes cash, execution quality and market credibility."
            recommendation = "Rank offers by margin, cash velocity, strategic fit and repeatability."
        elif key == "marketing":
            position = "Build account-based acquisition around priority sectors and measurable client pain."
            risk = "Generic visibility does not guarantee qualified pipeline."
            recommendation = "Create sector-specific proof assets and conversion funnels."
        elif key == "operations":
            position = "Sell only what can be delivered with controlled capacity and reusable assets."
            risk = "Overcommitment can erase margin and damage trust."
            recommendation = "Use capacity gates, standard work packages and delivery health KPIs."
        elif key == "cybersecurity":
            position = "Keep secrets out of code and enforce least privilege across agents, tools and data."
            risk = "Agentic integrations expand the attack surface and potential data leakage."
            recommendation = "Use isolated credentials, audit logs, allowlists and approval gates."
        else:
            position = "Instrument the revenue-to-cash chain with auditable operational data."
            risk = "Decisions degrade when pipeline and cash data are incomplete or stale."
            recommendation = "Define a governed KPI dictionary and automated data-quality checks."
        confidence = 0.86 if lead or cash else 0.72
        opinions.append(
            AdviserOpinion(
                adviser=ADVISERS[key],
                position=position,
                key_risk=risk,
                recommendation=recommendation,
                confidence=confidence,
            )
        )
    return opinions
