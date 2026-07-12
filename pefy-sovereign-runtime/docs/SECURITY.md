# Security Baseline

- Secrets are environment variables, never repository content.
- Production must use TLS, least-privilege service credentials and secret rotation.
- Add authentication before exposing write-capable tools or sensitive client data.
- Keep provider keys isolated by environment and workload.
- Log trace IDs and decisions, but redact prompts, PII, financial records and credentials.
- Apply input size limits, schema validation, rate limiting and origin allowlists.
- Run dependency, SAST and container scans before production promotion.
- Treat the previously pasted API key as compromised and revoke it.
