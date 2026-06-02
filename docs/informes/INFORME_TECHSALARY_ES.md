# Informe Completo: Análisis Salarial del Sector Tech en España

**Autor**: Análisis automatizado con datos reales  
**Fecha**: Mayo 2026

---

## 1. Objetivo del Proyecto

Construir un análisis salarial del sector tecnológico español usando **datos reales**, no sintéticos. Partiendo de 4 datasets de Kaggle (ofertas de empleo, trabajo remoto, PIB per cápita y demografía), el objetivo era:

- Explorar el mercado laboral tech en España
- Identificar los factores que determinan el salario
- Entrenar un modelo de regresión salarial
- Extraer conclusiones accionables

---

## 2. Flujo de Trabajo (Pipeline)

### Fase 1: Ingesta y Limpieza (Kaggle)

| Dataset | Registros | Problema | Solución |
|---------|-----------|----------|----------|
| Ofertas de empleo | 247 | Comas dentro de campos (ubicación, título) | Parser personalizado que rescata 248 registros |
| Demografía (1955-2050) | 24 filas | Formato europeo (coma como separador decimal) | Parseo con reemplazo de comas |
| PIB per cápita por región | 19 regiones × 17 años | Formato largo vs ancho | Melt + merge |
| Trabajo remoto | 17 regiones | Sin problemas mayores | Carga directa |

### Fase 2: Ingeniería de Variables

- **Geografía**: Mapeo provincia → Comunidad Autónoma (232/248 mapeadas)
- **Clasificación de roles**: Regex para Data (238) vs IT/Software (65)
- **Variable derivada**: `premium_salarial_regional` (ratio salarial respecto a PIB)
- **Merge final**: LEFT JOIN de ofertas + PIB + remoto → dataset maestro de 248 registros

### Fase 3: Análisis Exploratorio (EDA)

Se generaron **10 visualizaciones**:

1. Tendencia del PIB por región (2000-2016)
2. Distribución del PIB (2016)
3. Distribución de empleo remoto por región
4. Tendencias demográficas (población, edad mediana, dependencia)
5. Clasificación de roles (Data vs IT)
6. Mapa de calor de correlaciones (PIB + remoto + tech)
7. Dispersión PIB vs empleo remoto
8. Distribución por nivel de experiencia
9. Cuota de trabajo remoto por región
10. *(Añadido después)* Tendencia salarial real INE 2008-2024

### Fase 4: Modelo de Regresión (Primer Intento — FALLIDO)

Se entrenaron dos modelos:

| Modelo | R² (test) | MAE | Problema |
|--------|-----------|-----|----------|
| Random Forest | 0.82 | 1.628 € | Solo 1/248 ofertas tenía salario real |
| Regresión Lineal | 0.22 | 4.895 € | Sin poder predictivo real |

**Conclusión**: El R² de 0.82 es **engañoso**. El modelo aprendió la fórmula sintética que usamos para generar los salarios de entrenamiento, no patrones reales del mercado. La importancia de características mostraba `exp_code = 0.987` — el modelo solo usaba el nivel de experiencia porque era la única variable con varianza artificial.

### Fase 5: Corrección con Fuentes Reales (INE + Manfred + Ametic)

Se abandonó el enfoque de ML y se reemplazó por **estimaciones basadas en datos de mercado reales**:

| Fuente | Dato | Método de obtención |
|--------|------|---------------------|
| **INE Tabla 28185** | Salario medio sector J (Información y comunicaciones): 42.741 € (2024) | Archivo PC-Axis (.px) descargado y parseado |
| **INE Tabla 28191** | Salarios medios por CCAA (percentiles) | Archivo PC-Axis (.px) descargado |
| **Manfred Guía Salarial 2026** | Rangos por rol y experiencia (Backend: 20-55K, Data Scientist: 25-75K) | Extraído del sitio web |
| **Ametic/Expansión 2025** | Media tech: 48.900 € | Artículo de prensa |
| **INE Población** | España: 49.570.725 hab. (ene 2026) | Estadística Continua de Población |

---

## 3. Resultados Definitivos

### 3.1 Salario Real del Sector Tech (España, 2024)

| Métrica | Valor |
|---------|-------|
| Salario medio INE Sector J (2024) | **42.741 €** |
| Salario medio nacional (todos los sectores) | 29.540 € |
| **Prima salarial del sector tech** | **+44.7%** |
| Salario medio Ametic/Expansión (2025) | 48.900 € |
| Mediana Backend Manfred (2026) | ~45.000 € |
| **Rango de convergencia inter-fuentes** | **42.700 – 48.900 €** |

### 3.2 Evolución Histórica (INE 2008-2024)

```
2008: 30.628 €
2010: 32.426 €
2012: 32.522 €
2014: 32.754 €
2016: 32.448 €
2018: 33.118 €
2020: 35.664 €
2022: 37.439 €
2024: 42.742 €
```

**Crecimiento total 2008-2024**: +39.6%  
**Aceleración pospandemia (2020-2024)**: +19.9% en solo 4 años

### 3.3 Brecha Salarial de Género en Tech (INE 2024)

| Sexo | Salario Medio | Diferencia |
|------|--------------|------------|
| Hombres | 45.054 € | — |
| Mujeres | 38.807 € | -13.9% respecto a hombres |
| Ambos sexos | 42.742 € | **Gap: 16,1%** (los hombres ganan 16% más) |

La brecha se ha mantenido constante (~15-16%) desde 2008.

### 3.4 Por Nivel de Experiencia (Manfred 2026 + Multiplicador INE)

