# 🗺️ ROADMAP — Pearsons Four

> **Project:** EDA Data Science Job Salaries — LinkedIn + Stack Overflow + Spain Market Study
> **Owner:** Juan de la Fuente ([@juandelaf1](https://github.com/juandelaf1))
> **Status:** Active development — Phase 2.4 (Data Sources) in progress

---

## Legend

| Icon | Meaning |
|------|---------|
| ✅ | Completed |
| 🔄 | In progress |
| 📅 | Planned |
| 💡 | Future idea |

---

## Phase 1 — Team Project ✅

*Original team deliverable — May 2026*

- [x] **P1.1** LinkedIn Job Postings EDA (full notebook)
- [x] **P1.2** Stack Overflow Bias Analysis (Vanessa)
- [x] **P1.3** Cross-dataset comparison (LinkedIn vs SO)
- [x] **P1.4** Executive presentation (10 min slides)
- [x] **P1.5** README + GUIDE.md with results

---

## Phase 2 — Personal Extension 🔄

*Post-delivery improvements — June 2026*

### 2.1 — Foundation ✅

- [x] **2.1.1** Spain tech salary market study (5 sources)
- [x] **2.1.2** Modular data pipeline (`scripts/pipeline/`)
- [x] **2.1.3** Metric corrections (Data Roles vs All Professions)
- [x] **2.1.4** `pyproject.toml` + `uv` dependency management

### 2.2 — Professionalization ✅

- [x] **2.2.1** Interactive Plotly visualizations (5 HTML charts)
- [x] **2.2.2** Streamlit dashboard (`dashboard/app.py`)
- [x] **2.2.3** Unit tests (9 tests: config, cleaning, enrichment)
- [x] **2.2.4** GitHub Actions CI workflow
- [x] **2.2.5** Tableau Public data export (`data/tableau/`)

### 2.3 — Data Quality ✅

- [x] **2.3.1** Title normalization (1,037 → 15 roles, 99.8% capture)
- [x] **2.3.2** Seniority level extraction + standardization
- [ ] **2.3.3** Salary outlier policy (documented + filter options)
- [x] **2.3.4** Cross-source schema alignment (LinkedIn + Kaggle DS + Spain)

### 2.4 — New Data Sources 🔄

- [x] **2.4.1** **Eurostat** — Population (`demo_pjan`) + GDP (`nama_10_gdp`) for PPP-adjusted salary comparisons across EU
- [ ] **2.4.2** **Levels.fyi** — Verified tech salaries by company (Google, Meta, etc.) for Spain offices
- [ ] **2.4.3** **Glassdoor UK/DE/FR** — Extended European scraper for cross-country comparison
- [ ] **2.4.4** **InfoJobs API** — Live Spanish job market data (60%+ market share in ES)
- [x] **2.4.5** **Kaggle DS Salaries** — Multi-year global dataset (607 records, 2020–2024)
- [x] **2.4.6** **DuckDB analytics engine** — 5 SQL queries for median, country ranking, seniority premium, top roles, market sizing

### 2.5 — Advanced Analysis 📅

- [ ] **2.5.1** PPP-adjusted salary comparison (Spain vs EU vs US) — *Eurostat data loaded, needs dashboard integration*
- [ ] **2.5.2** Experience × Role interaction model (ANOVA + effect size)
- [ ] **2.5.3** Salary prediction baseline (linear regression, feature importance)
- [ ] **2.5.4** Time-series analysis if multi-year data available

### 2.6 — Documentation & Portfolio 🔄

- [x] **2.6.1** README restructured as executive summary + KPIs
- [x] **2.6.2** Bilingual conclusions template (ES/EN)
- [x] **2.6.3** CHANGELOG.md
- [x] **2.6.4** GitHub Issues + PR templates for task tracking
- [ ] **2.6.5** LinkedIn article / Medium post about the project
- [ ] **2.6.6** Slide deck v2 (incorporating Spain study + corrected metrics)

---

## Phase 3 — Future Vision 💡

*Ideas for after core completion*

- [ ] **3.1** Real-time dashboard (Streamlit Cloud or Render)
- [ ] **3.2** Monthly data refresh pipeline (GitHub Actions cron)
- [ ] **3.3** Interactive salary simulator web app
- [ ] **3.4** Integration with LinkedIn Jobs API for live Spanish postings
- [ ] **3.5** ML model: predict salary band from title, experience, location, skills
- [ ] **3.6** Tableau Public dashboard published and embedded in README

---

## Progress Summary

```
Phase 1 (Team)    ████████████████████ 100%
Phase 2.1 (Found) ████████████████████ 100%
Phase 2.2 (Prof)  ████████████████████ 100%
Phase 2.3 (Qual)  ████████████████████ 100%  ← completed
Phase 2.4 (Data)  ████████████░░░░░░░░  60%
Phase 2.5 (Anal)  ░░░░░░░░░░░░░░░░░░░░  10%
Phase 2.6 (Docs)  █████████████░░░░░░░  67%
---
**Overall:** ████████████░░░░░░░░░░  48%
```
