# Scrapemate Integration

This package integrates `github.com/gosom/scrapemate` into the PEFY-TECH runtime as a governed, reusable crawling capability.

## Scope of This Integration

Included:

- Account-level skill definition: `skills/scrapemate/SKILL.md`.
- Slash command: `commands/scrapemate.md`.
- Mandatory governance rule: `rules/scraping-governance.md`.
- Linux/macOS installer: `scripts/install-scrapemate.sh`.
- Windows installer: `scripts/install-scrapemate.ps1`.

The approved default is Scrapemate `v1.0.0`, which is MIT-licensed and supports static HTTP crawling, configurable retries, caching, output writers, proxy support, screenshots, and JavaScript rendering through Playwright or Rod.

## Important Architectural Boundary

Scrapemate is a Go library, not a native ChatGPT plugin and not an MCP server. Therefore:

- The skill and command become available wherever this runtime plugin is installed.
- The Go dependency must still be provisioned on each execution host, container, workstation, or server that will run crawlers.
- No installation inside a chat account can silently deploy binaries to phones, computers, servers, or cloud environments.
- Live crawling requires explicit target scope, authorisation, and runtime access.

## Install on Linux or macOS

```bash
bash scripts/install-scrapemate.sh
```

Install Chromium support for JavaScript-rendered pages:

```bash
SCRAPEMATE_INSTALL_PLAYWRIGHT=1 bash scripts/install-scrapemate.sh
```

Custom workspace or version:

```bash
SCRAPEMATE_HOME="$HOME/.pefy/scrapemate" \
SCRAPEMATE_VERSION="v1.0.0" \
bash scripts/install-scrapemate.sh
```

## Install on Windows

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-scrapemate.ps1
```

With Chromium support:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-scrapemate.ps1 -InstallPlaywright
```

## Verification

The installer must create:

```text
~/.pefy/scrapemate/SCRAPEMATE-INSTALLATION.txt
```

or the equivalent Windows path. Verify the dependency directly:

```bash
go list -m -f '{{.Path}} {{.Version}}' github.com/gosom/scrapemate
```

Expected version:

```text
github.com/gosom/scrapemate v1.0.0
```

## Operating Model

1. Invoke `/scrapemate` with the business purpose, permitted domains, required fields, output destination, frequency, and retention.
2. Produce the allowlist, schema, limits, stop conditions, and risk controls.
3. Develop and test against fixtures or an authorised target.
4. Review privacy, security, terms, copyright, and data-retention obligations.
5. Run with monitoring and retain evidence of execution and output validation.
6. Disable and investigate on denial, throttling, scope escape, or unexpected sensitive data.

## Upgrade Control

Do not track the upstream `main` branch automatically. Upgrade the pinned version only after:

- Changelog and breaking-change review.
- Go toolchain compatibility check.
- Dependency and vulnerability scan.
- Static and browser-mode regression testing.
- Data-quality comparison.
- Rollback validation.

## Current Known Constraints

The upstream project has open issues involving inactivity handling and browser shutdown behaviour. Treat long-running browser workloads as requiring soak tests, bounded execution, cancellation handling, and external health monitoring before production use.
