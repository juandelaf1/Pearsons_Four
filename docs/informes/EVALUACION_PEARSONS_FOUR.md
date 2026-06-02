# Evaluación del Proyecto Pearson's Four
## Para: DataTalent Solutions S.L. — Mayo 2026

---

## 0. ¿Qué es Pearson's Four?

Es un proyecto de **consultoría en equipo** (4 personas, 4 roles) para **DataTalent Solutions S.L.**, una empresa española de talento/recruiting que quiere lanzar un **programa de reskilling** en el mercado tech español.

El proyecto cruza **dos fuentes de datos** para darle al cliente información accionable:

| Fuente | Tipo | Rol en el proyecto |
|--------|------|-------------------|
| **LinkedIn Job Postings** (Kaggle) | Ofertas de empleo reales | Dataset principal — Personas 1, 2, 3 |
| **Stack Overflow Survey 2025** | Encuesta a desarrolladores | Análisis de sesgos y habilidades — Persona 4 (Vanessa) |

**Las 4 personas del equipo:**

| Persona | Rol | Fases | Dataset |
|---------|-----|-------|---------|
| **Persona 1** | Data Wrangler | Fases 1-2: Carga, limpieza, filtrado | LinkedIn |
| **Persona 2** | Statistical Analyst | Fase 3: Estadísticas, correlaciones, ANOVA | LinkedIn (limpio) |
| **Persona 3** | Visualizer | Fase 4: Gráficos, dashboard | LinkedIn (procesado) |
| **Persona 4 (Vanessa)** | Ethics & Strategy Consultant | Stack Overflow: sesgos MNAR, selección; cruce con LinkedIn | Stack Overflow + LinkedIn |

---

## 1. El Problema de Negocio del Cliente

DataTalent Solutions S.L. quiere lanzar un programa de reskilling en España y necesita saber:

1. **¿Qué habilidades técnicas están más demandadas?** → Para diseñar el plan de estudios
2. **¿Cuánto paga el mercado?** → Para fijar expectativas salariales realistas
3. **¿Qué sectores contratan más?** → Para enfocar la inserción laboral
4. **¿Qué sesgos existen en los datos?** → Para no tomar malas decisiones basadas en datos flawedos

**Problema estructural:** El dataset principal (LinkedIn) tiene **0 ofertas de España**. Es 99% USA. Pero el cliente opera en España.

---

## 2. El Dilema Central del Proyecto

```
Cliente: DataTalent (España)
    └── Quiere: Análisis del mercado tech español
         └── Pero el dataset LinkedIn tiene 0 ofertas de España
              └── Entonces: ¿qué hacemos?
```

**La respuesta del proyecto:**
- No podemos analizar España directamente con LinkedIn
- Pero podemos extraer **patrones estructurales del mercado tech global** que SÍ aplican a España
- Y **documentar los sesgos** para que DataTalent no cometa errores

**Lo que LinkedIn SÍ puede decir (aunque sea USA):**
- Qué habilidades se piden en roles de datos (SQL, Python, etc.)
- Qué industrias contratan más (IT Services, Software, Financial Services)
- Cómo escala el salario con la experiencia
- Prima del trabajo remoto
- Correlación entre experiencia y salario (Pearson r)

**Lo que LinkedIn NO puede decir:**
- Salarios en España (0 postings)
- Cuántas ofertas hay en España
- Sectores específicos del mercado español

---

## 3. Lo Que Cada Persona Hizo (Resumen)

### Persona 1 — Data Wrangler (Fases 1-2)
**Input:** 123,849 postings de LinkedIn, 31 columnas
**Output:** 1,831 data roles limpios, documentación bilingüe

Decisiones clave:
- Filtró por títulos data (regex): data scientist, data engineer, data analyst...
- Usó `normalized_salary` (29% poblado) en vez de `med_salary` (5%)
- Mergeó con `job_skills` y `company_industries` para enriquecer
- Detectó: 0 postings de España ("Madrid, NY" es USA)
- **Decisión:** Mantuvo outliers, usó mediana como medida central

**Hallazgo clave:** El 66% de los salarios son nulos → el análisis salarial se basa en solo 621 registros.

### Persona 2 — Statistical Analyst (Fase 3)
**Input:** 1,831 data roles (limpios por Persona 1)
**Output:** Estadísticas, correlaciones, probabilidad condicional

**Hallazgos:**
| Test | Resultado |
|------|-----------|
| Salario medio (limpio) | $96,795 USD |
| Salario mediano (limpio) | $82,500 USD |
| Salario alto (Q3) | $170,000 USD |
| Remote premium | +$35,000 mediana (+45.1%) |
| P(High Salary | Python) | 8.00% vs 7.09% (+12.8%) |
| ANOVA (experiencia vs salario) | p < 0.0001 → rechaza H₀ |
| Pearson r (experiencia vs salario) | Positiva |

