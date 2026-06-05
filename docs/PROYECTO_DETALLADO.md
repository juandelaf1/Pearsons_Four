# Pearson's Four - Proyecto DataTalent Solutions S.L.

Este repositorio documenta el desarrollo completo del proyecto **Pearson's Four**, realizado como parte del módulo de Análisis y Visualización de Datos.

## 1. Resumen Ejecutivo
El proyecto proporciona a *DataTalent Solutions S.L.* evidencia empírica sobre el mercado laboral de perfiles técnicos (Data Science). Analizamos dos fuentes de datos para identificar factores salariales, habilidades demandadas y sesgos del mercado.

## 2. Equipo y Responsabilidades
| Rol | Integrante | GitHub |
| :--- | :--- | :--- |
| **Product Owner & Data Wrangler** | Juan | [@juandelaf1](https://github.com/juandelaf1) |
| **Análisis Estadístico** | Isabela | [@Isabela-Tellez](https://github.com/Isabela-Tellez) |
| **Visualización (Storyteller)** | Anas | [@Anas28](https://github.com/Anas28) |
| **Consultora de Estrategia y Ética** | Vanessa | [@garciaguadalupevanessa-bit](https://github.com/garciaguadalupevanessa-bit) |

---

## 3. Informe Detallado: Proceso End-to-End

### Fase 1: Ingeniería y Limpieza (Juan)
- **Desafío:** Dataset de 123,849 registros con >70% de nulos en salarios.
- **Acción:** Implementación del *"Pearson's Pipeline"*.
- **Decisión:** Filtrado mediante Rango Intercuartílico (IQR) para eliminar valores extremos.
- **Resultado:** Obtención de una muestra de alta fidelidad con **607 registros** clave para el análisis de roles.

### Fase 2: Análisis Estadístico (Isabela)
- **Desafío:** Distribución asimétrica positiva en salarios.
- **Acción:** Uso de la **mediana** ($135,588) como métrica principal sobre la media.
- **Decisión:** Aplicación de test ANOVA.
- **Resultado:** Confirmación estadística (p < 0.0001) de que el nivel de experiencia es determinante para el salario.

### Fase 3: Visualización (Anas)
- **Acción:** Mapeo de la relación entre visualizaciones y aplicaciones.
- **Resultado:** Correlación moderada (r=0.62). Se concluye que el tráfico no garantiza conversión, destacando la importancia de la calidad en la descripción de las ofertas.

### Fase 4: Ética y Sesgos (Vanessa)
- **Acción:** Análisis MNAR (*Missing Not At Random*).
- **Resultado:** Identificación de sesgo en el ocultamiento de salarios (47% de juniors ocultan salario vs 23% de seniors).
- **Comparativa:** LinkedIn (ofertas reales) vs Stack Overflow (auto-reportadas). El mercado paga ~59% más que lo que los perfiles reportan en encuestas.

---

## 4. Metodología de Trabajo
- **GitHub Flow:** Uso de *feature branches*, *Pull Requests* y revisiones de código.
- **Colaboración:** *Pair programming* rotativo y uso de Google Colab para consistencia de datos.
- **Gestión:** Daily standups ágiles.

---

## 5. Hallazgos Estratégicos
- **Python:** Aumenta la probabilidad de salario alto en ~13%.
- **Experiencia:** Es el predictor salarial más fuerte (correlación 0.43).
- **Acción Estratégica:** Las tarifas de servicios y programas formativos deben basarse en datos corporativos (LinkedIn) y no en encuestas comunitarias (Stack Overflow).
