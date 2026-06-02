# GUÍA DE MÉTRICAS Y CAMBIOS
## Para el equipo: qué significa cada métrica, qué cambió y por qué

---

## 📌 RESUMEN DEL PROBLEMA DETECTADO

La notebook original (`Pearsons_Four_EDA_Linkedin.ipynb`) tiene un error estructural: la **Persona 2 (Isabela)** usó el dataset `df` (123,849 filas con TODAS las profesiones) para sus cálculos estadísticos, en lugar de usar `df_data` (1,831 filas solo de roles Data).

**Consecuencia:** varias métricas del proyecto estaban calculadas sobre TODAS las ofertas de LinkedIn (camareros, ingenieros, médicos, etc.), no solo sobre roles de datos.

**Solución:** Creamos `Pearsons_Four_EDA_Enhanced.ipynb` que corrige este error y añade mejoras.

---

## 📊 EXPLICACIÓN DE CADA MÉTRICA

### 1. MEDIANA SALARIAL
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | El valor central cuando ordenamos todos los salarios de menor a mayor. El 50% está por encima, el 50% por debajo. |
| **Cómo se calcula** | `df['normalized_salary'].median()` |
| **Por qué la usamos** | La distribución salarial tiene asimetría positiva (cola larga a la derecha). La mediana NO se ve afectada por valores extremos, a diferencia de la media. |
| **Valor CORREGIDO** | **$136,422 USD** (Data Roles USA) |
| **Valor antiguo** | $135,588 (diferencia mínima, ambos son correctos con ligeras variaciones de filtrado) |

### 2. MEDIA SALARIAL
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | La suma de todos los salarios dividida entre el número de registros. |
| **Cómo se calcula** | `df['normalized_salary'].mean()` |
| **Por qué NO es la principal** | La media es sensible a outliers. Como hay salarios muy altos (Director, Executive), la media ($142,936) es mayor que la mediana ($136,422). |
| **Valor CORREGIDO** | **$142,936 USD** |

### 3. REMOTE PREMIUM
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | La diferencia porcentual entre el salario mediano de ofertas remotas y presenciales. |
| **Cómo se calcula** | `(median(remote) / median(onsite) - 1) * 100` |
| **ERROR DETECTADO** | El +45.1% del README original se calculó sobre TODAS las ofertas de LinkedIn (35641 registros), donde oficios presenciales de baja cualificación reducían la mediana presencial a $78,000. |
| **Valor CORREGIDO (Data Roles)** | **-1.2%** ($135,200 remoto vs $136,900 presencial). Test estadístico: no significativo (p=0.46). |
| **¿Qué significa?** | Para roles de datos específicamente, trabajar remoto NO implica un salario diferente al presencial. El mercado valora igual ambas modalidades. |
| **Valor para TODAS las ofertas** | +45.3% (sigue siendo correcto, pero NO aplica a nuestro análisis de Data Roles) |

### 4. CORRELACIÓN DE PEARSON (r)
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | Mide la relación LINEAL entre dos variables. Va de -1 a +1. +1 = correlación perfecta positiva, 0 = sin relación, -1 = correlación perfecta negativa. |
| **Cómo se calcula** | `scipy.stats.pearsonr(x, y)` |
| **Cuándo usarla** | Cuando la relación entre variables es aproximadamente lineal y ambas tienen distribución normal o aproximadamente normal. |

**Correlaciones CORREGIDAS (Data Roles):**
| Variables | Pearson r | Interpretación |
|-----------|-----------|----------------|
| Experiencia → Salario | **0.49** | Moderada-fuerte. A más experiencia, más salario. Es el hallazgo #1. |
| Views → Applies | **0.91** | Muy fuerte. A más visualizaciones, más aplicaciones. |
| Views → Salario | **-0.15** | Muy débil negativa. Casi no hay relación. Las ofertas más vistas NO pagan más. |
| Remote → Salario | **0.04** | Cero. No hay relación. Ser remoto no implica mayor o menor salario en Data. |

**Valores antiguos (erróneos):** Experiencia=0.43 (diferencia menor), Views-Apps=0.62 (MUY diferente, porque incluía todas las profesiones), Views-Salario=0.04.

