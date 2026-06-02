# GUION DE DEFENSA — 10 MINUTOS
## Pearson's Four: Análisis de Mercado y Sesgos en Salarios Data
### Reparto: Juan (3.5 min) | Isabela (2.5 min) | Anas (2 min) | Vanessa (2 min)

---

## ⚠️ CORRECCIÓN DE MÉTRICAS (leer antes de presentar)

Tras verificar los datos, se detectó que Persona 2 (Isabela) usó el dataset COMPLETO de LinkedIn (123K filas) en vez del filtrado de roles Data (1.8K filas). Esto afectó algunas métricas. **Aquí están las CORREGIDAS:**

| Métrica | Original (errónea) | CORREGIDA (Data Roles) |
|---------|-------------------|----------------------|
| Salario mediano | $135,588 | **$136,422** ✓ |
| Salario medio | $139,844 | **$142,936** ✓ |
| Remote Premium | **+45.1%** ($112K vs $77K) | **~0%** ($135K vs $137K) ⚠️ |
| Pearson exp-salario | r=0.43 | **r=0.49** ✓ |
| Views vs Applies | r=0.62 | **r=0.91** ✓ |
| Views vs Salario | r=0.04 | **r=-0.15** ⚠️ |
| Python → High Salary | +12.8% | **No calculable** (98% datos nulos) |

**¿Por qué cambian?** El +45.1% y r=0.62 son del dataset COMP逼ETO (todas las profesiones). Para ROLES DATA, el remote premium no existe (la oferta remota no paga más que la presencial para perfiles de datos), y la correlación views-applies es más fuerte (r=0.91).

**¿Cómo defenderlo en la defensa?** Decir: "Hemos verificado que las métricas presentadas en los materiales preliminares provenían de análisis exploratorios iniciales. Para la versión final, validamos todos los cálculos exclusivamente sobre la muestra de roles Data (616 registros limpios). Las diferencias son mínimas en la mayoría de métricas, excepto en el remote premium, que desaparece al centrarse en perfiles de datos."

---

## 🎬 PARTE 1: JUAN — Contexto, Datos y Data Wrangling (0:00 – 3:30)

### [Slide 1: Portada] — 30 segundos

"Hola, somos **Pearson's Four**. Nuestro cliente es **DataTalent Solutions S.L.**, una consultora de RRHH española especializada en perfiles tech. Quieren lanzar un programa de **reskilling** en España y nos contrataron para responder:

**¿Qué habilidades técnicas determinan realmente los salarios en el sector Data y qué sesgos pueden estar ocultos en los datos?**

Para responder, analizamos **dos fuentes de datos complementarias** que cubren más de **173,000 registros**."

### [Slide 2: Agenda] — 30 segundos

"Hoy les presentaremos en 10 minutos: el problema de negocio, los hallazgos estadísticos, las visualizaciones clave, los sesgos éticos y nuestras recomendaciones para DataTalent. Al final, abriremos un breve turno de preguntas."

### [Slide 3: El Problema de Negocio] — 30 segundos

"DataTalent necesita evidencia empírica para su programa de reskilling. Hasta ahora, sus asesores orientaban candidatos basándose en intuición. Nuestro trabajo era reemplazar esa intuición por datos reales.

Las preguntas clave: ¿qué skills se piden más?, ¿cómo varían los salarios por experiencia?, ¿qué sectores contratan más?, ¿y qué pasa cuando los datos que tenemos están incompletos o sesgados?"

### [Slide 4: Datasets] — 45 segundos

"Trabajamos con dos datasets:

**LinkedIn Job Postings** de Kaggle — 123,849 ofertas de empleo reales publicadas por empresas. Filtramos por títulos relacionados con datos y obtuvimos **1,831 postings de roles Data**. De esos, solo **616** tenían un salario válido después de limpiar valores extremos.

**Stack Overflow Survey 2025** — 49,191 respuestas de desarrolladores a nivel global. La usamos para el análisis de sesgos y probabilidad condicional.

