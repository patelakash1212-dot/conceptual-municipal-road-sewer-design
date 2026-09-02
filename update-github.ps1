[CmdletBinding()]
param(
    [switch]$NoPush,
    [string]$Message = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = $PSScriptRoot
$SourcePdf = Join-Path $Repo "source\Project.pdf"
$Builder = Join-Path $Repo "scripts\build_portfolio.py"

if (-not (Test-Path -LiteralPath $SourcePdf)) {
    throw "Missing $SourcePdf. Copy your newly plotted multi-sheet PDF there and keep the name Project.pdf."
}

$UserProfilePath = [Environment]::GetFolderPath("UserProfile")
$BundledPython = Join-Path $UserProfilePath ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if (Test-Path -LiteralPath $BundledPython) {
    $Python = $BundledPython
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $Python = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $Python = "python"
} else {
    throw "Python 3 was not found. Install Python 3, Pillow, pypdf and reportlab."
}

Push-Location $Repo
try {
    if ($Python -eq "py") {
        & $Python -3 $Builder
    } else {
        & $Python $Builder
    }
    if ($LASTEXITCODE -ne 0) { throw "Portfolio build or PDF validation failed." }

    Write-Host ""
    Write-Host "QA preview: $Repo\qa-preview" -ForegroundColor Cyan
    Write-Host "Portfolio:   $Repo\docs\Municipal_Road_and_Sewer_Design_Portfolio.pdf" -ForegroundColor Cyan

    if ($NoPush) {
        Write-Host "Build complete. Nothing was committed or pushed (-NoPush)." -ForegroundColor Yellow
        exit 0
    }

    git add -- "docs/Municipal_Road_and_Sewer_Design_Portfolio.pdf" "assets/portfolio-cover.png" "assets/plan-profile-sample.png"
    $Pending = git diff --cached --name-only
    if (-not $Pending) {
        Write-Host "No generated portfolio changes were found; GitHub is already current." -ForegroundColor Green
        exit 0
    }

    if ([string]::IsNullOrWhiteSpace($Message)) {
        $Message = "Update municipal portfolio sheets $(Get-Date -Format 'yyyy-MM-dd')"
    }
    git commit -m $Message
    if ($LASTEXITCODE -ne 0) { throw "Git commit failed." }
    git push origin HEAD
    if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
    Write-Host "GitHub portfolio updated successfully." -ForegroundColor Green
}
finally {
    Pop-Location
}
