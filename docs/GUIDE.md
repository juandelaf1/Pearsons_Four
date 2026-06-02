# Pearsons Four — Team Guide / Guía del Equipo

**Bilingual — English / Español**

---

## 1. Team & Roles / Equipo y Roles

| Person | Role | GitHub |
|--------|------|--------|
| **Juan** | Responsable de Ingeniería de Datos (Data Wrangler) | [@juandelaf1](https://github.com/juandelaf1) |
| **Isabela** | Responsable de Análisis Estadístico | [@Isabela-Tellez](https://github.com/Isabela-Tellez) |
| **Anas** | Responsable de Visualización (Data Storyteller) | [@Anasfady](https://github.com/Anasfady) |
| **Vanessa** | Consultora de Estrategia y Ética de Datos | [@garciaguadalupevanessa-bit](https://github.com/garciaguadalupevanessa-bit) |

**Scrum Master:** Anas — Facilitates the process, removes blockers, manages the repo.
**Product Owner:** Juan — Prioritizes backlog, validates business questions, prepares executive presentation.

---

## 2. Workflow / Flujo de Trabajo

### GitHub Flow
```
main (protected — no direct pushes)
  ├── feature/data-wrangling        → PR → review → merge
  ├── feature/analisis-estadistico  → PR → review → merge
  ├── feature/visualizaciones       → PR → review → merge
  ├── feature/sesgos-etica          → PR → review → merge
  └── feature/slides-readme         → PR → review → merge
```

**Rules / Reglas:**
- Never push directly to `main`
- Every change = a branch → Pull Request → someone reviews → merge
- Branch naming: `feature/lo-que-sea` or `fix/lo-que-sea`
- Commits in English: `feat: load dataset and inspect`, `fix: handle null salaries`

### Daily Standup (5 min)
- What did I do yesterday?
- What will I do today?
- Any blockers?
- Led by Anas (SM)

---

## 3. Task Distribution / Distribución de Tareas

### Role 1 — Responsable de Ingeniería de Datos (Data Wrangler)
**Owner: Juan** | Foco: Calidad y estructura del dato (Fases 1 y 2)

| Cell | Task | Code / Action |
|------|------|---------------|
| 1.1 | Carga e Inspección | `df.shape()`, `df.info()`, `df.describe()` |
| 1.2 | Limpieza | Tratamiento de nulos (imputación o eliminación) |
| 1.3 | Normalización de textos | `df['col'].str.lower().str.strip()` |
| 1.4 | Gestión de Outliers | IQR (`Q1-1.5*IQR`, `Q3+1.5*IQR`) y z-score (`np.abs(stats.zscore()) < 3`) |
| 1.5 | Documentación | Justificar cada decisión de limpieza en celdas Markdown |

### Role 2 — Responsable de Análisis Estadístico
**Owner: Isabela** | Foco: Evidencia empírica y correlaciones (Fase 3)

| Cell | Task | Code / Action |
|------|------|---------------|
| 2.1 | Descriptivos | `mean()`, `median()`, `std()` de salario y variables clave |
| 2.2 | Agrupamientos | `df.groupby()`, `pivot_table()` — salario por ciudad, sector, género |
| 2.3 | Matriz de Correlación | `df.corr()` + heatmap — experiencia, skills, salario |
| 2.4 | Probabilidad Condicional | P(salario_alto ∣ Python) y otras probabilidades condicionales |
| 2.5 | ANOVA / Tests | `stats.f_oneway()` — validar diferencias significativas |

### Role 3 — Responsable de Visualización (Data Storyteller)
**Owner: Anas** | Foco: Comunicación visual y claridad (Fase 4)

| Cell | Task | Code / Action |
|------|------|---------------|
| 3.1 | Histograma + KDE | `sns.histplot(kde=True)` — distribución salarial |
| 3.2 | Boxplot por experiencia | `sns.boxplot(x='experience', y='salary')` |
| 3.3 | Barras: top roles | `df['title'].value_counts().head(10).plot(kind='bar')` |
| 3.4 | Barras: top industrias | `df['industry'].value_counts().head(10).plot(kind='bar')` |
| 3.5 | Dispersión: views vs applies | `sns.scatterplot(x='views', y='applies')` |
| 3.6 | Heatmap de correlación | `sns.heatmap(corr, annot=True, cmap='coolwarm')` |
| 3.7 | Distribución Normal / KDE | Visualización con curva de densidad sobre datos reales |
| 3.8 | Estética profesional | Títulos, etiquetas de ejes, leyendas claras en TODOS los gráficos |
| 3.9 | Interpretación | Redactar interpretación escrita de cada hallazgo visual |

**Mínimo obligatorio:** 6 visualizaciones con interpretación cada una.

### Role 4 — Consultor de Estrategia y Ética de Datos
**Owner: Vanessa** | Foco: Sesgos, recomendaciones y presentación final

| Cell | Task | Code / Action |
|------|------|---------------|
| 4.1 | Identificación de Sesgos | Detectar subrepresentación, sesgos geográficos, MNAR |
| 4.2 | Impacto Predictivo | Analizar cómo los sesgos afectarían a modelos de IA |
| 4.3 | Ranking de Skills | Determinar habilidades más demandadas (Python, SQL, AWS, etc.) |
| 4.4 | Probabilidad Condicional sesgos | P(skill ∣ high_salary), P(gender ∣ role) |
| 4.5 | Presentación Ejecutiva | Liderar creación de slides + recomendaciones finales |

---

## 4. Project Structure / Estructura del Proyecto

```
Pearsons_Four/
├── screenshots/                 # Banner + capturas de gráficos
│   └── banner.png
├── docs/
│   ├── GUIDE.md                 # This file / Este archivo
│   └── trello_template.json
├── notebooks/
│   ├── Pearsons_Four_EDA_Linkedin.ipynb              # LinkedIn EDA (full)
│   └── VGGPearsonsFour.ipynb                         # Bias + Cross-dataset (Vanessa)
├── data/
│   └── linkedin_data_roles_procesed.csv              # Cleaned LinkedIn data roles
├── .github/
│   └── ISSUE_TEMPLATE/
│       └── task.md
└── README.md
```

---

## 5. Cell Formatting Convention

```python
# === SECTION 1.1 ===
# by: Juan
# date: 2026-05-27
import pandas as pd
df = pd.read_csv('/content/postings.csv')
```

- Every code cell needs a Markdown cell before it explaining the approach
- Every Markdown cell after code must interpret the results
- Graphs must have: title, axis labels, legend (if applicable)

---

## 6. Definition of Done (DoD)

A task is complete when:

- [ ] Code runs without errors
- [ ] All code cells have a corresponding **Markdown interpretation**
- [ ] Graphs have: title, axis labels, legend (if applicable)
- [ ] Peer has reviewed and approved
- [ ] PR merged to main

---

## 7. Final Checklist / Lista de Verificación

| Item | Verifies |
|------|----------|
| Mínimo 6 gráficos con título + etiquetas + interpretación | **Anas** |
| Al menos 1 distribución (histograma + KDE) | **Anas** |
| 2+ sesgos identificados con origen e impacto | **Vanessa** |
| `groupby()` usado e interpretado | **Isabela** |
| Matriz de correlación + heatmap | **Isabela** |
| Mean/median/std de 3+ variables clave | **Isabela** |
| Cada decisión de limpieza justificada | **Juan** |
| Nulos cuantificados y tratados | **Juan** |
| Outliers por IQR y z-score | **Juan** |
| Probabilidad condicional calculada | **Isabella / Vanessa** |
| Presentación ejecutiva (10 min slides) | **Vanessa (lidera) + Juan** |
| Notebook subido a GitHub + README actualizado | **Anas** |
| Banner en README | **Anas** |

---

## 8. Presentation Plan (10 min, 4 personas)

| Time | Speaker | Topic |
|------|---------|-------|
| 0:00–0:30 | Juan | Intro: DataTalent case, business questions, datasets used |
| 0:30–2:30 | Juan | Role 1: Data Wrangling — carga, limpieza, outliers, decisiones |
| 2:30–4:30 | Isabella | Role 2: Análisis Estadístico — correlaciones, probabilidades, ANOVA |
| 4:30–6:30 | Anas | Role 3: Visualizaciones — mostrar 4–6 gráficos clave, interpretación |
| 6:30–8:30 | Vanessa | Role 4: Sesgos, ética, impacto en IA, ranking de skills |
| 8:30–9:30 | Vanessa | Recomendaciones para DataTalent |
| 9:30–10:00 | Juan | Cierre, Q&A |

---

## 9. Glossary / Glosario

| English | Spanish | Definition |
|---------|---------|------------|
| **EDA** | Análisis Exploratorio de Datos | Process of examining datasets to summarize main characteristics |
| **NaN** | Valor nulo | Missing value in a dataset |
| **Outlier** | Valor atípico | Data point far from others |
| **Standard Deviation** | Desviación estándar | How spread out values are from the mean |
| **Correlation** | Correlación | How two variables change together (-1 to +1) |
| **Bias** | Sesgo | Systematic error causing over/underrepresentation |
| **MNAR** | Missing Not At Random | Missing data depends on unobserved value |
| **IQR** | Rango Intercuartílico | Q3 - Q1, used to detect outliers |
| **Conditional Probability** | Probabilidad condicional | P(A∣B): probability of A given B occurred |
| **ANOVA** | ANOVA | Analysis of variance — tests if group means differ |
| **Skewness** | Asimetría | Measure of distribution asymmetry |
| **Kurtosis** | Curtosis | Measure of tail heaviness |

---

*Pearsons Four — Module II: Data Analysis & Visualization*
*May 2026*
