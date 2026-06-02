# PROMPT DEFINITIVO — Slides + Speeche Balanceados
## 10 min | 10 slides | Reparto equitativo

---

## 📐 ESTRUCTURA BASE (10 slides, ~10 min)

```
Slide 1  → Juan (portada+problema)
Slide 2  → Juan (datos+wrangling)        ← Juan: 2 slides + cierre = 2:30
─────────────────────────────────────
Slide 3  → Isabela (descriptivos) 
Slide 4  → Isabela (correlaciones+test)  ← Isabela: 2 slides = 2:30
─────────────────────────────────────
Slide 5  → Anas (visualizaciones I)
Slide 6  → Anas (visualizaciones II)     ← Anas: 2 slides = 2:30
─────────────────────────────────────
Slide 7  → Vanessa (sesgos)
Slide 8  → Vanessa (comparativa+recom)   ← Vanessa: 2 slides = 2:30
─────────────────────────────────────
Slide 9  → Juan (conclusión España opcional)
Slide 10 → Juan (cierre)                 ← Cierre
```

---

## 📋 PROMPT PARA GENERAR SLIDES

```
Genera una presentación de 10 diapositivas para defensa de 10 minutos.
TÍTULO: "Pearson's Four — EDA Data Science Job Salaries"
CLIENTE: DataTalent Solutions S.L. | Módulo II | Junio 2026
EQUIPO: Juan | Isabela | Anas | Vanessa
REPARTO: Cada persona presenta 2 diapositivas (~2:30 cada uno).
         Juan abre y cierra.

MÉTRICAS CORREGIDAS (Data Roles, LinkedIn USA, n=616):
  Mediana: $136,422 | Media: $142,936
  Remote Premium Data Roles: -1.2% (NO significativo, p=0.46)
  NOTA: El +45.3% existe para LinkedIn COMPLETO, pero NO aplica a Data Roles
  Pearson exp-salario: r=0.49 | Spearman: ρ=0.50
  Views-Applies: r=0.91 | Views-Salario: r=-0.15
  ANOVA: F=43.79, p<0.00001
  MNAR: 47.3% juniors vs 23.8% seniors ocultan salario
  Brecha SO vs LinkedIn: $85K vs $136K = +59%
  España: 0 postings en LinkedIn

=== DIAPOSITIVA 1 — JUAN (Portada + Problema) [~1 min] ===
Título: "Pearson's Four — Análisis de Mercado Data"
Subtítulo: DataTalent Solutions S.L. necesita evidencia empírica para su programa de reskilling.
Preguntas: ¿Qué skills? ¿Cuánto pagan? ¿Qué sectores? ¿Hay sesgos?
Pie: Juan | Isabela | Anas | Vanessa

=== DIAPOSITIVA 2 — JUAN (Datos + Wrangling) [~1:30] ===
LinkedIn: 123,849 → 1,831 Data Roles → 616 con salario válido
Stack Overflow: 49,191 respuestas
Data Wrangling: textos normalizados, experiencia mapeada (0-5)
70.87% nulos en salario | Outliers IQR: 14 (mantenidos, usamos mediana)
0 ofertas de España (sesgo geográfico documentado)
Iconos: dataset, filtro, limpieza, advertencia

=== DIAPOSITIVA 3 — ISABELA (Estadísticas Descriptivas) [~1:15] ===
Mediana: $136,422 ← medida principal (asimetría positiva)
Media: $142,936
Remote Premium Data Roles: -1.2%  (NO significativo)
  Aclaración: El +45.3% es para LinkedIn completo, no para Data Roles
Progresión por experiencia:
  Entry $115K → Mid-Senior $140K → Director $213K → Executive $223K
Gráfico: barra o línea de progresión

=== DIAPOSITIVA 4 — ISABELA (Correlaciones + Tests) [~1:15] ===
Pearson exp-salario: r=0.49 | Spearman: ρ=0.50 (moderada-fuerte)
Views-Applies: r=0.91 (fuerte) | Views-Salario: r=-0.15 (casi nula)
ANOVA: F=43.79, p<0.00001 → la experiencia SÍ afecta al salario
Heatmap de correlaciones como apoyo visual

=== DIAPOSITIVA 5 — ANAS (Visualizaciones I) [~1:15] ===
Boxplot: progresión clara por experiencia
Histograma + KDE: asimetría positiva → justifica mediana
Line Graph: progresión — mayor salto Associate→Mid-Senior (+$43K)
CDF: 50% de ofertas entre $107K y $170K
Mosaico de 4 miniaturas con título cada una

=== DIAPOSITIVA 6 — ANAS (Visualizaciones II) [~1:15] ===
Scatter Views vs Applies: r=0.91 con línea de regresión
Remote Premium Data Roles: barras comparativas (~0% diferencia)
Pairplot o Violin: refuerzan relación experiencia-salario
Cada gráfico con nota: elección estadística justificada
Mosaico de 3 miniaturas

=== DIAPOSITIVA 7 — VANESSA (Sesgos) [~1:15] ===
MNAR: 47.3% juniors ocultan salario vs 23.8% seniors
  → Modelos infravalorarían salarios junior
Geográfico: 0 ofertas España → datos no generalizables
Selección: 84% seniors en muestra → penaliza perfiles junior
Skills: 98% skills_desc nulo → NO podemos extraer Python/SQL de LinkedIn
Diagrama: 4 recuadros con iconos de advertencia

=== DIAPOSITIVA 8 — VANESSA (Comparativa + Recomendaciones) [~1:15] ===
Stack Overflow (comunidad): $85K
LinkedIn (mercado): $136K
Brecha: +59% → DataTalent debe usar ofertas reales, no encuestas
Recomendaciones:
  1. Datos locales España (InfoJobs, INE, LinkedIn Spain)
  2. Priorizar 3 roles: Data Analyst, Engineer, Scientist
  3. Corregir MNAR con weighted sampling
  4. La experiencia es el factor #1

=== DIAPOSITIVA 9 — JUAN (Contexto España — Opcional) [~30s] ===
Contraste con datos INE + Manfred + Ametic:
  INE Sector J 2024: 42.742€ | Manfred: ~45.000€ | Ametic: 48.900€
  Factor ajuste USA→España: ~0.34-0.48x
  Los patrones se mantienen: experiencia, skills, remote premium (menor)
Solo mostrar si hay tiempo. Si no, omitir.

=== DIAPOSITIVA 10 — JUAN (Cierre) [~30s] ===
"La experiencia es el principal determinante salarial en Data.
Los datos faltantes no son aleatorios: ignorarlos genera decisiones sesgadas.
Combinar estadística, negocio y ética para decisiones basadas en datos."
Pearson's Four | Módulo II | ¿Preguntas?
```

