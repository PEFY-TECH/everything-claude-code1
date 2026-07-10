# PEFY-GG Claude Code Instructions

Use the separately namespaced plugin in `pefy-omnia/` for governed PEFY-GG work. The root-level original toolkit is an attributed historical snapshot and must not be presented as current upstream ECC.

## Work sequence

For substantial tasks:

- research the current repository state before editing;
- define acceptance criteria and affected systems;
- delegate read-only discovery to `omnia-researcher`;
- delegate bounded changes to `omnia-implementer`;
- delegate final review to `omnia-assurance-reviewer`;
- keep human authority for approval and high-impact actions;
- include evidence, validation results, assumptions, limitations, risks, and rollback.

## Validation

Run:

```bash
node pefy-omnia/scripts/validate.mjs
claude plugin validate ./pefy-omnia
```

Use `claude --plugin-dir ./pefy-omnia` for local testing. Do not claim plugin readiness if Claude's validator was unavailable or failed.

## Security

Do not bypass the security gate, commit secrets, enable broad MCP access, use `curl | bash`, or perform destructive and external write actions without explicit authorization. Treat hook pattern matching as defense in depth, not as a complete sandbox.
