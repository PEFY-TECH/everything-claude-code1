# PEFY-GG Repository Agent Instructions

These instructions apply to Codex and other agent harnesses that read `AGENTS.md`.

## Repository purpose

This repository contains an attributed snapshot of Everything Claude Code plus a separately namespaced PEFY-GG OMNIA Agent OS overlay under `pefy-omnia/`. Preserve upstream attribution and license notices. Do not imply that the PEFY overlay is the current upstream ECC distribution.

## Default operating method

For substantial work:

1. Inspect before modifying.
2. State objective, scope, constraints, affected systems, and acceptance criteria.
3. Separate research, implementation, and independent assurance.
4. Make the smallest coherent change.
5. Run deterministic validation and report observed results.
6. Record assumptions, unverified claims, security impact, residual risks, and rollback.
7. Use `NOT READY`, `CONDITIONALLY READY`, or `READY FOR REVIEW`; only a human authority may mark work approved.

## Security boundaries

- Never commit literal secrets, private keys, credentials, or personal access tokens.
- Do not use opaque download-and-execute pipelines.
- Do not enable all MCP servers by default.
- Use least privilege and task-scoped tools.
- Require human confirmation for destructive, irreversible, production, financial, legal, identity, security, publication, and external write operations.
- Preserve sandbox, permission, branch-protection, and review controls.

## Required checks for PEFY OMNIA changes

Run:

```bash
node pefy-omnia/scripts/validate.mjs
```

When Claude Code is available, also run:

```bash
claude plugin validate ./pefy-omnia
```

Review `.claude-plugin/marketplace.json` whenever the plugin name, source, or distribution metadata changes.

## Change discipline

- Use a feature branch and pull request.
- Keep original toolkit changes separate from `pefy-omnia/` unless a compatibility fix requires both.
- Add tests for changed security-gate behavior.
- Do not weaken a deny rule without documenting the threat, false-positive evidence, replacement control, and rollback.
- Update `pefy-omnia/README.md` and the benchmark document when architecture or activation behavior changes.
