# Pearsons Four — EDA Data Science Job Salaries

<p align="center">
  <img src="screenshots/Logo (2).png" alt="Pearsons Four Banner" width="800">
</p>

**Full-stack data analysis project: LinkedIn job market + Stack Overflow bias + Spain tech salary study.**

---

## Executive Summary

| KPI | Value |
|-----|-------|
| Datasets analyzed | 3 (LinkedIn 123K rows, SO Survey 49K, Spain 5 sources) |
| Clean records (LinkedIn data roles) | **616** |
| Mean salary (data roles) | **$142,936 USD** |
| Median salary (data roles) | **$136,422 USD** |
| Experience → Salary correlation | **r = 0.49** (moderate-strong, p < 0.00001) |
| Views → Applies correlation | **r = 0.91** (strong) |
| Remote premium (data roles) | **-1.2%** (p = 0.46, not significant) |
| Salary MNAR rate | **70.87%** missing in LinkedIn |
| Spain tech avg (INE 2024) | **€42,742** (+44.7% vs national €29,540) |
| Spain regional spread | Madrid €35,170 ↔ Extremadura €23,194 |
| Interactive charts | **5 Plotly HTML** + **11 static** + **1 Streamlit dashboard** |
| Data pipeline modules | **6** (config, loaders × 3, clean, enrich) |
| Test coverage | **9 unit tests** (config, cleaning, enrichment) |

---

## Key Findings

### Market Intelligence
- **Salary predictor:** Experience level is the dominant factor (ANOVA p < 0.00001). Mid-Senior to Director jump = **+$72K**
- **Remote work:** No salary premium for data roles (-1.2%, p = 0.46). Earlier +45% finding was an aggregation artifact across all professions
- **Traffic conversion:** Views → Applies correlates strongly (r = 0.91). Visibility drives applications
- **Spain context:** INE Sector J (tech) averages €42,742 — 44.7% above the national mean. Data Scientist ranges: €25K (junior) to €75K (senior)

### Data Quality & Bias
- **MNAR salaries:** 70.87% of LinkedIn postings hide salary. Juniors disproportionately affected (47.33% hide vs 23.86% seniors) → models underestimate entry-level compensation
- **Geographic bias:** 0 postings from Spain in the LinkedIn Kaggle dataset. US/UK overrepresented
- **Selection bias:** 83.81% Senior/Experienced vs 16.19% Junior → ML models penalize junior profiles by lack of training data
- **Skills sparsity:** 98.03% missing `skills_desc` → conditional probability analysis limited to Stack Overflow

### Methodology Corrected
Initial analysis calculated metrics on all LinkedIn postings (~75K salaries). **Corrected metrics** isolate **Data Roles only** (616 records), eliminating aggregation bias:

| Metric | All Professions (original) | Data Roles Only (corrected) |
|--------|---------------------------|---------------------------|
| Remote premium | +45.1% | **-1.2%** (p=0.46) |
| Views → Applies | r = 0.62 | **r = 0.91** |
| Experience → Salary | r = 0.43 | **r = 0.49** |

---

## Datasets

| Dataset | Source | Rows | Purpose |
|---------|--------|------|---------|
| **LinkedIn Job Postings** | Kaggle (arshkon) | 123,849 | Main EDA: salaries, skills, industries |
| **Stack Overflow Survey 2025** | Stack Overflow | 49,191 | Bias analysis (MNAR, demographics) |
| **Spain Tech Salaries** | Manfred 2026 + INE + Glassdoor + Tecnoempleo + Ticjob + InfoJobs + Indeed | 149 salaries + 77 offers | Spain-specific market analysis |

---

## Repository Structure