### 5. CORRELACIÓN DE SPEARMAN (ρ)
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | Como Pearson, pero basado en RANGOS (posiciones) en vez de valores brutos. No asume linealidad ni normalidad. |
| **Por qué lo añadimos** | Porque el salario tiene asimetría positiva, Spearman es más robusto. Si ρ > r, la relación es monótona pero no perfectamente lineal. |
| **Valor** | Experiencia-Salario: ρ = **0.50** (similar a Pearson 0.49, lo que indica que la relación es bastante lineal) |

### 6. ANOVA (Analysis of Variance)
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | Test estadístico que compara si las medias de varios grupos son diferentes. |
| **Hipótesis nula (H₀)** | "La experiencia NO afecta al salario" (todos los grupos tienen la misma media) |
| **Resultado** | F = 43.79, **p < 0.00001** |
| **Conclusión** | Rechazamos H₀. Con un 99.999% de confianza, la experiencia SÍ afecta al salario. |
| **Analogía** | Es como decir: "La probabilidad de que estas diferencias salariales entre niveles sean por casualidad es MENOR que 0.001%". |

### 7. PROBABILIDAD CONDICIONAL
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | P(A | B) = probabilidad de que ocurra A dado que ocurrió B. |
| **Ejemplo** | P(Salario Alto | Python) = probabilidad de tener salario alto (>$170K) si la oferta menciona Python. |
| **Problema** | No pudimos calcularla porque el 98% de las ofertas tienen `skills_desc` nulo. La métrica original (+12.8%) NO es fiable. |

### 8. MNAR (Missing Not At Random)
| Concepto | Explicación |
|----------|-------------|
| **Qué es** | Los datos faltantes NO son aleatorios, siguen un patrón. |
| **Evidencia** | 47.33% de juniors ocultan salario vs 23.86% de seniors. |
| **Impacto** | Si imputamos la media general, subestimamos salarios junior. Si entrenamos un modelo, aprenderá biased. |

---

## 📋 QUÉ ARCHIVOS CAMBIAN Y CUÁLES SUBIR

### Archivos que ya están CORREGIDOS en el repo:

| Archivo | Cambio | Estado |
|---------|--------|--------|
| `README.md` | URLs de GitHub corregidas | ✅ Listo |
| `docs/GUIDE.md` | URLs de GitHub corregidas | ✅ Listo |
| `screenshots/linkedin_boxplot_experience.png` | Regenerado con datos correctos | ✅ Listo |
| `screenshots/linkedin_histogram_kde.png` | Regenerado con datos correctos | ✅ Listo |
| `screenshots/linkedin_salary_spread.png` | Regenerado | ✅ Listo |
| `screenshots/linkedin_top_roles.png` | Regenerado | ✅ Listo |
| `screenshots/linkedin_views_vs_applies.png` | Regenerado con r=0.91 y línea de regresión | ✅ Listo |
| `screenshots/linkedin_remote_premium.png` | **NUEVO**: remote premium comparativo | ✅ Listo |
| `screenshots/linkedin_salary_progression.png` | **NUEVO**: línea de progresión salarial | ✅ Listo |
| `screenshots/linkedin_salary_cdf.png` | **NUEVO**: distribución acumulada (CDF) | ✅ Listo |

### Archivos nuevos para SUBIR:

| Archivo | Por qué |
|---------|---------|
| `notebooks/Pearsons_Four_EDA_Enhanced.ipynb` | Versión corregida + mejorada (107 celdas, Spearman, bootstrap, pairplot, violin, QQ-plot, line graphs, CDF, conclusiones bilingües, footnotes) |
| `scripts/generate_visualizations.py` | Para regenerar gráficos reproduciblemente |
| `scripts/verify_all_metrics.py` | Script de verificación de todas las métricas |
| `slides/Data_Market_Intelligence.pptx` | Presentación nueva de Isabela |
| `slides/Pearsons_Four_..._Data_Science.pptx` | Presentación alternativa |
| `docs/GUION_DEFENSA_COMPLETO.md` | Guion de defensa con métricas corregidas |
| `docs/GUIA_METRICAS_Y_CAMBIOS.md` | Este documento — explicación para el equipo |

### Archivos QUE NO SE SUBEN:

