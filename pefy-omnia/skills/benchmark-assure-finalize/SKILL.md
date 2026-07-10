---
description: Benchmark, cross-check, test, audit, and finalize substantial deliverables without false-positive readiness. Use before release, deployment, submission, publication, or executive validation.
---

# Benchmark, Assure, Finalize

Use an evidence-based gate. Optimism is not evidence.

## Gate 1 — Specification integrity

Verify that the objective, scope, requirements, constraints, acceptance criteria, interfaces, and decision authority are explicit. Record ambiguities as assumptions; do not silently convert them into facts.

## Gate 2 — Evidence register

For every material claim, identify one of:

- direct repository or system evidence;
- deterministic test result;
- authoritative external source;
- stakeholder-approved assumption;
- unverified claim requiring validation.

## Gate 3 — Benchmark

Compare the deliverable against relevant baselines:

- official vendor or standards guidance;
- current upstream or reference implementation;
- repository conventions and compatibility requirements;
- security and privacy good practice;
- operational cost, maintainability, portability, and recovery expectations.

State where the benchmark is fully met, partially met, not met, or not applicable.

## Gate 4 — Verification

Run the smallest sufficient verification set:

- syntax and schema validation;
- unit, integration, end-to-end, or scenario tests;
- lint, type, build, and dependency checks;
- security and secret scanning;
- negative, boundary, failure, and rollback tests;
- documentation and operator-path verification.

Report the exact commands and observed results. Do not claim a test ran when it did not.

## Gate 5 — Independent review

Use a reviewer that did not author the implementation. Review findings by severity:

1. Very Low / Trivial
2. Low / Minor
3. Medium / Moderate
4. High / Major
5. Critical / Severe

For high-stakes work, score Likelihood 1-5 x Impact 1-5 and record inherent risk, controls, residual risk, owner, and treatment.

## Gate 6 — Fix and re-test

Correct accepted findings, rerun affected checks, and update the evidence register. Do not close a finding merely because a change was made; close it only when evidence demonstrates resolution.

## Gate 7 — Readiness decision

Use only:

- NOT READY — material requirements, evidence, controls, or tests are missing or failed.
- CONDITIONALLY READY — usable under explicit conditions, limitations, and human validation.
- READY FOR REVIEW — evidence supports independent stakeholder review.
- APPROVED — reserved for the designated human authority.

The final output must include scope, benchmark summary, validation results, open findings, assumptions, unverified claims, residual risks, rollback path, and readiness status.
