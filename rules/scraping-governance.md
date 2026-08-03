# Web Crawling and Scraping Governance

These controls apply to every crawler, scraper, browser-automation extractor, monitoring bot, and data-harvesting workflow.

## Authorisation

- Define the accountable owner, legitimate purpose, target scope, and intended downstream use before execution.
- Technical accessibility is not authorisation.
- Respect access controls, terms, robots directives, privacy obligations, copyright, database rights, and applicable law.

## Prohibited Behaviour

- No bypass of authentication, paywalls, CAPTCHAs, anti-bot controls, or technical restrictions.
- No credential collection, unauthorised private-data access, indiscriminate personal-data collection, or abusive high-volume extraction.
- No use intended to destabilise services, evade enforcement, impersonate users, or conceal unlawful activity.

## Default Technical Controls

- Domain allowlist required.
- Static HTTP before browser automation.
- Concurrency limited to 1-3 requests per domain unless formally approved.
- Bounded timeouts, maximum three retries, exponential backoff, and jitter.
- Explicit stop on repeated 401, 403, 429, CAPTCHA, block pages, or scope escape.
- Cache, deduplication, schema validation, provenance, and structured logging enabled where relevant.
- Secrets and sensitive payloads excluded from repositories, logs, screenshots, and artifacts.

## Data Governance

- Collect only necessary fields.
- Classify data before storage.
- Define retention and deletion.
- Encrypt sensitive outputs and apply least-privilege access.
- Preserve source URL, retrieval timestamp, parser version, schema version, and processing status.

## Readiness Gate

Production use requires documented scope, tests, risk review, data-quality controls, monitoring, rollback, and evidence of owner acceptance.
