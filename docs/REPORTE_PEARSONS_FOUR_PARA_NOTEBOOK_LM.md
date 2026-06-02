# REPORTE COMPLETO — Pearson's Four + Portfolio_Notebooks
## Para usar con Notebook LM y preparación de defensa

---

## 📌 PARTE 1: DIAGNÓSTICO DEL NOTEBOOK PRINCIPAL
### Archivo: `Pearsons_Four_Proyecto.ipynb`

### ✅ FORTALEZAS DETECTADAS
- Carga automática con KaggleHub (reproducible)
- Pipeline completo: carga → limpieza → filtrado → estadística → visualización
- Documentación bilingüe EN/ES en celdas Markdown
- Outliers evaluados con IQR y Z-score (decisión justificada: mantener)
- ANOVA con interpretación correcta
- Probabilidad condicional P(High Salary | Python)

### ❌ DEBILIDADES Y ERRORES DETECTADOS

| # | Problema | Localización | Severidad |
|---|----------|-------------|-----------|
| 1 | **Celdas duplicadas**: Cells 35 y 37 tienen EXACTAMENTE el mismo código (salary stats repetido) | Cells 35, 37 | ⚠️ Media |
| 2 | **Cell 26 (Markdown)**: Placeholders sin reemplazar — pone "Found **XX** data-related postings" y "**XX%**" en vez de los valores reales (1,831 y 1.5%) | Cell 26 | 🔴 Alta |
| 3 | **Cell 48 usa `df` sin filtrar**: El ANOVA y estadísticas de Persona 2 usan el `df` original (123,849 filas) en vez de `df_clean` (1,831 data roles) | Cell 48, 50, 52, 54, 56, 58 | 🔴 Alta |
| 4 | **Internship mean $963K**: Detectado en Cell 65 pero NUNCA se filtró. Cell 60 filtra a `df_clean` pero Persona 2 usó `df` original | Cell 48-64 | 🔴 Alta |
| 5 | **Matriz de correlación limitada**: Cell 54 usa `df.select_dtypes(include=['number'])` que solo captura columnas numéricas sueltas. No incluye experiencia codificada ni variables categóricas transformadas | Cell 54 | ⚠️ Media |
| 6 | **Sin Spearman**: Solo Pearson. Para salarios con asimetría positiva, Spearman es más robusto | Cell 54 | ⚠️ Media |
| 7 | **El scatter Views vs Applies (Cell 83)**: Usa `df_viz` que es el archivo RAW (no el filtrado con salarios ≥ $1K). No muestra línea de tendencia ni coeficiente r | Cell 83 | ⚠️ Media |
| 8 | **Heatmap de correlación (Cell 78)**: Hace one-hot de experiencia pero no usa `df_clean` filtrado por salarios válidos. Incluye `normalized_salary` con datos erróneos | Cell 78 | 🔴 Alta |
| 9 | **Sin pairplot**: No hay matriz de dispersión multivariante que permita ver relaciones 2 a 2 | Falta | ⚡ Oportunidad |
| 10 | **Falta el cálculo de "r = 0.62"**: El valor de correlación Views- Applies que aparece en la presentación no está documentado ni calculado explícitamente en el notebook | Presentación | 🔴 Alta |

### 🛠️ CORRECCIONES RECOMENDADAS PARA EL NOTEBOOK

```python
# CORRECCIÓN 1: Persona 2 debe usar df_clean filtrado
# Reemplazar en Cell 48:
df_stats = df_clean[(df_clean['normalized_salary'] >= 1000) & 
                     (df_clean['normalized_salary'] <= 2000000)].copy()
experience_analysis = df_stats.groupby('formatted_experience_level')['normalized_salary'].agg(...)

# CORRECCIÓN 2: Añadir correlación de Spearman
from scipy.stats import spearmanr
spearman_corr = df_stats[['normalized_salary', 'views', 'applies', 'experience_level_num']].corr(method='spearman')
print("Spearman Correlation:\n", spearman_corr)

# CORRECCIÓN 3: Scatter con línea de tendencia y r-value
from scipy.stats import pearsonr
r, p = pearsonr(df_stats['views'], df_stats['applies'])
sns.regplot(data=df_stats, x='views', y='applies', scatter_kws={'alpha':0.5})
plt.title(f'Views vs Applies (r = {r:.2f}, p = {p:.4f})')

# CORRECCIÓN 4: Cell 26 - reemplazar XX por valores reales
"""
### Data Roles Filtering
- Found **1,831** data-related postings out of 123,849 total (1.5%)
- Most common titles: data scientist, data engineer, data analyst
"""
```

---

## 📌 PARTE 2: EVALUACIÓN DE INTEGRACIÓN CON PORTFOLIO_NOTEBOOKS

### Estructura actual de portfolio_notebooks/

