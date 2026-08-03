---
description: Design, install, validate, or operate a governed Scrapemate crawler with explicit scope, rate limits, data controls, and evidence.
---

# Scrapemate Command

Use `/scrapemate` for approved Go-based crawling and structured data extraction with `github.com/gosom/scrapemate`.

## Required Inputs

- Business purpose.
- Target domain or URL list.
- Required fields.
- Access authorisation.
- Maximum frequency and concurrency.
- Output format and destination.
- Retention period.

When details are absent, create a safe draft with visible placeholders. Do not run against a live target until scope and authorisation are established.

## Execution Flow

1. Confirm target scope and owner.
2. Check terms, robots directives, privacy, copyright, and contractual constraints.
3. Produce a domain allowlist and stop conditions.
4. Define the output schema and provenance fields.
5. Prefer static HTTP extraction; enable browser rendering only when required.
6. Generate or update the Go crawler using Scrapemate `v1.0.0`.
7. Add bounded concurrency, timeout, retry, backoff, cache, deduplication, and structured logging.
8. Test against fixtures or an authorised target.
9. Validate schema, completeness, duplicates, rate limits, denial handling, and secret hygiene.
10. Produce the runbook, evidence register, and disable/rollback steps.

## Installation

Linux/macOS:

```bash
bash scripts/install-scrapemate.sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-scrapemate.ps1
```

The installer provisions the dependency in a controlled local workspace. It does not create permission to scrape any website.

## Stop Conditions

Stop immediately on repeated `401`, `403`, `429`, CAPTCHA, block pages, unexpected authentication prompts, scope escape, or uncertain data classification.

## Completion Standard

Report separately:

- Installed and verified components.
- Components prepared but not executed.
- Live-target tests actually performed.
- Remaining approvals, credentials, infrastructure, or legal checks.
