---
name: scrapemate
description: Use this skill to design, implement, review, or operate governed web-crawling and structured-data extraction workflows with github.com/gosom/scrapemate. Activate for Go-based crawlers, JavaScript-rendered pages, selector extraction, caching, retries, CSV/data sinks, and controlled browser automation.
---

# Scrapemate Governed Crawling Skill

## Purpose

Use Scrapemate as the Go crawling engine for approved PEFY-GG research, monitoring, evidence collection, testing, interoperability, and data-ingestion workflows.

Reference implementation: `github.com/gosom/scrapemate`.

Default approved version: `v1.0.0`. Upgrade only after dependency, compatibility, licence, security, and regression review.

## Mandatory Intake

Before generating or running a crawler, establish:

1. Business purpose and accountable owner.
2. Target domains and exact URL scope.
3. Data fields required and retention period.
4. Legal basis, site terms, robots directives, and contractual restrictions.
5. Authentication status and whether the operator is authorised to access the content.
6. Rate limit, concurrency, retry ceiling, and operating window.
7. Output classification, destination, encryption, and access control.
8. Acceptance criteria, evidence requirements, and deletion procedure.

Do not infer permission from technical accessibility.

## Non-Negotiable Controls

- Do not bypass authentication, paywalls, CAPTCHAs, access controls, or anti-bot protections.
- Do not collect credentials, special-category personal data, private communications, or unnecessary personal data.
- Do not perform abusive, indiscriminate, high-volume, or destabilising scraping.
- Use an explicit identifying user agent and a monitored contact channel when appropriate.
- Apply least-data, least-frequency, least-retention, and least-privilege principles.
- Respect domain allowlists, robots directives, terms, copyright, database rights, privacy requirements, and applicable law.
- Stop on repeated `401`, `403`, `429`, CAPTCHA, block pages, legal notices, or unexpected authentication prompts.
- Never place secrets, cookies, session tokens, proxy credentials, or customer data in source control.
- Record provenance: source URL, retrieval timestamp, parser version, schema version, and processing status.

## Engineering Baseline

Use these defaults unless the approved design requires stricter values:

- Concurrency: `1-3` per domain.
- Request timeout: `10-30 seconds`.
- Retries: maximum `3`, with capped exponential backoff and jitter.
- Cache: enabled for development, testing, and repeatable evidence collection.
- JavaScript rendering: disabled unless static HTTP extraction is insufficient.
- Screenshots: only for evidence or debugging; redact sensitive content before retention.
- Output: structured schema with validation before storage.
- Logging: no secrets or full sensitive payloads.
- Idempotency: deterministic job IDs and deduplication keys.
- Failure mode: fail closed when scope, permission, or destination is uncertain.

## Browser Engines

Scrapemate `v1.0.0` supports Playwright by default and Rod through the `rod` build tag.

Use static HTTP first. Use Playwright when deterministic browser control or multi-browser behaviour is required. Use Rod when a smaller Chromium-only deployment is preferable and the project has validated its behaviour.

## Required Deliverables

Every production crawler must include:

- Approved scope manifest.
- Data dictionary and output schema.
- Domain allowlist.
- Rate-limit and retry policy.
- Error and stop-condition handling.
- Test fixtures or a permitted staging target.
- Data-quality checks.
- Security and privacy review.
- Operations runbook and rollback/disable procedure.
- Evidence register and execution log.

## Validation Gate

A crawler is ready only when:

- It cannot navigate outside the allowlist.
- It honours configured delays and concurrency.
- It stops correctly on denial or throttling signals.
- Its output schema validates.
- Duplicate and partial records are handled.
- Secrets do not appear in code, logs, screenshots, or artifacts.
- The owner has accepted retention, deletion, and downstream-use controls.

## Invocation Pattern

When the user invokes Scrapemate, return or implement:

1. Scope and control summary.
2. Proposed extraction schema.
3. Crawler architecture.
4. Safe implementation.
5. Test and validation results.
6. Risks, limitations, and operating instructions.

Do not claim that a crawler ran unless execution evidence is available.
