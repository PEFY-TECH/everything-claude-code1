# PEFY-GG OMNIA Agent OS

A governed system-of-systems activation layer for Claude Code and compatible agent workflows. It complements the repository's original Everything Claude Code snapshot without replacing or misrepresenting the upstream project.

## What this plugin adds

- a default `omnia-orchestrator` main agent;
- read-only research, bounded implementation, and independent assurance subagents;
- system-of-systems workflow design;
- evidence-based benchmark, audit, fix, and readiness gates;
- secure activation controls for hooks, plugins, MCP servers, and account-level automation;
- a deterministic pre-tool security gate;
- a dependency-free validation harness and GitHub Actions check;
- cross-harness repository instructions through `AGENTS.md` and Claude-specific instructions through `CLAUDE.md`.

## Safe operating model

The plugin separates three duties:

1. **Research** — read-only discovery and evidence collection.
2. **Implementation** — bounded changes against explicit acceptance criteria.
3. **Assurance** — independent review without editing the implementation.

The default readiness vocabulary is:

- `NOT READY`
- `CONDITIONALLY READY`
- `READY FOR REVIEW`
- `APPROVED` — human authority only

## Test locally

From the repository root:

```bash
node pefy-omnia/scripts/validate.mjs
claude plugin validate ./pefy-omnia
claude --plugin-dir ./pefy-omnia
```

Inside Claude Code, verify the active agent and invoke the skills:

```text
/context
/pefy-omnia-agent-os:system-of-systems-orchestration
/pefy-omnia-agent-os:benchmark-assure-finalize
/pefy-omnia-agent-os:secure-activation
```

## Install from the PEFY marketplace

After this branch is reviewed and merged:

```text
/plugin marketplace add PEFY-TECH/everything-claude-code1
/plugin install pefy-omnia-agent-os@everything-claude-code
/reload-plugins
```

The plugin's `settings.json` activates `omnia-orchestrator` as the main agent while the plugin is enabled.

## Security defaults

The plugin does **not** auto-enable MCP servers or store credentials. Add MCP servers by role and task, preferably scoped to a subagent. Keep write-capable production tools disabled until explicitly required.

The pre-tool security gate blocks:

- recursive deletion of root or home paths;
- filesystem formatting and raw disk writes;
- host shutdown or reboot commands;
- opaque `curl | bash`, `wget | sh`, and similar pipelines;
- uncontrolled `git push --force`;
- obvious private keys and literal credentials written to files.

It permits reviewed alternatives such as `git push --force-with-lease` and placeholder values in `.example`, `.sample`, and template files.

## Staged activation

Use this rollout sequence:

1. **Local validation** — run the dependency-free validator.
2. **Local plugin test** — use `claude --plugin-dir ./pefy-omnia`.
3. **Pilot project** — enable for one non-production repository.
4. **Independent assurance** — review hook behavior, permissions, logs, and false positives.
5. **Controlled user activation** — install from the marketplace.
6. **Account or team rollout** — only after operator training, rollback testing, and managed MCP policy.

## Rollback

Disable or uninstall `pefy-omnia-agent-os`, then reload plugins. The plugin does not modify project files during installation and does not auto-configure external credentials or MCP servers.

## Validation

```bash
node pefy-omnia/scripts/validate.mjs
```

The validator checks required files, JSON schemas at the syntax level, agent and skill frontmatter, and security-gate scenarios. Claude's own validator remains mandatory before release:

```bash
claude plugin validate ./pefy-omnia
```

## Current limitations

- This is a controlled PEFY overlay, not a full synchronization with ECC 2.0.
- The CI environment validates structure and deterministic security cases but cannot confirm a user's local Claude installation or external MCP credentials.
- Security pattern matching is a defense-in-depth control, not a replacement for sandboxing, permissions, code review, secret scanning, endpoint protection, or human authorization.