| Nivel | Rango Estimado | Medio |
|-------|---------------|-------|
| Junior | 27.000 – 35.000 € | ~30.000 € |
| Mid | 35.000 – 47.000 € | ~41.000 € |
| Senior | 49.000 – 70.000 € | ~53.000 € |

### 3.5 Por Región (Multiplicadores INE 2024)

| Comunidad Autónoma | Salario Medio (todos los sectores) | Multiplicador | Salario Tech Estimado |
|-------------------|-----------------------------------|---------------|----------------------|
| **Madrid** | 35.170 € | **×1.19** | **~50.900 €** |
| **País Vasco** | 31.064 € | ×1.05 | ~44.900 € |
| **Navarra** | 32.605 € | ×1.10 | ~47.100 € |
| **Cataluña** | 31.730 € | ×1.07 | ~45.800 € |
| **Aragón** | 28.062 € | ×0.95 | ~40.600 € |
| **C. Valenciana** | 26.822 € | ×0.91 | ~38.800 € |
| **Andalucía** | 26.090 € | ×0.88 | ~37.700 € |
| **Extremadura** | 23.194 € | ×0.78 | ~33.400 € |

### 3.6 Corrección Demográfica

El dataset de Kaggle proyectaba una población española en declive (~45M para 2025-2030). **Datos reales del INE**:

| Fecha | Población Real | Fuente |
|------|---------------|--------|
| Abril 2025 | 49.153.849 | INE Estadística Continua |
| Enero 2026 | 49.570.725 | INE (cifras oficiales) |
| Abril 2026 | 49.687.120 | INE (datos provisionales) |

**La población crece por inmigración** (colombiana, marroquí, venezolana). La proyección de declive del dataset Kaggle no se materializó.

### 3.7 Distribución del Dataset de Ofertas

| Métrica | Valor |
|---------|-------|
| Total ofertas analizadas | 247 |
| Roles Data | 238 (96%) |
| Roles IT/Software | 65 (26%) — hay solapamiento |
| Ofertas en Cataluña | 215 (87%) |
| Ofertas con salario real | **1 (0.4%)** |
| Ofertas sin dato salarial | 246 (99.6%) |

---

## 4. Problemas y Limitaciones

### 4.1 Problemas Técnicos Superados

1. **CSV mal formateado**: Comas dentro de campos de texto → parser personalizado
2. **Formato numérico europeo**: Comas como separadores decimales en demografía → normalización
3. **Archivos PC-Axis del INE (.px)**: Formato propietario no estándar → parser regex
4. **API INE 404**: La API JSON directa devolvía 404 → se usó el archivo .px directamente
5. **Guía Hays/Block&Capital**: Detrás de formulario → se usó Manfred + Ametic como fuentes alternativas

### 4.2 Limitaciones del Análisis

| Limitación | Impacto |
|-----------|---------|
| 87% de ofertas son de Cataluña | La muestra NO representa a España |
| Solo 1 salario real en 247 ofertas | Imposible validar estimaciones contra datos reales |
| PIB solo hasta 2016 (último disponible en Kaggle) | Desactualizado para 2024-2026 |
| INE no publica salarios tech por CCAA (muestra insuficiente) | Los multiplicadores regionales son para todos los sectores |
| Datos de ofertas web → sesgo hacia perfiles digitales | No representa el sector tech completo (incluye consultoras, startups) |

---

## 5. Conclusiones Finales

### En Inglés

1. **Tech sector commands a 44.7% salary premium** over Spain's national average.
2. **Three independent sources converge**: INE (42,742€), Manfred (~45,000€), Ametic (48,900€).
3. **Gender gap persists at 16%** in tech — unchanged since 2008.
4. **Madrid pays 19% above national average**, Extremadura 22% below.
5. **The Kaggle-only approach failed**: 1 real salary out of 248 offers made ML modeling impossible without synthetic data. The previous R²=0.82 was the model learning its own formula.
6. **Population is 49.57M and growing** (2026), contradicting the Kaggle dataset's decline projection.

### En Español

1. **El sector tech paga un 44.7% más** que la media nacional española.
2. **Tres fuentes independientes convergen**: INE (42.742€), Manfred (~45.000€), Ametic (48.900€).
3. **La brecha de género se mantiene en 16%** en tech — sin cambios desde 2008.
4. **Madrid paga un 19% sobre la media**, Extremadura un 22% por debajo.
5. **El enfoque solo con Kaggle falló**: 1 salario real de 248 ofertas hizo imposible el ML. El R²=0.82 era el modelo aprendiendo su propia fórmula.
6. **La población real es 49.57M y crece** (2026), contradiciendo la proyección de declive del dataset Kaggle.

---

## 6. Archivos Generados

| Archivo | Contenido |
|---------|-----------|
| `Spain_EDA_Integrated.ipynb` | Notebook principal con EDA + datos reales |
| `Spain_EDA_Integrated_executed.ipynb` | Versión ejecutada con outputs |
| `Pearsons_Four_Enhanced.ipynb` | Análisis de correlación de Pearson |
| `build_real_salary_pipeline.py` | Pipeline reutilizable con datos reales |
| `spain_tech_salaries_real.csv` | 247 ofertas enriquecidas con estimaciones reales |
| `ine_salaries_by_sector.csv` | 969 registros salariales del INE por sector, año y sexo |
| `spain_salaries_real_estimates.csv` | Resumen limpio de estimaciones |
| `INFORME_TECHSALARY_ES.md` | Este informe |
| `*.png` (13 archivos) | Visualizaciones generadas |

---

**Fin del informe.**