| Archivo | Motivo |
|---------|--------|
| `.venv/` | Entorno virtual, no va en el repo (añadir a .gitignore) |
| `Pearsons_Four_Integrated_ES/` | Carpeta fuera del repo |
| `scripts/verify_salaries.py` | Reemplazado por verify_all_metrics.py (más completo) |

### Archivos que REQUIEREN ATENCIÓN:

| Archivo | Problema | Solución |
|---------|----------|----------|
| `slides/presentacion_pearsons_four.pptx` | Contiene métricas antiguas (remote premium +45.1%, views-Apps 0.62) | Actualizar las diapositivas con los valores corregidos. Las diapositivas de Isabela (Data_Market_Intelligence.pptx) probablemente ya tienen los correctos. |
| `README.md` (sección Key Findings) | Tiene métricas mixtas (algunas correctas, otras no) | Hay que actualizar los números. Lo hago a continuación. |

---

## 🛠️ ACTUALIZACIÓN DEL README

Sección "Key Findings" del README debe actualizarse con valores CORREGIDOS para Data Roles:

### Statistical Analysis (CORREGIDO)
```diff
- | Remote premium | +45.1% (Remote: $112,500 vs On-site: $77,500 median) |
+ | Remote premium (Data Roles) | -1.2% (Remote: $135,200 vs On-site: $136,900) — No significativo |
+ | Remote premium (All LinkedIn) | +45.3% — Contexto general del mercado |

- | Views → Applies | 0.62 (moderate positive) |
+ | Views → Applies | 0.91 (strong positive) |

- | Experience level → Salary | 0.43 (moderate positive) |
+ | Experience level → Salary | 0.49 (moderate positive) |

+ | Spearman ρ (experience → salary) | 0.50 (validación robusta) |

+ | Views → Salary | -0.15 (near-zero, negative trend) |
```

---

## 👥 CÓMO PRESENTARLO AL EQUIPO

### Reunión de 5 minutos para alinear al equipo:

**Tú (Juan):** "Chicos, he estado revisando los números en profundidad y he detectado algo importante. Cuando Isabela hizo el análisis estadístico, usó el dataset COMPLETO de LinkedIn (123K ofertas) en vez del filtrado de roles Data (1.8K). Esto hizo que métricas como el remote premium (+45%) y views-applies (0.62) reflejaran TODAS las profesiones, no solo Data Roles.

**El impacto real es este:**
- El remote premium del +45% es real... para el mercado laboral EN GENERAL. Para roles Data, no hay diferencia significativa entre remoto y presencial.
- La correlación views-applies es 0.91 (no 0.62) — más fuerte de lo que pensábamos.
- La correlación experiencia-salario es 0.49 (no 0.43) — también más fuerte.
- La probabilidad condicional de Python no es fiable porque el 98% de skills_desc está vacío.

**Lo bueno:** los hallazgos principales se mantienen o mejoran. La experiencia sigue siendo el factor #1. El MNAR sigue siendo el hallazgo diferencial.

**Propongo:**
1. Usar la nueva notebook `Pearsons_Four_EDA_Enhanced.ipynb` para la defensa — tiene los números correctos
2. Actualizar las slides con las métricas corregidas
3. Las diapositivas que ya hizo Isabela probablemente están bien, pero revisemos juntos los números
4. Si alguien pregunta por qué cambian las cifras, decimos: 'Hemos validado todos los cálculos exclusivamente sobre la muestra de roles Data (616 registros), eliminando el ruido de otras profesiones'"

### Puntos clave para que cada miembro sepa:

| Persona | Le afecta | Qué decir si preguntan |
|---------|-----------|----------------------|
| **Isabela** | Sí — sus métricas cambian | "Los cálculos iniciales incluían todas las profesiones. Los corregidos son solo Data Roles." |
| **Anas** | Sí — el scatter cambia de r=0.62 a r=0.91 | "Actualicé el scatter con línea de regresión y el valor corregido." |
| **Vanessa** | No — sesgos no cambian | Sin cambios en su parte. El MNAR sigue igual. |
| **Juan** | Sí — debe explicar la corrección al cliente | "Validación final de métricas exclusivas para Data Roles." |
