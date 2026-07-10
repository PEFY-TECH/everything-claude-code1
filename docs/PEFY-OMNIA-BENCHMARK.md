# PEFY-GG OMNIA Agent OS — Benchmark and Controlled Improvement Assessment

**Assessment date:** 2026-07-10  
**Repository:** `PEFY-TECH/everything-claude-code1`  
**Assessed baseline:** `main` at `432485ba6b92c14fb357276a98957f348bcff9ee`  
**Improvement branch:** `agent/pefy-omnia-agent-os-v1`

## Executive finding

The baseline is a useful January 2026 snapshot of the former Everything Claude Code project, with agents, skills, commands, rules, memory hooks, cross-platform Node.js scripts, and a small test suite. It is not current with the upstream project as of July 2026 and should not be activated account-wide without adaptation.

The original upstream repository has since moved to `affaan-m/ECC` and describes ECC 2.0 as a cross-harness agent operating system with materially expanded install, orchestration, security, repair, validation, and operator capabilities. The PEFY repository therefore needs either a controlled upstream synchronization strategy or a clearly separated PEFY overlay. This change implements the overlay approach to avoid an uncontrolled mass merge.

## Evidence reviewed

- Baseline README and plugin structure.
- Baseline plugin and marketplace manifests.
- Baseline hook configuration and MCP examples.
- Baseline commits through 2026-01-23.
- Current upstream ECC README and commits through 2026-07-09.
- Current Claude Code plugin, hook, subagent, and skill conventions.
- Current Codex `AGENTS.md` instruction-layer convention.

## Baseline strengths

1. Clear modular separation of agents, skills, commands, rules, hooks, scripts, contexts, and MCP examples.
2. Cross-platform Node.js conversion and package-manager detection.
3. Session memory, strategic compaction, verification-loop, and continuous-learning concepts.
4. Existing security reviewer, code reviewer, TDD, architecture, and planning roles.
5. MIT license and an extensible plugin layout.

## Material gaps

### 1. Currency and upstream divergence — Severity 5 / Critical

The PEFY snapshot stopped in January 2026. The upstream project was renamed to ECC and reached a documented 2.0 line in June 2026, followed by active July 2026 changes. Directly presenting the snapshot as current would create compatibility, security, and expectation risk.

**Control implemented:** a separately namespaced `pefy-omnia-agent-os` overlay with explicit attribution and a documented non-synchronization limitation.

### 2. Marketplace identity and provenance — Severity 4 / High

The PEFY-hosted marketplace still identifies the original author as the marketplace owner and points plugin metadata to the old upstream repository. That is appropriate for attribution of the original plugin but not for the PEFY marketplace or a PEFY-developed extension.

**Control implemented:** register the original plugin with preserved attribution and add a distinct PEFY plugin entry owned and maintained by PEFY-TECH.

### 3. Hook portability and false positives — Severity 4 / High

The baseline claims cross-platform support but includes behavior that forces `tmux`, blocks most Markdown and text-file creation, and embeds complex one-line Node scripts in JSON. These defaults are opinionated, difficult to test, and likely to create false positives or portability failures.

**Control implemented:** dependency-light external Node.js hook logic, current simple matcher syntax, structured deny decisions, and deterministic allow/deny tests.

### 4. Secret and MCP activation risk — Severity 5 / Critical

The baseline MCP example instructs operators to replace literal placeholders with actual tokens in JSON. It also uses unpinned `npx -y` and `@latest` packages. Copying this configuration can encourage secrets in local files, supply-chain drift, unnecessary context use, and excessive tool privileges.

**Control implemented:** the PEFY plugin auto-enables no MCP server, stores no credentials, requires environment-variable or secret-manager use, and prescribes role-scoped MCP access.

### 5. Independent assurance and human authority — Severity 4 / High

The baseline contains review roles but does not enforce separation between authoring and assurance or reserve final approval for a designated human authority.

**Control implemented:** separate researcher, implementer, and assurance reviewer contracts; evidence-based readiness labels; human-only approval.

### 6. System-of-systems and cross-functional governance — Severity 4 / High

The baseline is primarily software-development oriented. It lacks a transversal operating model for business, finance, legal, QSE, cybersecurity, data, product, marketing, operations, and organizational transformation.

