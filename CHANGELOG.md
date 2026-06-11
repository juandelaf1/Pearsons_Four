# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] — 2026-06-08

### Added
- Title normalization: 1,037 unique titles mapped to 15 standard roles (99.8% capture rate)
- `scripts/normalize_titles.py` — extraction of role + seniority from raw job titles
- `data/linkedin_data_normalized.csv` — dataset with `role_normalized` and `seniority` columns
- ROADMAP.md with full milestone tracking (Phase 1, 2, 3)
- CHANGELOG.md (this file)
- `.github/ISSUE_TEMPLATE/` — bug report, feature request, task templates
- `.github/PULL_REQUEST_TEMPLATE.md`

### Changed
- README restructured as executive portfolio: KPIs table, corrected metrics, bilingual credits

## [2.0.0] — 2026-06-07

### Added
- `pyproject.toml` with `uv` dependency management (79 packages)
- Modular data pipeline (`scripts/pipeline/`: config, loaders ×3, clean_normalize, enrich_countries)
- Streamlit interactive dashboard (`dashboard/app.py`)
- Unit tests (9 tests: config, cleaning, enrichment)
- Plotly interactive visualizations (`scripts/generate_plotly_viz.py`, 5 HTML charts)
- E2E pipeline orchestrator (`run_all.ps1`)
- GitHub Actions CI workflow (`.github/workflows/ci.yml`)
- Spain tech salary study (5-source scraper + INE official data)
- Tableau Public data export scripts
- `docs/PROYECTO_DETALLADO.md` (from team repo)
- `notebooks/Auditoria_Pearson_4_CORREGIDO.ipynb` (Plotly refactor)

### Fixed
- INE salary parser: dot vs comma decimal ambiguity resolved
- `enrich_countries()`: now handles missing columns gracefully
- Pipeline relative imports corrected

### Changed
- `.gitignore` extended with `.pytest_cache/`, `*.px`, `data/espana/_debug_*.html`
- README updated with Spain study, pipeline docs, new structure

## [1.0.0] — 2026-06-02

### Added
- Unified merge: LinkedIn EDA + Spain study + docs/scripts
- Verified corrected metrics (Data Roles only)
- Spain data scrapers (Manfred, INE, Glassdoor, Tecnoempleo, Ticjob)

## [0.5.0] — 2026-05-28

### Added
- Visualization screenshots
- Enhanced notebook with corrected metrics

## [0.4.0] — 2026-05-27

### Added
- Stack Overflow bias analysis notebook (Vanessa)
- Cross-dataset comparison

## [0.3.0] — 2026-05-25

### Added
- README, GUIDE.md, issue templates, Trello backup
- Initial repo structure

## [0.1.0] — 2026-05-25

### Added
- Initial commit (Anas Fady)
- LinkedIn EDA notebook base