---

## 🎤 SPEECH 4 PERSONAS (balanceado)

| Slide | Quién | Tiempo | Acumulado |
|-------|-------|--------|-----------|
| 1 | **Juan** — Portada + Problema | 1:00 | 1:00 |
| 2 | **Juan** — Datos + Wrangling | 1:30 | 2:30 |
| 3 | **Isabela** — Estadísticas descriptivas | 1:15 | 3:45 |
| 4 | **Isabela** — Correlaciones + Tests | 1:15 | 5:00 |
| 5 | **Anas** — Visualizaciones I | 1:15 | 6:15 |
| 6 | **Anas** — Visualizaciones II | 1:15 | 7:30 |
| 7 | **Vanessa** — Sesgos | 1:15 | 8:45 |
| 8 | **Vanessa** — Comparativa + Recomendaciones | 1:15 | 10:00 |
| 9 | **Juan** — España (opcional, si sobra tiempo) | — | — |
| 10 | **Juan** — Cierre | 0:30 | 10:00 |

### Guion palabra por palabra:

**[Slide 1 — Juan, 1:00]** "Hola, somos Pearson's Four. DataTalent Solutions, una consultora HR tech española, nos contrató para responder: ¿qué factores determinan los salarios en el sector Data? Y más importante aún: ¿qué ocurre cuando los datos que tenemos están incompletos o sesgados? Hoy les presentamos nuestro análisis en 10 minutos."

**[Slide 2 — Juan, 1:30]** "Trabajamos con dos fuentes: LinkedIn Job Postings (123K ofertas reales, filtradas a 1.831 roles Data) y Stack Overflow Survey 2025 (49K respuestas). En limpieza: normalizamos textos, mapeamos experiencia, detectamos 70.87% de nulos en salario y 14 outliers por IQR. Decisión: mantuvimos outliers y usamos mediana. Dato crítico: 0 ofertas de España."

**[Slide 3 — Isabela, 1:15]** "Sobre los 616 Data Roles con salario válido: la mediana es $136,422, la media $142,936. Usamos mediana por asimetría positiva. Remote Premium: para Data Roles no hay diferencia significativa (-1.2%, p=0.46). El +45.3% que aparece en LinkedIn general aplica a TODAS las profesiones, no a Data. Progresión: Entry $115K, Mid-Senior $140K, Executive $223K."

**[Slide 4 — Isabela, 1:15]** "Correlaciones: experiencia-salario r=0.49 (Pearson), ρ=0.50 (Spearman). Views-Applies r=0.91 — correlación fuerte. Views-Salario r=-0.15 — las ofertas populares no pagan más. ANOVA: F=43.79, p<0.00001. Conclusión: la experiencia afecta significativamente al salario."