**Control implemented:** a system-of-systems orchestration skill with human/AI operating modes, Retro/Now/Future layers, interfaces, decision authority, KPIs, risk controls, and stop conditions.

### 7. Release validation — Severity 4 / High

The baseline test suite does not validate the new PEFY-specific architecture because it did not exist.

**Control implemented:** a standalone validator and GitHub Actions workflow that check required files, JSON syntax, agent and skill frontmatter, and security-gate scenarios.

## Comparative maturity score

Scale: 1 = ad hoc, 2 = repeatable, 3 = defined, 4 = controlled, 5 = optimized.

| Capability | Baseline | PEFY overlay target | Evidence / control |
|---|---:|---:|---|
| Current upstream alignment | 1 | 3 | Explicit overlay and synchronization decision required |
| Plugin structure | 3 | 4 | Separate manifest, settings, agents, skills, hooks |
| Cross-harness guidance | 1 | 4 | `AGENTS.md` plus `CLAUDE.md` |
| Role and permission separation | 2 | 4 | Research / implement / assurance contracts |
| Security and secret controls | 2 | 4 | Pre-tool deny gate and no automatic MCP activation |
| Evidence-based assurance | 2 | 4 | Benchmark and readiness skill |
| System-of-systems orchestration | 1 | 4 | Dedicated orchestration skill and default agent |
| Automated validation | 2 | 4 | Node validator and CI workflow |
| Account-wide activation safety | 1 | 3 | Staged rollout and rollback; local environment validation still required |

## Implemented architecture

```text
PEFY marketplace
└── pefy-omnia-agent-os
    ├── settings.json -> omnia-orchestrator
    ├── agents
    │   ├── omnia-orchestrator
    │   ├── omnia-researcher      [read-only]
    │   ├── omnia-implementer     [bounded write]
    │   └── omnia-assurance-reviewer [read-only]
    ├── skills
    │   ├── system-of-systems-orchestration
    │   ├── benchmark-assure-finalize
    │   └── secure-activation
    ├── hooks
    │   └── PreToolUse security gate
    └── scripts
        ├── security-gate.mjs
        └── validate.mjs
```

## Verification requirements

Before merge:

```bash
node pefy-omnia/scripts/validate.mjs
claude plugin validate ./pefy-omnia
claude --plugin-dir ./pefy-omnia
```

Required manual scenarios:

1. Confirm the default main agent is `omnia-orchestrator`.
2. Confirm each subagent appears and respects its tool restrictions.
3. Confirm safe Bash and file-write operations continue normally.
4. Confirm destructive commands and literal secrets are denied with a clear reason.
5. Confirm plugin uninstall or disable restores the prior Claude Code behavior.
6. Confirm no MCP server or credential is activated automatically.

## Residual risks

- The PEFY fork remains behind ECC 2.0; the overlay does not import all upstream capabilities.
- Pattern-based secret detection can produce false negatives and false positives.
- GitHub Actions cannot validate a user's local Claude Code version, enterprise policy, OS permissions, or MCP credentials.
- The default main-agent setting changes behavior while the plugin is enabled and requires operator awareness.
- Account-wide activation requires staged pilot evidence and managed rollback.

## Recommended roadmap

### Phase 1 — Controlled pilot

Merge the overlay after CI and local Claude validation. Pilot it in one non-production repository and collect denied-command, false-positive, cycle-time, rework, and evidence-completeness metrics.

### Phase 2 — Upstream strategy

Choose one:

- periodically rebase from ECC with a documented compatibility matrix;
- retain the lightweight PEFY overlay and consume selected upstream releases as dependencies;
- create a new clean PEFY repository that references ECC rather than carrying a stale snapshot.

### Phase 3 — Enterprise controls

Add managed MCP allowlists, signed release artifacts, dependency pinning, secret scanning, SBOM/provenance, policy-as-code, release approvals, and organization-level deployment documentation.

### Phase 4 — Cross-domain skill mesh

Add separately governed skill packs for DevSecOps, QSE/ISO, project management, finance, legal review, data analysis, product design, marketing, language services, and institutional documentation. Keep each pack progressively disclosed and activated only when relevant.

## Readiness decision

**CONDITIONALLY READY for pull-request review and local pilot validation.**  
Not approved for account-wide or production activation until CI passes, `claude plugin validate` passes on a current Claude Code installation, manual permission scenarios are completed, and a designated human authority approves rollout.
