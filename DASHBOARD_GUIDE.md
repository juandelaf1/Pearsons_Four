# DataScope — Dashboard

## Opción 1: Docker (recomendado, más fácil)

```bash
# Solo necesitas Docker instalado
docker pull juandelaf/datascope
docker run -p 8501:8501 juandelaf/datascope
```

O con docker-compose:

```bash
docker compose up
```

Abrir http://localhost:8501

## Opción 2: Local con Python

```bash
# Requisitos: Python 3.11+, uv o pip
git clone https://github.com/juandelaf1/DataScope.git
cd DataScope

# Instalar
uv sync

# Ejecutar
uv run streamlit run dashboard/app.py
```

## Estructura

```
dashboard/
├── app.py                    # Página principal — KPIs + Mapa mundial
├── utils.py                  # Carga de datos centralizada
├── style.py                  # CSS personalizado (tema oscuro)
└── pages/
    ├── 01_🌍_Global.py       # Análisis global (mapa, roles, seniority)
    ├── 02_🇪🇸_Spain.py        # Análisis España multi-fuente
    ├── 03_📊_Analytics.py    # DuckDB Analytics (5 queries)
    └── 04_⚠️_Bias.py          # Bias & Data Quality
```

## Navegación

Las páginas aparecen automáticamente en la barra lateral. Usa los filtros en la sidebar para refinar los datos.

## Enlaces

- GitHub: https://github.com/juandelaf1/DataScope
- DockerHub: https://hub.docker.com/r/juandelaf/datascope
- Kaggle Dataset: https://www.kaggle.com/datasets/juandelaf/datascope-salary-analytics
