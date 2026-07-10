---
description: Safely activate plugins, agents, hooks, MCP servers, automation, and account-level workflows using least privilege, validation, rollback, and supply-chain controls.
---

# Secure Activation

Use this skill whenever enabling an agent runtime, plugin, hook, MCP server, automation, background process, marketplace, or account-wide configuration.

## Before activation

1. Confirm the source, maintainer, license, commit or version, and intended scope.
2. Review executable scripts, hooks, install commands, dependencies, network endpoints, and update behavior.
3. Identify secrets, credentials, personal data, production access, destructive capabilities, and external data flows.
4. Define the minimum permissions, directories, tools, MCP servers, and duration required.
5. Back up the current configuration and document a rollback procedure.

## Supply-chain controls

- Prefer official registries, signed releases, pinned versions, checksums, and verified repositories.
- Do not execute `curl | sh`, `wget | bash`, unreviewed PowerShell download-and-execute commands, or opaque binaries.
- Avoid `@latest` for production activation unless a controlled update policy and validation pipeline exist.
- Do not place literal secrets in version-controlled JSON, Markdown, scripts, examples, or prompts.
- Use environment-variable references, secret managers, short-lived tokens, and least-privilege scopes.

## MCP controls

- Enable MCP servers by role or task, not all at once.
- Prefer subagent-scoped MCP access where the parent does not need the tool descriptions or credentials.
- Maintain allowlists and denylists for servers and write-capable tools.
- Separate read-only discovery from write actions.
- Require explicit human confirmation for production, financial, legal, identity, security, deletion, publication, and irreversible operations.

## Hook controls

- Use current documented matcher syntax and structured JSON decisions.
- Keep hooks deterministic, fast, cross-platform, and dependency-light.
- Test allow and deny paths.
- Avoid broad hooks that block normal documentation, force a specific terminal multiplexer, or mutate files unexpectedly.
- Fail safely and emit actionable reasons.

## Activation gate

Activation is allowed only when:

- schemas validate;
- required files and commands exist;
- security tests pass;
- no obvious secrets are committed;
- permissions are minimized;
- backup and rollback are documented;
- the operator understands what becomes automatic.

Use CONDITIONALLY READY for pilot activation. Use staged rollout before account-wide or production activation.
