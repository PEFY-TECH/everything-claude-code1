# PEFY-GG Universal AI Sovereign Runtime™

Executable reference implementation of the sovereign, provider-neutral orchestration layer for Dr Erick Franck PATHINVO and PEFY-GG.

## Implemented capabilities

- Revenue opportunity scoring based on strategic fit, authority, budget, payment reliability and delivery complexity.
- Cash runway and 30-day funding-gap diagnostics in XOF.
- Virtual advisory council covering strategy, finance, sales, legal, risk and optional specialists.
- Evidence, assumptions, unverified-claim and human-approval controls.
- OpenAI synthesis when explicitly enabled; deterministic rules remain available without an API key.
- FastAPI/OpenAPI service, MCP tools and A2A-compatible agent discovery card.
- Docker and Vercel deployment manifests.

## Quick start

```bash
cd pefy-sovereign-runtime
cp .env.example .env
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## AI activation

Keep the key outside Git:

```bash
PEFY_DEFAULT_PROVIDER=openai
OPENAI_API_KEY=<secret managed by the deployment platform>
PEFY_OPENAI_MODEL=gpt-5-mini
```

The service remains operational in `rules` mode without a provider key.

## API example

```bash
curl -X POST http://127.0.0.1:8000/v1/runtime/execute \
  -H 'Content-Type: application/json' \
  -d '{
    "objective": "Increase collectible revenue and protect 90-day cash for PEFY-GG.",
    "use_ai_synthesis": false,
    "cash": {
      "cash_available_xof": 20000000,
      "monthly_fixed_cost_xof": 7000000,
      "monthly_variable_cost_xof": 3000000,
      "receivables_xof": 45000000,
      "overdue_receivables_xof": 15000000,
      "payables_due_30d_xof": 8000000,
      "expected_collections_30d_xof": 12000000,
      "expected_sales_cash_30d_xof": 6000000
    }
  }'
```

## MCP server

```bash
uv run python -m mcp_server.server
```

Tools: `score_client_opportunity` and `diagnose_cash_position`.

## Deployment gates

1. Revoke any key pasted in chat or logs.
2. Inject a newly rotated key as an encrypted environment variable.
3. Enable authentication, rate limiting and audit storage before handling confidential client data.
4. Validate preview deployment, then promote the same artifact to production.
5. Human approval remains mandatory for official offers, pricing, contracts and financial decisions.