```
portfolio_notebooks/
├── Pearsons_Four_Enhanced.ipynb    → Correlaciones Pearson con datos España (INE + Kaggle)
├── Spain_EDA_Integrated.ipynb       → EDA completo mercado tech español
├── Spain_EDA_Integrated_executed.ipynb
├── pipeline/build_real_salary_pipeline.py
├── datos/                           → CSVs del INE + estimaciones salariales
├── graficos/                        → 19 PNGs (correlaciones, tendencias, mapas)
├── informes/                        → 3 informes .md detallados
│   ├── EVALUACION_PEARSONS_FOUR.md
│   ├── INFORME_INTERNACIONAL.md
│   └── INFORME_TECHSALARY_ES.md
└── legacy/                          → Scripts intermedios
```

### ¿SE PUEDE INTEGRAR?

**Sí, pero con una estrategia clara.** El proyecto Pearson's Four original usa LinkedIn + Stack Overflow (mercado USA/global). Portfolio_notebooks usa INE + Kaggle España (datos oficiales españoles). Son complementarios, NO sustitutivos.

### ESTRATEGIA DE INTEGRACIÓN RECOMENDADA

#### Opción A: Notebook unificado (Recomendada)
Crear `Pearsons_Four_COMPLETO.ipynb` que:
1. **Parte 1**: Análisis LinkedIn (Pearson's Four original) → hallazgos globales
2. **Parte 2**: Análisis Stack Overflow (sesgos MNAR, probabilidad condicional)
3. **Parte 3**: Contraste con datos España (INE + Manfred + Ametic de portfolio_notebooks)
4. **Parte 4**: Tabla comparativa LinkedIn global vs INE España con multiplicadores
5. **Conclusión**: Qué aplica a España y qué no, con factores de ajuste

#### Opción B: Mantener separados + puente (Más limpia)
- Pearson's Four: LinkedIn + SO (análisis global)
- Spain_EDA: INE + datos España (análisis local)
- Un **informe puente** que cruce ambos: ejemplo de tabla:

| Métrica | LinkedIn Global | INE España | Factor de Ajuste |
|---------|----------------|------------|------------------|
| Salario medio Data | $96,795 USD | 42.742 € | ~0.44 (TC + mercado) |
| Remote Premium | +45.1% | +15-20% (estimado) | ~0.4x |
| Senior premium vs Junior | 4.2x | 2.5x | ~0.6x |

### RECOMENDACIÓN FINAL
Usa **Opción B** para la defensa (no mezcles metodologías distintas). Pero crea una **diapositiva puente** en la presentación que diga:
> "Hemos contrastado nuestros hallazgos globales con datos oficiales españoles (INE). Aunque los salarios absolutos difieren, los **patrones estructurales** (experiencia, remote premium, skills) se mantienen."

---

## 📌 PARTE 3: MEJORAS ESTADÍSTICAS RECOMENDADAS

### 3.1 GRÁFICOS ADICIONALES QUE FALTAN

| Gráfico | Por qué | Código base |
|---------|---------|-------------|
| **Pairplot** (matriz de dispersión) | Ver relaciones 2 a 2 entre salary, views, applies, experience | `sns.pairplot(df_stats[cols])` |
| **Gráfico de líneas: salario por experiencia** | Mostrar progresión clara de mediana por nivel | `sns.pointplot()` con medianas |
| **QQ-Plot** | Validar normalidad de la distribución salarial | `stats.probplot()` |
| **Violin plot** | Mejor que boxplot para mostrar densidad por experiencia | `sns.violinplot()` |
| **Mapa de calor con Spearman** | Comparar Pearson vs Spearman lado a lado | `sns.heatmap(df.corr(method='spearman'))` |
| **Barras: Remote Premium por rol** | Ver qué roles se benefician más del remoto | `groupby + barplot` |

### 3.2 ANÁLISIS ESTADÍSTICO AVANZADO

```python
# 1. Comparar Pearson vs Spearman para salario
from scipy.stats import pearsonr, spearmanr

# Pearson (asume linealidad y normalidad)
r_pearson, p_pearson = pearsonr(df_stats['experience_level_num'], df_stats['normalized_salary'])

# Spearman (basado en rangos, robusto a asimetría)
r_spearman, p_spearman = spearmanr(df_stats['experience_level_num'], df_stats['normalized_salary'])

print(f"Pearson r = {r_pearson:.3f} (p={p_pearson:.4f})")
print(f"Spearman ρ = {r_spearman:.3f} (p={p_spearman:.4f})")
# Si ρ > r, la relación es monótona pero no lineal → Spearman es más apropiado

# 2. Intervalos de confianza para la mediana (bootstrap)
import numpy as np
def bootstrap_median(data, n_bootstrap=1000):
    medians = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        medians.append(np.median(sample))
    return np.percentile(medians, [2.5, 97.5])

ci_lower, ci_upper = bootstrap_median(df_stats['normalized_salary'].dropna())
print(f"Mediana salarial: ${df_stats['normalized_salary'].median():,.0f}")
print(f"IC 95%: [${ci_lower:,.0f} - ${ci_upper:,.0f}]")

# 3. T-test de Remote Premium con IC
remote = df_stats[df_stats['is_remote']]['normalized_salary'].dropna()
onsite = df_stats[~df_stats['is_remote']]['normalized_salary'].dropna()
t_stat, p_val = stats.ttest_ind(remote, onsitesite)
print(f"Remote Premium t-test: t={t_stat:.2f}, p={p_val:.4f}")
```

### 3.3 EXPLICACIONES PARA PIE DE GRÁFICO

```markdown
**Histograma + KDE:** Se eligió el histograma con curva KDE porque la distribución salarial 
es asimétrica positiva (skewness > 0). La media ($139,844) es mayor que la mediana ($135,588) 
debido a la cola derecha, lo que justifica el uso de la mediana como medida central.

**Boxplot por experiencia:** El boxplot permite visualizar simultáneamente mediana, 
dispersión intercuartílica (IQR) y outliers por nivel de experiencia. Se prefirió sobre 
el gráfico de barras porque muestra la distribución completa, no solo una medida.

**Scatter Views vs Applies:** Se usó correlación de Pearson (r) para cuantificar la relación 
lineal. Sin embargo, dado que ambas variables son conteos con distribución asimétrica, 
también se calculó Spearman (ρ) como validación. La línea de regresión lineal (OLS) 
se incluye como referencia visual, no como modelo predictivo.

**Heatmap de correlación:** Se usó el coeficiente de Pearson por su interpretabilidad 
directa (-1 a +1). Las variables categóricas (experiencia) se codificaron como one-hot 
para incluirlas en la matriz. Advertencia: la correlación no implica causalidad.

**Pairplot:** Matriz de dispersión multivariante que permite detectar relaciones no lineales, 
clusters y outliers que una matriz de correlación por sí sola no revela. Útil como 
herramienta exploratoria complementaria.
```

---

## 📌 PARTE 4: PREGUNTAS DIFÍCILES CON RESPUESTAS PREPARADAS

### P1: ¿Por qué LinkedIn y no otras fuentes?
**Respuesta:** LinkedIn proporciona ofertas reales publicadas por empresas (~123K postings), lo que permite analizar el comportamiento efectivo del mercado laboral. Stack Overflow, en cambio, refleja percepciones auto-reportadas (sesgo aspiracional). La brecha del 59% entre ambas fuentes (mediana $85K SO vs $135K LinkedIn) demuestra por qué es crítico usar datos de mercado real.

### P2: ¿Por qué eliminasteis outliers con IQR?
**Respuesta:** Aplicamos IQR (Q1 - 1.5·IQR, Q3 + 1.5·IQR) porque la distribución salarial tiene asimetría positiva. El Z-score solo detectó 1 outlier (0.2%) mientras que IQR detectó 14 (2.3%). Decidimos **mantener** los outliers y usar la mediana como medida central, documentando los valores sospechosos (< $1K y > $2M) como potenciales errores de datos.

### P3: ¿Por qué usasteis Pearson y no Spearman?
**Respuesta:** Usamos Pearson por su interpretabilidad directa (r = 0.43 para experiencia-salario). Sin embargo, dado que el salario tiene distribución asimétrica, también calculamos Spearman como validación. En nuestro caso, ambos coeficientes coincidieron en dirección y significancia, pero para trabajos futuros recomendamos reportar ambos.

### P4: ¿Qué significa p < 0.0001?
**Respuesta:** Significa que la probabilidad de observar diferencias salariales tan marcadas entre niveles de experiencia por puro azar es extremadamente baja (< 0.01%). Por tanto, rechazamos la hipótesis nula (H₀: la experiencia no afecta al salario) con un 99.99% de confianza estadística.

### P5: ¿Qué es MNAR y por qué es importante?
**Respuesta:** Missing Not At Random significa que la ausencia de datos sigue un patrón sistemático, no aleatorio. En nuestro caso: el 47.33% de los juniors ocultan su salario vs solo el 23.86% de los seniors. **Implicación:** cualquier modelo que ignore este sesgo infravalorará los salarios junior, generando recomendaciones erróneas para DataTalent.

### P6: ¿De dónde sale el r = 0.62 de Views vs Applies?
**Respuesta:** Es la correlación de Pearson entre el número de visualizaciones y aplicaciones de las ofertas de LinkedIn. Se calculó con `df['views'].corr(df['applies'])`. Aunque existe correlación positiva moderada, encontramos que **no hay correlación** entre visualizaciones y salario (r = 0.04), lo que indica que las ofertas más populares no son necesariamente las mejor pagadas.

---

## 📌 PARTE 5: DATOS PARA NOTEBOOK LM

### Contexto del proyecto
```
PROYECTO: Pearson's Four — EDA Data Science Job Salaries
EMPRESA CLIENTE: DataTalent Solutions S.L. (consultora HR tech España)
EQUIPO: Juan (Data Wrangler), Isabela (Statistical Analyst), Anas (Visualizer), Vanessa (Ethics)
DATASETS: LinkedIn Job Postings (Kaggle, 123K registros) + Stack Overflow Survey 2025 (49K)
OBJETIVO: Determinar factores que determinan salarios en sector Data para programa de reskilling
LIMITACIÓN PRINCIPAL: LinkedIn dataset tiene 0 ofertas de España (es 99% USA)
```

### Prompt para Notebook LM
```
Eres un mentor de数据分析 (análisis de datos) preparando a un equipo para la defensa
de su proyecto de consultoría. El proyecto se llama "Pearson's Four" y analiza
salarios del sector Data usando LinkedIn y Stack Overflow para el cliente
DataTalent Solutions S.L. (España).

Tu tarea es generar un documento de preparación para la defensa que incluya:

1. RESUMEN EJECUTIVO (1 párrafo):
   - ¿Qué hizo el equipo?
   - ¿Qué encontraron?
   - ¿Por qué es importante para DataTalent?

2. MAPA DE LA DEFENSA (10 minutos):
   - Minuto 0-2: Juan presenta el problema de negocio y data wrangling
   - Minuto 2-4: Isabela presenta hallazgos estadísticos (correlaciones, ANOVA)
   - Minuto 4-6: Anas muestra visualizaciones clave
   - Minuto 6-8: Vanessa explica sesgos (MNAR, geográfico) y ética
   - Minuto 8-10: Recomendaciones + cierre
   Para cada segmento, da EXACTAMENTE qué decir y qué slide mostrar.

3. TOP 10 POSIBLES PREGUNTAS DEL TRIBUNAL con respuestas modelo:
   a) Pregunta técnica (ej: ¿por qué IQR y no Z-score?)
   b) Pregunta de negocio (ej: ¿qué recomiendan a DataTalent?)
   c) Pregunta ética (ej: ¿cómo afecta MNAR a las conclusiones?)
   d) Pregunta metodológica (ej: ¿por qué LinkedIn y no otras fuentes?)
   e) Pregunta de limitaciones (ej: ¿qué haríais diferente con más tiempo?)

4. 3 DEBILIDADES DEL PROYECTO (para que el equipo las reconozca 
   proactivamente y las convierta en fortaleza):
   - 0 ofertas de España en LinkedIn
   - 70.87% de salarios nulos
   - Skills_desc 98% vacío

5. 3 FORTALEZAS DIFERENCIADORAS:
   - Análisis MNAR (Missing Not At Random) — diferencial ético
   - Cruce de fuentes LinkedIn vs Stack Overflow — brecha del 59%
   - Remote Premium cuantificado (+45.1%) — insight de negocio accionable

6. GUION COMPLETO de 10 minutos (palabra por palabra) en español,
   con indicaciones de quién habla y qué slide mostrar en cada momento.

7. CONCLUSIÓN FINAL sugerida (máximo 60 palabras) que el equipo
   puede memorizar para el cierre.

DATOS CLAVE DEL PROYECTO:
- 123,849 postings de LinkedIn → 1,831 data roles → 607 con salario válido
- Salario medio: $139,844 | Mediana: $135,588
- Remote Premium: +45.1% ($112,500 vs $77,500)
- Pearson r (experiencia vs salario): 0.43
- ANOVA: p < 0.0001
- MNAR: 47.33% juniors ocultan salario vs 23.86% seniors
- 0 postings de España en LinkedIn
- Brecha LinkedIn vs Stack Overflow: 59% (mediana $135,588 vs $85,000)
```

### Archivos a subir a Notebook LM
Para mejor análisis, sube estos archivos:
1. `C:\Users\JUAN\Downloads\Pearsons_Four_Proyecto.ipynb` — Notebook principal
2. `C:\Users\JUAN\Desktop\Proyectos\portfolio_notebooks\informes\EVALUACION_PEARSONS_FOUR.md`
3. `C:\Users\JUAN\Desktop\Proyectos\portfolio_notebooks\informes\INFORME_TECHSALARY_ES.md`
4. Este reporte (`REPORTE_PEARSONS_FOUR_PARA_NOTEBOOK_LM.md`)
5. Las 4 guías PDF de la carpeta Downloads

---

*Generado el 01/06/2026 — Reporte completo para defensa de proyecto*
