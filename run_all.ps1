<#:
.SYNOPSIS
  End-to-end pipeline for Pearson's Four project.
.DESCRIPTION
  Runs the complete data pipeline: scrape -> clean -> analyze -> visualize -> test.
  Usage: .\run_all.ps1 [-SkipScrape] [-SkipViz] [-SkipTests] [-SkipDashboard]
#>

param(
    [switch]$SkipScrape,
    [switch]$SkipViz,
    [switch]$SkipTests,
    [switch]$SkipDashboard
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSCommandPath
Set-Location $root

Write-Host "=" x 60
Write-Host "PEARSON'S FOUR — END-TO-END PIPELINE"
Write-Host ("=" x 60)
Write-Host ""

# 1. Scrape Spain salary data
if (-not $SkipScrape) {
    Write-Host "`n[1/5] Scraping Spain salary data..."
    python scripts/scrape_spain_salaries.py
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Scrape failed, continuing..."; }
} else {
    Write-Host "`n[1/5] Skipped: Scrape"
}

# 2. Run INE pipeline
Write-Host "`n[2/5] Building INE salary pipeline..."
python scripts/build_real_salary_pipeline.py
if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Pipeline failed, continuing..."; }

# 3. Verify metrics
Write-Host "`n[3/5] Verifying statistical metrics..."
python scripts/verify_all_metrics.py
if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Verification failed, continuing..."; }

# 4. Generate visualizations (Matplotlib/Seaborn)
if (-not $SkipViz) {
    Write-Host "`n[4/6] Generating static visualizations..."
    python scripts/generate_visualizations.py
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Viz generation failed, continuing..."; }
} else {
    Write-Host "`n[4/6] Skipped: Static visualizations"
}

# 5. Generate interactive visualizations (Plotly)
if (-not $SkipViz) {
    Write-Host "`n[5/6] Generating interactive Plotly visualizations..."
    python scripts/generate_plotly_viz.py
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Plotly viz generation failed, continuing..."; }
} else {
    Write-Host "`n[5/6] Skipped: Interactive visualizations"
}

# 6. Run tests
if (-not $SkipTests) {
    Write-Host "`n[6/6] Running tests..."
    uv run pytest tests/ -v --tb=short
    if ($LASTEXITCODE -ne 0) { Write-Host "⚠ Some tests failed"; }
} else {
    Write-Host "`n[6/6] Skipped: Tests"
}

# Optional: launch dashboard
if (-not $SkipDashboard) {
    Write-Host "`n`nDashboard: run 'uv run streamlit run dashboard/app.py' to launch"
}

Write-Host ""
Write-Host ("=" x 60)
Write-Host "Pipeline complete."