**[Slide 5 — Anas, 1:15]** "Primer bloque de visualizaciones: Boxplot muestra progresión clara Entry→Executive. Histograma+KDE confirma asimetría positiva. Line Graph: el mayor salto es de Associate a Mid-Senior (+$43K). CDF: 50% de ofertas entre $107K y $170K. Cada gráfico incluye nota explicativa."

**[Slide 6 — Anas, 1:15]** "Segundo bloque: Scatter Views vs Applies con r=0.91 y línea de regresión. Remote Premium: comparativa directa — prácticamente igual para Data Roles. Violin/Pairplot refuerzan que experiencia es el factor principal."

**[Slide 7 — Vanessa, 1:15]** "Cuatro sesgos identificados: 1) MNAR: 47.3% de juniors ocultan salario vs 23.8% seniors — cualquier modelo ignorando esto infravalorará salarios junior. 2) Geográfico: 0 ofertas de España. 3) Selección: 84% seniors. 4) Skills: 98% nulo."

**[Slide 8 — Vanessa, 1:15]** "Comparativa: SO $85K vs LinkedIn $136K — brecha del 59%. DataTalent debe basarse en ofertas reales. Recomendaciones: 1) datos locales, 2) priorizar 3 roles Data, 3) corregir MNAR, 4) la experiencia es el factor #1."

**[Slide 10 — Juan, 0:30]** "Conclusión: la experiencia es el principal determinante salarial en Data. Los datos faltantes no son aleatorios e ignorarlos genera decisiones sesgadas. Combinar estadística, negocio y ética. Gracias. ¿Preguntas?"

---

## 🎤 SPEECH 3 PERSONAS (sin Anas, balanceado)

| Slide | Quién | Tiempo | Acumulado |
|-------|-------|--------|-----------|
| 1 | **Juan** — Portada + Problema | 1:00 | 1:00 |
| 2 | **Juan** — Datos + Wrangling | 1:30 | 2:30 |
| 3 | **Isabela** — Estadísticas descriptivas | 1:00 | 3:30 |
| 4 | **Isabela** — Correlaciones + Tests | 1:00 | 4:30 |
| 5 | **Isabela** — Visualizaciones I | 1:30 | 6:00 |
| 6 | **Vanessa** — Visualizaciones II | 1:00 | 7:00 |
| 7 | **Vanessa** — Sesgos | 1:15 | 8:15 |
| 8 | **Vanessa** — Comparativa + Recomendaciones | 1:15 | 9:30 |
| 9 | **Juan** — Cierre | 0:30 | 10:00 |

### Cambios respecto a versión 4 personas:

**[Isabela añade Slide 5, 1:30]**
"Y ahora las visualizaciones. Primero: Boxplot — la progresión es clara, de Entry a Executive la mediana se duplica. Histograma+KDE — la asimetría positiva justifica usar mediana. Line Graph — el mayor salto salarial es de Associate a Mid-Senior (+$43K). CDF — el 50% de ofertas Data están entre $107K y $170K."

**[Vanessa añade Slide 6, 1:00 antes de entrar a sesgos]**
"Completando las visualizaciones: el Scatter muestra correlación fuerte entre views y applies (r=0.91). La comparativa Remote Premium confirma que para Data Roles no hay diferencia significativa. Estos gráficos refuerzan que la experiencia es el factor visualmente más claro."

**[Luego continúa normal con Slides 7 y 8]**

**[Juan — Cierra en Slide 9 en vez de 10]**
Misma conclusión.

### Tabla de tiempos 3 personas:

| Min | Quién | Tema |
|-----|-------|------|
| 0:00–2:30 | **Juan** | Portada + Problema + Datos + Wrangling |
| 2:30–4:30 | **Isabela** | Estadísticas + Correlaciones + Tests |
| 4:30–6:00 | **Isabela** | Visualizaciones I (Boxplot, Hist, Line, CDF) |
| 6:00–7:00 | **Vanessa** | Visualizaciones II (Scatter, Remote) |
| 7:00–9:30 | **Vanessa** | Sesgos + Comparativa + Recomendaciones |
| 9:30–10:00 | **Juan** | Cierre |
```

---

## 📋 MÉTRICAS DEFINITIVAS (para imprimir)

```
DATA ROLES (n=616, LinkedIn USA):
  Mediana: $136,422  |  Media: $142,936
  Remote: -1.2% (NS) |  r(exp)=0.49
  r(v-apps)=0.91     |  r(v-sal)=-0.15
  ANOVA: p<0.00001   |  MNAR: 47% vs 24%

CONTEXTO LinkedIn COMPLETO (NO Data Roles):
  Remote: +45.3%     |  r(v-apps)=0.62

ESPAÑA:
  INE: 42,742€ | Manfred: 45K€ | Ametic: 48.9K€
  Factor: ~0.34-0.48x
```