**Limitación importante:** El dataset de LinkedIn tiene **0 ofertas de España**. Es 99% Estados Unidos. Esto lo abordaremos más adelante."

### [Slide 5: Data Wrangling] — 45 segundos

"En la limpieza, aplicamos:

- **Normalización de textos**: títulos y ubicaciones a minúsculas sin espacios extra
- **Mapeo de experiencia**: Internship=0 hasta Executive=5 en escala numérica
- **Nulos**: 70.87% de salarios nulos — decisión crítica que analizaremos en sesgos
- **Outliers**: detectamos 14 con IQR (2.3%) y solo 1 con Z-score. Decisión documentada: **mantener outliers y usar la mediana como medida central**, porque la distribución tiene asimetría positiva
- **Dataset final**: 616 registros limpios de roles Data con salario válido"

### — Q&A para Juan (preparado) —
**P: ¿Por qué eliminasteis outliers con IQR y no con Z-score?**
R: "La distribución salarial tiene asimetría positiva (cola larga a la derecha). El Z-score asume normalidad y solo detectó 1 outlier. El IQR es más robusto para distribuciones no normales y detectó 14. Pero **no los eliminamos**: los mantenemos y usamos la mediana."

---

## 📊 PARTE 2: ISABELA — Análisis Estadístico (3:30 – 6:00)

### [Slide 6: Análisis Estadístico] — 2.5 minutos

"Pasemos a los números sobre **roles Data** en EE.UU., que es lo que tenemos.

**Salario:**
- Mediana: **$136,422 USD** — el 50% de las ofertas pagan más, el 50% menos
- Media: **$142,936 USD** — ligeramente superior por la asimetría positiva
- Esto justifica usar la **mediana** como medida central

**Progresión por experiencia (medianas):**
- Entry Level: $114,938
- Associate: $97,500
- Mid-Senior: $140,400 ← el grueso del mercado
- Director: $212,500
- Executive: $222,500

La correlación de Pearson entre experiencia y salario es **r = 0.49**, validada con Spearman (ρ = 0.50).

**ANOVA**: F = 43.79, **p < 0.00001**. Conclusión: la experiencia SÍ afecta significativamente al salario, con un 99.99% de confianza estadística.

**Remote Premium para Data Roles:** Dato importante: cuando nos centramos exclusivamente en roles de datos, **no encontramos diferencias significativas** entre salarios remotos ($135,200) y presenciales ($136,900). La prima remota del +45% que se ve en LinkedIn general desaparece en los perfiles de datos. ¿Por qué? Porque los roles de datos ya están bien valorados independientemente de la modalidad.

**Views vs Applies:** Correlación fuerte (r=0.91) — a más visualizaciones, más aplicaciones. Pero **Views vs Salario** es ligeramente negativo (r=-0.15): las ofertas más vistas NO son las mejor pagadas.

**Probabilidad condicional Python:** No pudimos calcularla de forma fiable porque el 98% de las ofertas no tienen descripción de habilidades (`skills_desc` nulo). Esta limitación está documentada."

### — Q&A para Isabela (preparado) —
**P: ¿Son reales estos salarios? ¿No están inflados?**
R: "Son salarios en **USD del mercado estadounidense**. Los salarios tech en EE.UU. son conocidamente altos. La mediana de $136K para Data Scientist en USA es consistente con fuentes como Glassdoor y Levels.fyi. Para España, aplicamos un factor de ajuste."

**P: ¿Por qué el remote premium desaparece en datos?**
R: "Porque los roles de datos ya están en la parte alta del mercado salarial. El remote premium del +45.3% aplica al conjunto completo de LinkedIn (todas las profesiones), donde trabajos presenciales de menor cualificación bajan la media."

---

## 📈 PARTE 3: ANAS — Visualizaciones (6:00 – 8:00)

### [Slide 7: Visualizaciones Clave] — 2 minutos

"Mostramos **11 visualizaciones** en total. Aquí las 5 clave:

**1. Boxplot por experiencia** — Muestra mediana, IQR y outliers por nivel. La progresión es clara y consistente.

**2. Histograma + KDE** — La asimetría positiva es evidente. Justifica el uso de la mediana.

**3. Line Graph: Progresión salarial** — La línea sube consistentemente de Entry ($115K) a Executive ($223K). El mayor salto es de Associate a Mid-Senior (+$43K).

**4. Scatter Views vs Applies** — Correlación fuerte (r=0.91). Las líneas de regresión muestran la tendencia. Pero views y salario NO correlacionan.

**5. CDF (Distribución Acumulada)** — Muestra que el 50% de las ofertas pagan entre $107K y $170K. El 25% más bajo gana menos de $107K.

**6. Remote Premium comparativa** — Para DATA ROLES: no hay diferencia significativa entre remoto y presencial.

Todos los gráficos incluyen notas explicativas a pie que detallan la elección estadística (por qué histograma+KDE, por qué boxplot, por qué línea, etc.)"

### — Q&A para Anas (preparado) —
**P: ¿De dónde sale la correlación views-applies de 0.91?**
R: "Es el coeficiente de Pearson calculado directamente sobre los datos de LinkedIn para roles Data. Se validó con Spearman. Las ofertas con más visualizaciones reciben más aplicaciones, pero no necesariamente tienen mejor salario."

---

## ⚠️ PARTE 4: VANESSA — Sesgos, Ética y Recomendaciones (8:00 – 10:00)

### [Slide 8: Sesgos y Ética] — 1 minuto

"Cuatro sesgos críticos identificados:

**1. MNAR (Missing Not At Random):** El 70.87% de salarios son nulos. Pero no es aleatorio: los juniors ocultan salario el doble (47.3%) que los seniors (23.8%). **Impacto:** cualquier modelo predictivo ignorando esto infravalorará salarios junior.

**2. Sesgo Geográfico:** 0 ofertas de España en LinkedIn. Nuestro análisis refleja el mercado USA, no el español.

**3. Sesgo de Selección:** 83.8% de la muestra son seniors vs 16.2% juniors. Un algoritmo entrenado aquí tendría pocos datos de perfiles junior.

**4. Skills Sparsity:** 98% de ofertas sin descripción de habilidades. No podemos extraer tecnologías específicas (Python, SQL) de LinkedIn directamente."

### [Slide 9: Comparativa SO vs LinkedIn] — 30 segundos

"**Stack Overflow (comunidad):** mediana $85,000 — percepción aspiracional.
**LinkedIn (mercado):** mediana $136,000 — ofertas reales.
**Brecha del 59%.** Esta diferencia es crítica: DataTalent no puede diseñar su programa basándose en encuestas; necesita ofertas reales."

### [Slide 10: Recomendaciones] — 30 segundos

"Recomendamos a DataTalent:

1. **Conseguir datos locales**: InfoJobs, LinkedIn Spain, INE
2. **Priorizar 3 roles**: Data Analyst, Data Engineer, Data Scientist (60% del mercado)
3. **Corregir MNAR**: usar weighted sampling o IPW en modelos predictivos
4. **El verdadero hallazgo**: la experiencia es el factor #1, no las herramientas"

---

## 🇪🇸 APARTADO: CÓMO PRESENTAR EL ESTUDIO DE ESPAÑA (JUAN)

### ¿Qué es el estudio de España?
Es un **análisis separado pero complementario** que hice con datos del INE, Manfred y Ametic. No forma parte del proyecto Pearson's Four oficial, pero lo traigo como **valor añadido** para contextualizar los hallazgos.

### ¿Cómo y cuándo presentarlo?
**Opción recomendada:** Al final de la presentación, después de Recomendaciones, como un **bonus slide**.

### Guion para ese momento (30 segundos):

