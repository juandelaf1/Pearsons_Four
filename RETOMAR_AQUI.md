# Retomar aquí — sesión 02/06/2026

## Estado actual

### Hecho ✓
- Merge completado de 3 proyectos → `Pearsons_Four/`
- Push a `github.com/juandelaf1/Pearsons_Four` (force push, ya actualizado)
- Eliminadas carpetas locales: `Pearsons_Four_Integrated_ES/`, `portfolio_notebooks/`
- Repo del grupo clonado local en `C:\Users\JUAN\Desktop\Proyectos\Pearsons_Four_grupo`

### Estructura actual de Pearsons_Four/
```
├── README.md
├── .gitignore
├── data/
│   ├── linkedin_data_roles_procesed.csv
│   └── espana/              ← INE salaries, tech salaries
├── notebooks/
│   ├── Pearsons_Four_EDA_Linkedin.ipynb
│   ├── Pearsons_Four_EDA_Enhanced.ipynb
│   ├── VGGPearsonsFour.ipynb
│   └── espana/              ← Spain EDA + enhanced correlations
├── screenshots/
│   ├── linkedin_*.png       ← 12 gráficas LinkedIn
│   └── espana/              ← 18 gráficas España
├── slides/
│   ├── presentacion_pearsons_four.pptx
│   └── extras/              ← PPTs grandes (referencia)
├── scripts/
│   ├── generate_visualizations.py
│   ├── verify_all_metrics.py
│   ├── verify_salaries.py
│   └── build_real_salary_pipeline.py
└── docs/
    ├── GUIDE.md
    ├── PROMPT_DEFINITIVO_SLIDES_Y_SPEECH.md
    ├── GUION_DEFENSA_COMPLETO.md
    ├── GUIA_METRICAS_Y_CAMBIOS.md
    ├── INFORME_PUENTE.md
    ├── REPORTE_PEARSONS_FOUR_PARA_NOTEBOOK_LM.md
    └── informes/             ← evaluación, internacional, techsalary ES
```

## Pendiente / Próximos pasos

### 1. Revisar repo del grupo
Ruta: `C:\Users\JUAN\Desktop\Proyectos\Pearsons_Four_grupo`
- Ver qué commits nuevos metió Anasfady (PROYECTO_DETALLADO.md, patches)
- Ver qué screenshots añadieron (heatmap_download.png, salary_spread (3).png)
- Decidir si mergear esos archivos a nuestro repo personal

### 2. Evaluar si añadir Spain study al repo grupal
Posible estructura en Anasfady/Pearsons_Four:
```
notebooks/espana/           ← Spain EDA notebooks
data/espana/                ← CSVs de INE + tech salaries
screenshots/espana/         ← gráficas
```
**⚠️ Problema detectado:** el Spain EDA tiene datos antiguos de Kaggle, algunos solo de Cataluña, y mezcla fuentes en un mismo notebook. Habría que limpiar/revisar antes de subirlo al repo del grupo.

### 3. Si se decide agregar al repo grupal
- Hacer PR desde `juandelaf1/Pearsons_Four` → `Anasfady/Pearsons_Four`
- O agregar remote `anasfady` y pushear rama

### 4. Entrega mañana
- Revisar que notebooks ejecuten limpios
- Confirmar métricas corregidas (ver scripts/verify_all_metrics.py)
- Slides de Isabella

## Comandos útiles

```powershell
# Ver diferencias entre tu repo y el del grupo
cd C:\Users\JUAN\Desktop\Proyectos\Pearsons_Four
git diff --stat anasfady/main..main

# Actualizar clone del grupo
cd C:\Users\JUAN\Desktop\Proyectos\Pearsons_Four_grupo
git pull origin main

# Pushear a tu repo personal
cd C:\Users\JUAN\Desktop\Proyectos\Pearsons_Four
git push origin main
```
