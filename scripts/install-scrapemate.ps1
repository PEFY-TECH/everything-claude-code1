param(
    [string]$Version = $(if ($env:SCRAPEMATE_VERSION) { $env:SCRAPEMATE_VERSION } else { "v1.0.0" }),
    [string]$InstallPath = $(if ($env:SCRAPEMATE_HOME) { $env:SCRAPEMATE_HOME } else { Join-Path $HOME ".pefy\scrapemate" }),
    [switch]$InstallPlaywright
)

$ErrorActionPreference = "Stop"

function Write-Log([string]$Message) {
    Write-Host "[scrapemate] $Message"
}

if (-not (Get-Command go -ErrorAction SilentlyContinue)) {
    throw "Go is required. Install a supported Go toolchain, then rerun this script."
}

if (-not $env:GOTOOLCHAIN) {
    $env:GOTOOLCHAIN = "auto"
}

New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
Push-Location $InstallPath

try {
    if (-not (Test-Path "go.mod")) {
        Write-Log "Creating controlled Go workspace at $InstallPath"
        & go mod init pefy.local/scrapemate-runtime | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "go mod init failed." }
    }

    Write-Log "Installing github.com/gosom/scrapemate@$Version"
    & go get "github.com/gosom/scrapemate@$Version"
    if ($LASTEXITCODE -ne 0) { throw "Scrapemate dependency installation failed." }

    if ($InstallPlaywright -or $env:SCRAPEMATE_INSTALL_PLAYWRIGHT -eq "1") {
        Write-Log "Installing Playwright Chromium runtime"
        & go run github.com/playwright-community/playwright-go/cmd/playwright@v0.5200.0 install --with-deps chromium
        if ($LASTEXITCODE -ne 0) { throw "Playwright Chromium installation failed." }
        $PlaywrightInstalled = "1"
    }
    else {
        Write-Log "Skipping browser installation. Use -InstallPlaywright when JavaScript rendering is required."
        $PlaywrightInstalled = "0"
    }

    $InstalledVersion = (& go list -m -f '{{.Version}}' github.com/gosom/scrapemate).Trim()
    if (-not $InstalledVersion) { throw "Scrapemate dependency verification failed." }

    $Timestamp = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
    @"
component=github.com/gosom/scrapemate
requested_version=$Version
installed_version=$InstalledVersion
workspace=$InstallPath
playwright_installed=$PlaywrightInstalled
installed_at_utc=$Timestamp
"@ | Set-Content -Path "SCRAPEMATE-INSTALLATION.txt" -Encoding UTF8

    Write-Log "Verified Scrapemate $InstalledVersion"
    Write-Log "Workspace: $InstallPath"
    Write-Log "Installation does not authorise scraping. Apply the repository governance rule before every live run."
}
finally {
    Pop-Location
}
