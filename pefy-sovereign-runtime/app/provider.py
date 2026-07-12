import json
from typing import Protocol

from openai import AsyncOpenAI

from app.config import Settings
from app.models import AdviserOpinion, Recommendation


class SynthesisProvider(Protocol):
    name: str

    async def synthesize(
        self,
        *,
        objective: str,
        recommendations: list[Recommendation],
        council: list[AdviserOpinion],
        assumptions: list[str],
    ) -> str: ...


class RulesProvider:
    name = "rules"

    async def synthesize(
        self,
        *,
        objective: str,
        recommendations: list[Recommendation],
        council: list[AdviserOpinion],
        assumptions: list[str],
    ) -> str:
        top = sorted(recommendations, key=lambda item: item.priority, reverse=True)[:3]
        actions = "; ".join(item.action for item in top)
        return (
            f"For the objective '{objective}', execute the highest-priority controls first: {actions}. "
            "Treat all financial impacts as estimates until verified against source records and obtain "
            "human approval before external commitment."
        )


class OpenAIProvider:
    name = "openai"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for the OpenAI provider")
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.pefy_openai_model

    async def synthesize(
        self,
        *,
        objective: str,
        recommendations: list[Recommendation],
        council: list[AdviserOpinion],
        assumptions: list[str],
    ) -> str:
        payload = {
            "objective": objective,
            "recommendations": [item.model_dump() for item in recommendations],
            "council": [item.model_dump() for item in council],
            "assumptions": assumptions,
        }
        response = await self._client.responses.create(
            model=self._model,
            instructions=(
                "You are the PEFY-GG executive synthesis layer. Produce a concise, evidence-conscious "
                "action brief focused on revenue quality, ROI, cash conversion, risk and human approval. "
                "Do not invent facts, clients, amounts or legal conclusions."
            ),
            input=json.dumps(payload, ensure_ascii=False),
        )
        return response.output_text.strip()


def build_provider(settings: Settings, requested_ai: bool) -> SynthesisProvider:
    if requested_ai and settings.ai_enabled:
        return OpenAIProvider(settings)
    return RulesProvider()