```
Pearsons_Four/
├── .github/workflows/ci.yml       # CI pipeline
├── dashboard/app.py                # Streamlit interactive dashboard
├── notebooks/                      # Jupyter notebooks
│   ├── Pearsons_Four_EDA_Linkedin.ipynb
│   ├── Pearsons_Four_EDA_Enhanced.ipynb
│   ├── VGGPearsonsFour.ipynb          # Bias analysis (Vanessa)
│   ├── Auditoria_Pearson_4_CORREGIDO.ipynb  # Plotly refactor
│   └── espana/                         # Spain EDA notebooks
├── scripts/
│   ├── pipeline/                   # Modular data pipeline
│   │   ├── config.py               # Schema, roles, categories
│   │   ├── load_linkedin.py        # LinkedIn loader
│   │   ├── load_kaggle_ds.py       # Kaggle DS loader
│   │   ├── load_spain.py          # Spain data loader
│   │   ├── clean_normalize.py      # Cleaning & IQR
│   │   └── enrich_countries.py     # Country metadata
│   ├── generate_visualizations.py  # Static charts (matplotlib/seaborn)
│   ├── generate_plotly_viz.py      # Interactive HTML charts (Plotly)
│   ├── scrape_spain_salaries.py    # Scraper (5 sources)
│   ├── build_real_salary_pipeline.py
│   ├── verify_all_metrics.py       # Statistical verification
│   ├── export_tableau_v2.py        # Tableau-ready CSV export
│   └── export_tableau.py
├── tests/                          # Unit tests (9 tests)
├── dashboard/                      # Streamlit dashboard
├── data/
│   ├── linkedin_data_roles_procesed.csv   # Cleaned LinkedIn
│   ├── espana/                            # Spain data (17 files)
│   └── tableau/                           # Tableau-ready CSVs
├── screenshots/                    # Static PNGs + Plotly HTML
├── docs/                           # Reports, methodology, defense
├── slides/                         # Presentation decks
├── pyproject.toml                  # Dependencies (uv)
└── run_all.ps1                     # E2E pipeline orchestrator
```

---

## Tools & Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.11 |
| **Data** | pandas, numpy, scipy |
| **Visualization** | matplotlib, seaborn, plotly |
| **Scraping** | scrapling (Chrome TLS impersonation) |
| **Dashboard** | Streamlit |
| **Pipeline** | uv (package manager), custom modular pipeline |
| **BI** | Tableau Public |
| **CI/CD** | GitHub Actions (9 tests, notebook validation) |
| **Notebooks** | Jupyter / Google Colab |

---

## Quick Start

```bash
# Install
uv sync

# Run full pipeline
.\run_all.ps1

# Generate visualizations
uv run python scripts/generate_visualizations.py    # Static
uv run python scripts/generate_plotly_viz.py        # Interactive HTML

# Run tests
uv run pytest tests/ -v

# Launch dashboard
uv run streamlit run dashboard/app.py

# Export for Tableau
uv run python scripts/export_tableau_v2.py
```

---

## Credits

### Original Team Project (Phase 1 — May 2026)

| Role | Name | GitHub |
|------|------|--------|
| Data Wrangler & Product Owner | **Juan de la Fuente** | [@juandelaf1](https://github.com/juandelaf1) |
| Statistical Analysis | **Isabela Téllez** | [@Isabela-Tellez](https://github.com/Isabela-Tellez) |
| Data Visualization & Scrum Master | **Anas Fady** | [@Anasfady](https://github.com/Anasfady) |
| Ethics & Strategy | **Vanessa García** | [@garciaguadalupevanessa-bit](https://github.com/garciaguadalupevanessa-bit) |

### Personal Extension (Phase 2 — June 2026)

This repository is a **personal fork/extended version** by Juan de la Fuente, adding:
- Spain tech salary market study (5-source scraping + INE official data)
- Modular data pipeline (`scripts/pipeline/`)
- Interactive Plotly visualizations (HTML export)
- Streamlit dashboard
- Unit tests + CI/CD (GitHub Actions)
- Tableau Public integration
- Metric corrections (Data Roles vs All Professions)

---

## License

Educational project — Module II: Data Analysis & Visualization
*Pearsons Four — May/June 2026*