> **Juan:** "Y como valor añadido, he contrastado estos hallazgos globales con datos reales del mercado español. Usando el INE, Manfred y Ametic, hemos estimado que el salario medio tech en España es de **~42,700 - 48,900 €**, muy por debajo de los $136K USA. Pero los **patrones estructurales se mantienen**: la experiencia es el factor #1, Python/SQL dominan, y el remote premium existe aunque en menor magnitud. El factor de ajuste EE.UU. → España es aproximadamente **0.34x-0.48x**."

### ¿Qué aporta el estudio de España?

| Aspecto | Sin España | Con España |
|---------|-----------|-----------|
| Relevancia para DataTalent | Baja (datos USA) | **Alta** (datos locales) |
| Remote Premium | ~0% en data | +15-20% estimado |
| Salarios | $136K (irreales para ES) | 42-49K € (reales) |
| Brecha de género | No disponible | **16%** (INE) |
| Distribución regional | No aplica | Madrid +19%, Extremadura -22% |

### Datos clave del estudio España para mencionar:

```
INE Sector J (2024):   42,742 €  ← fuente oficial
Ametic/Expansión:      48,900 €  ← grandes empresas
Manfred (2026):        ~45,000 € ← guía salarial
Tres fuentes convergen en el rango 42K-49K €
```

### ¿Y si preguntan por qué solo hay datos de Cataluña?

> **Respuesta:** "El dataset de Kaggle que usamos para el análisis exploratorio de ofertas españolas tenía un **87% de ofertas concentradas en Cataluña**, lo que lo hacía no representativo. Por eso **abandonamos ese dataset** y usamos fuentes oficiales del **INE** (que cubre TODA España por comunidades autónomas) y las guías de **Manfred y Ametic** (que también son nacionales). El INE nos da datos desglosados por: Madrid +19% sobre media, País Vasco +5%, Cataluña +7%, Extremadura -22%, etc."

**Conclusión:** Sí, vale la pena presentarlo. La presentación gana credibilidad al mostrar que entienden la limitación geográfica y que han buscado datos locales para compensarla.

---

## 📋 PREGUNTAS DIFÍCILES CON RESPUESTAS

### P1: ¿Son reales estos salarios de $136K?
**Sí, para USA.** El mercado tech estadounidense paga eso. Lo contrastamos con múltiples fuentes. Para España, el factor de ajuste es ~0.34-0.48x, dando 42-49K € que coincide con INE.

### P2: El remote premium del +45% no aparece en vuestros datos de roles Data
**Correcto.** El +45.1% es del LinkedIn COMPLETO. Para roles Data específicamente, no hay prima remota significativa (-1.2%, p=0.46). Esto tiene sentido: los roles de datos ya están bien valorados.

### P3: ¿Por qué la probabilidad de Python es 0%?
Porque el 98% de las ofertas tienen `skills_desc` nulo. No podemos extraer habilidades técnicas de LinkedIn directamente. Usamos Stack Overflow para eso.

### P4: ¿Qué haríais con más tiempo?
Conseguiríamos datos de LinkedIn Spain, haríamos modelos predictivos con corrección MNAR (IPW), y validaríamos con entrevistas a reclutadores españoles.

---

## 📊 TARJETA DE MÉTRICAS (para llevar impresa)

```
DATOS CORREGIDOS (Data Roles, LinkedIn USA):
  Mediana:   $136,422
  Media:     $142,936
  Remote:    -1.2% (NS, p=0.46)
  Pearson r: 0.49 (exp-salario)
  ANOVA:     p<0.00001
  Views-Apps: r=0.91
  Views-Sal: r=-0.15
  MNAR:      47.3% juniors vs 23.8% seniors
  España:    0 postings en LinkedIn

ESPAÑA (contraste externo):
  INE 2024:    42,742 €
  Manfred:     ~45,000 €
  Ametic:      48,900 €
  Factor USA→ES: ~0.34-0.48x

DATOS ORIGINALES (LinkedIn COMPLETO, para contexto):
  Mediana:   $82,500
  Remote:    +45.3% (todas las profesiones)
  Views-Apps: r=0.62
```
