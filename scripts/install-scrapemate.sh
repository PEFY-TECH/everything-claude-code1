#!/usr/bin/env bash
set -Eeuo pipefail

SCRAPEMATE_VERSION="${SCRAPEMATE_VERSION:-v1.0.0}"
SCRAPEMATE_HOME="${SCRAPEMATE_HOME:-$HOME/.pefy/scrapemate}"
INSTALL_PLAYWRIGHT="${SCRAPEMATE_INSTALL_PLAYWRIGHT:-0}"

log() {
  printf '[scrapemate] %s\n' "$*"
}

fail() {
  printf '[scrapemate] ERROR: %s\n' "$*" >&2
  exit 1
}

command -v go >/dev/null 2>&1 || fail "Go is required. Install a supported Go toolchain, then rerun this script."

export GOTOOLCHAIN="${GOTOOLCHAIN:-auto}"

mkdir -p "$SCRAPEMATE_HOME"
cd "$SCRAPEMATE_HOME"

if [[ ! -f go.mod ]]; then
  log "Creating controlled Go workspace at $SCRAPEMATE_HOME"
  go mod init pefy.local/scrapemate-runtime >/dev/null
fi

log "Installing github.com/gosom/scrapemate@$SCRAPEMATE_VERSION"
go get "github.com/gosom/scrapemate@$SCRAPEMATE_VERSION"

if [[ "$INSTALL_PLAYWRIGHT" == "1" ]]; then
  log "Installing Playwright Chromium runtime"
  go run github.com/playwright-community/playwright-go/cmd/playwright@v0.5200.0 install --with-deps chromium
else
  log "Skipping browser installation. Set SCRAPEMATE_INSTALL_PLAYWRIGHT=1 when JavaScript rendering is required."
fi

INSTALLED_VERSION="$(go list -m -f '{{.Version}}' github.com/gosom/scrapemate)"
[[ -n "$INSTALLED_VERSION" ]] || fail "Scrapemate dependency verification failed."

cat > SCRAPEMATE-INSTALLATION.txt <<EOF
component=github.com/gosom/scrapemate
requested_version=$SCRAPEMATE_VERSION
installed_version=$INSTALLED_VERSION
workspace=$SCRAPEMATE_HOME
playwright_installed=$INSTALL_PLAYWRIGHT
installed_at_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF

log "Verified Scrapemate $INSTALLED_VERSION"
log "Workspace: $SCRAPEMATE_HOME"
log "Installation does not authorise scraping. Apply the repository governance rule before every live run."
