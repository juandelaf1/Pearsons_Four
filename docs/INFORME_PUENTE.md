# INFORME PUENTE — Pearson's Four ↔ Spain EDA
## Estrategia B: Proyectos separados + tabla de correspondencia

---

## 1. Propósito de este informe

Pearson's Four analiza **LinkedIn (global)** + **Stack Overflow** para patrones estructurales del mercado Data.
Spain_EDA_Integrated analiza **INE + fuentes españolas** para el mercado local.

Este informe tiende el puente entre ambos sin mezclar metodologías.

---

## 2. Tabla de Correspondencia

| Métrica | Pearson's Four (LinkedIn Global) | Spain EDA (INE España) | ¿Correspondencia? |
|---------|----------------------------------|------------------------|-------------------|
| Salario medio Data | $96,795 USD (~89.000 €) | 42.742 € (Sector J INE) | Difieren por mercado y moneda. Factor ~0.48 |
| Remote Premium | +45.1% (USA) | +15-20% estimado (España) | Patrón similar, magnitud menor en ES |
| Senior vs Junior ratio | 4.2x (Director vs Entry) | ~2.5x (Manfred 2026) | Misma dirección, menor desigualdad en ES |
| Top industrias | IT Services, Software, Finance | IT Services, Consultoría, Banca | Matching alto |
| Skills más demandadas | Python + SQL (LinkedIn) | Python + SQL (Manfred) | Coincidencia total |
| Sesgo principal | MNAR (juniors ocultan salario) | Brecha género 16% en tech | Sesgos distintos pero complementarios |

---

## 3. Los 5 patrones que SÍ se mantienen

Aunque los salarios absolutos cambian, estos patrones estructurales se repiten:

1. **La experiencia es el factor #1** — Pearson r ~0.43 en LinkedIn, misma progresión en datos INE
2. **Remote premium existe** — +45% en USA, estimado +15-20% en España por menor arbitraje
3. **Python + SQL dominan** — Top skills en ambas fuentes
4. **IT Services lidera contratación** — Mismo sector #1 en USA y España
5. **Sesgo de selección** — Datos no representativos de toda la población (LinkedIn = USA, Kaggle ES sesgado a Cataluña)

---

## 4. Correspondencia salarial: cómo llevar los hallazgos globales a España

```
LinkedIn Global (data roles): $96,795
               │
               ▼ Ajuste por tipo de cambio (1 USD ≈ 0.92 EUR): ~89.000 €
               │
               ▼ Ajuste por mercado (EE.UU. paga más): factor ~0.50-0.55x
               │
               ▼ Rango estimado para España: 42.000 - 48.000 €
               │
               ▼ Contraste con INE Sector J (2024): 42.742 € ✓
               │
               ▼ Contraste con Ametic/Expansión (2025): 48.900 € ✓
               │
               ▼ Conclusión: El factor de ajuste EE.UU. → España es ~0.48x
```

**Regla práctica:** Para estimar un salario español desde los datos de LinkedIn, multiplicar por ~0.48 y convertir a euros.

---

## 5. Datos complementarios

| Dato | Pearson's Four | Spain EDA | Quién debe usarlo |
|------|---------------|-----------|-------------------|
| Análisis MNAR | ✅ Sí | ❌ No | Vanessa (ética) |
| Remote Premium | ✅ +45.1% USA | ✅ +15-20% ES | Juan (recomendaciones) |
| Salarios por experiencia | ✅ LinkedIn global | ✅ Manfred España | Isabela + Anas |
| Brecha de género | ❌ No disponible | ✅ 16% en tech | Vanessa (sesgos adicionales) |
| Salarios por CCAA | ❌ No aplica | ✅ Tabla por región | Juan (contexto local) |
| Correlación Pearson | ✅ r = 0.43 | ✅ Similar (Pearsons_Four_Enhanced) | Isabela |

---

## 6. Para la defensa: frase puente recomendada

> "Nuestro análisis principal usa LinkedIn y Stack Overflow por ser datasets robustos y ampliamente documentados. Para contextualizar los hallazgos en el mercado español, hemos contrastado nuestros resultados con fuentes oficiales como el INE y guías salariales locales (Manfred, Ametic). Aunque los salarios absolutos en EE.UU. son más altos, los **patrones estructurales** —la prima por experiencia, el valor del trabajo remoto, la demanda de Python/SQL— se mantienen y son aplicables al ecosistema tech español."