### Persona 3 — Visualizer (Fase 4)
**Input:** Datos procesados por Persona 1 y 2
**Output:** 6 gráficos:
1. Boxplot: salario por nivel de experiencia
2. Histograma + KDE: distribución salarial
3. Heatmap: correlaciones numéricas
4. Top 10 roles de datos (frecuencia)
5. Top 10 industrias contratantes
6. Scatter: views vs applies

### Persona 4 / Vanessa — Ethics & Strategy Consultant
**Input:** Stack Overflow Survey 2025 + LinkedIn procesado
**Output:** Análisis de sesgos + cruce de fuentes + recomendaciones

**Tres análisis:**

1. **Sesgo de Selección:** La muestra de SO sobre-representa perfiles jóvenes → cualquier modelo entrenado aquí discriminaría a seniors y minorías

2. **MNAR (Missing Not At Random):** Ciertos grupos demográficos ocultan sistemáticamente su salario → imputar con la media sesgaría los resultados

3. **Cruce Stack Overflow vs LinkedIn:**
   - SO (comunidad): mediana más alta, curva ancha → percepciones aspiracionales
   - LinkedIn (mercado): mediana más baja, curva estrecha → ofertas reales
   - **Decisión estratégica para DataTalent:** Usar LinkedIn para el "suelo" real del mercado, SO para entender hacia dónde especializarse

---

## 4. Lo Que Está FUERA del Alcance de Pearson's Four

Estos análisis son de proyectos SEPARADOS, NO de Pearson's Four:

| Fuente | Proyecto al que pertenece |
|--------|--------------------------|
| **INE Tabla 28185 / 28191** | Spain_EDA_Integrated (análisis propio) |
| **Manfred 2026 Salary Guide** | Spain_EDA_Integrated |
| **Ametic / Expansión 2025** | Spain_EDA_Integrated |
| **salarios_tech_limpio.csv** | Spain_EDA_Integrated |
| **Pearsons_Four_Enhanced.ipynb** | Spain_EDA_Integrated (notebook mío) |
| **build_real_salary_pipeline.py** | Spain_EDA_Integrated |
| **Multiplicadores regionales** | Spain_EDA_Integrated |

**¿Por qué no encajan en Pearson's Four?**
- Pearson's Four usa **LinkedIn + Stack Overflow** exclusivamente
- El INE/Manfred/Ametic son de un proyecto diferente que analiza España con fuentes oficiales
- Mezclarlos crea confusión porque son metodologías, datasets y preguntas de negocio distintas

---

## 5. Lo Que SIRVE para Pearson's Four

### Análisis que tienen sentido dentro del proyecto:

**a) LinkedIn dataset (Personas 1, 2, 3):**
- 1,831 data roles, 621 con salario
- Correlaciones y ANOVA
- Remote premium (+45.1%)
- Top skills, top industries
- Gráficos de distribución

**b) Stack Overflow (Persona 4 / Vanessa):**
- Top 10 habilidades técnicas más demandadas
- Sesgo de selección (demographics)
- MNAR (datos faltantes no aleatorios)
- Probabilidad condicional por grupo demográfico

**c) Cruce LinkedIn ↔ Stack Overflow (Persona 4 / Vanessa):**
- Comparativa de medianas: SO ($) vs LinkedIn ($)
- Curvas KDE comparadas: SO más ancha, LinkedIn más estrecha
- **Conclusión para DataTalent:** LinkedIn da el suelo real, SO da la dirección aspiracional

**d) Lo que NO se puede hacer (y se documenta como limitación):**
- Análisis salarial de España con LinkedIn (0 postings)
- Skill analysis detallado con LinkedIn (categorías muy generales)

---

## 6. ¿Qué Falta o Está Incompleto?

| Elemento | Estado |
|----------|--------|
| **README del proyecto** | Se menciona en VGG pero no se ve en los archivos |
| **Informe ejecutivo para DataTalent** | Solo en markdown dentro de los notebooks (cells 45, 65-69, 17, 20) |
| **Gráficos guardados como PNG** | Solo existen si se ejecutaron los notebooks (no en disco) |
| **Dataset limpio exportado** | linkedin_data_roles_raw_nulls.csv (Persona 1) |
| **Cruce formal de fuentes** | Fase 5 en VGG — tabla comparativa y KDE overlay |
| **Recomendaciones de negocio** | Cells 17 y 20 de VGG — bien redactadas para DataTalent |

---

## 7. Conclusión

**Pearson's Four** es un proyecto de consultoría que **hace lo correcto con lo que tiene**: sabiendo que LinkedIn no tiene datos de España, extrae patrones globales útiles y documenta los sesgos para que DataTalent no tome malas decisiones.

El valor real del proyecto está en:
1. Demostrar **qué se puede** y **qué no se puede** hacer con cada dataset
2. El **análisis de sesgos** (MNAR, selección) que evita errores costosos
3. El **cruce de fuentes** que calibra expectativas (SO aspiracional vs LinkedIn real)

El INE, Manfred, Ametic, y el dataset multi-país **no pertenecen a este proyecto**. Son análisis complementarios pero separados.
