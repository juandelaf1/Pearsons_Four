"""
generate_visualizations.py — Mejorado
Genera graficos del proyecto Pearson's Four usando datos locales.
Incluye visualizaciones del dataset LinkedIn + datos salariales de Espana.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys, json
from pathlib import Path

sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)

BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = BASE_DIR / 'screenshots'
DATA_DIR = BASE_DIR / 'data'
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def load_linkedin_data():
    """Carga datos locales de LinkedIn si existen, si no intenta desde kagglehub."""
    csv_path = DATA_DIR / 'linkedin_data_roles_procesed.csv'
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"  Cargado local: {len(df)} registros")
        return df

    try:
        import kagglehub
        path = kagglehub.dataset_download('arshkon/linkedin-job-postings')
        df = pd.read_csv(os.path.join(path, 'postings.csv'))
        print(f"  Cargado Kaggle: {len(df)} registros")

        # Filter data roles
        data_kw = 'data scientist|data engineer|data analyst|machine learning|ml engineer|ai engineer|business intelligence|data architect|analytics|data manager'
        df_data = df[df['title'].str.contains(data_kw, case=False, na=False)].copy()
        df_data['title'] = df_data['title'].str.lower().str.strip()
        df_data['location'] = df_data['location'].str.lower().str.strip()
        exp_map = {'internship': 0, 'entry level': 1, 'associate': 2, 'mid-senior level': 3, 'director': 4, 'executive': 5}
        df_data['experience_level_num'] = df_data['formatted_experience_level'].str.lower().map(exp_map)
        df_data = df_data[(df_data['normalized_salary'] >= 1000) & (df_data['normalized_salary'] <= 2000000)].copy()
        df_data['is_remote'] = df_data['remote_allowed'].fillna(0).astype(bool)
        print(f"  Filtrado: {len(df_data)} data roles con salario valido")
        return df_data
    except Exception as e:
        print(f"  No se pudo cargar LinkedIn: {e}")
        return pd.DataFrame()


def load_spain_data():
    """Carga los datos salariales de Espana scraped."""
    csv_path = BASE_DIR / 'data' / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not csv_path.exists():
        print("  Datos de Espana no encontrados. Ejecuta scrape_spain_salaries.py primero.")
        return pd.DataFrame()

    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"  Cargados {len(df)} registros de Espana")
    return df


def graph_1_boxplot_linkedin(df):
    plt.figure(figsize=(12, 6))
    exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
    sns.boxplot(data=df, x='formatted_experience_level', y='normalized_salary',
                order=exp_order, palette='Set2')
    plt.title('Distribucion Salarial por Nivel de Experiencia (LinkedIn)', fontsize=14, fontweight='bold')
    plt.xlabel('Nivel de Experiencia')
    plt.ylabel('Salario Normalizado Anual (USD)')
    plt.ylim(0, 500000)
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_boxplot_experience.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [1/8] Boxplot experiencia guardado")


def graph_2_histogram_kde(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='normalized_salary', kde=True, bins=40, color='teal')
    plt.title('Distribucion de Salarios Tech con KDE (LinkedIn)', fontsize=14, fontweight='bold')
    plt.xlabel('Salario Normalizado Anual (USD)')
    plt.ylabel('Numero de Ofertas')
    plt.xlim(0, 400000)
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_histogram_kde.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [2/8] Histograma KDE guardado")


def graph_3_salary_spread(df):
    plt.figure(figsize=(10, 6))
    sal = df['normalized_salary'].dropna()
    plt.subplot(1, 2, 1)
    plt.boxplot(sal, vert=False)
    plt.title('Distribucion (Boxplot)')
    plt.xlabel('Salario (USD)')
    plt.subplot(1, 2, 2)
    plt.hist(sal, bins=30, color='teal', edgecolor='white')
    plt.title('Distribucion (Histograma)')
    plt.xlabel('Salario (USD)')
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_salary_spread.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [3/8] Salary spread guardado")


def graph_4_top_roles(df):
    plt.figure(figsize=(10, 6))
    top_titles = df['title'].value_counts().head(10)
    sns.barplot(x=top_titles.values, y=top_titles.index, palette='viridis')
    plt.title('Top 10 Roles Tech mas Demandados (LinkedIn)', fontsize=14, fontweight='bold')
    plt.xlabel('Numero de Ofertas')
    plt.ylabel('Titulo del Puesto')
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_top_roles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [4/8] Top roles guardado")


def graph_5_views_vs_applies(df):
    from scipy.stats import pearsonr
    r, p = pearsonr(df['views'], df['applies'])
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='views', y='applies', alpha=0.6, color='coral')
    sns.regplot(data=df, x='views', y='applies', scatter=False, color='darkred')
    plt.title(f'Correlacion: Visualizaciones vs Aplicaciones (r = {r:.2f})', fontsize=14, fontweight='bold')
    plt.xlabel('Visualizaciones')
    plt.ylabel('Aplicaciones')
    plt.xlim(0, 1000)
    plt.ylim(0, 200)
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_views_vs_applies.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [5/8] Views vs Applies guardado")


def graph_6_salary_progression(df):
    exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
    exp_medians = df.groupby('formatted_experience_level')['normalized_salary'].median()
    exp_medians = exp_medians.reindex(exp_order).dropna()
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(exp_medians)), exp_medians.values, 'bo-', linewidth=2.5, markersize=10)
    for i, v in enumerate(exp_medians.values):
        plt.text(i, v + 5000, f'${v:,.0f}', ha='center', fontsize=11, fontweight='bold')
    plt.xticks(range(len(exp_medians)), exp_medians.index, fontsize=11)
    plt.ylabel('Salario Mediano (USD)')
    plt.title('Progresion Salarial por Experiencia (LinkedIn)', fontsize=14, fontweight='bold')
    plt.ylim(0, exp_medians.max() * 1.2)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_salary_progression.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [6/8] Progresion salarial guardado")


def graph_7_remote_premium(df):
    # Handle both column name variants
    col_remote = 'is_remote' if 'is_remote' in df.columns else 'remote_allowed'
    if col_remote not in df.columns:
        print("  [7/8] Saltado: sin columna remote")
        return

    # Convert to bool if needed
    if df[col_remote].dtype not in (bool, np.bool_):
        df['_remote_bool'] = df[col_remote].fillna(0).astype(bool)
        group_col = '_remote_bool'
    else:
        group_col = col_remote

    remote_comp = df.groupby(group_col)['normalized_salary'].median()
    plt.figure(figsize=(8, 6))
    vals = [remote_comp.get(False, 0), remote_comp.get(True, 0)]
    colors = ['#e74c3c', '#2ecc71']
    plt.bar(['Presencial', 'Remoto'], vals, color=colors, width=0.5)
    for i, v in enumerate(vals):
        plt.text(i, v + 2000, f'${v:,.0f}', ha='center', fontsize=12, fontweight='bold')
    premium = ((vals[1] / max(vals[0], 1)) - 1) * 100
    plt.title(f'Prima por Trabajo Remoto: +{premium:.1f}%', fontsize=14, fontweight='bold')
    plt.ylabel('Salario Mediano (USD)')
    plt.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'linkedin_remote_premium.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [7/8] Remote premium guardado (+{premium:.1f}%)")


def graph_8_spain_salaries(df_es):
    """NUEVO: Grafico comparativo de salarios tech en Espana por fuente y rol."""
    if df_es.empty:
        print("  [8/8] Saltado (sin datos Espana)")
        return

    # Manfred data: salaries by role
    manfred = df_es[df_es['fuente'] == 'Manfred 2026'].copy()
    if manfred.empty:
        print("  [8/8] Saltado (sin datos Manfred)")
        return

    # Focus on data roles with full experience
    data_roles = ['Data Engineer', 'Data Scientist', 'Data Analyst', 'MLOps Engineer', 'Data Architect']
    plot_data = manfred[manfred['rol'].isin(data_roles)].copy()

    plt.figure(figsize=(14, 8))
    for i, rol in enumerate(data_roles):
        subset = plot_data[plot_data['rol'] == rol]
        if subset.empty:
            continue
        # Parse salary from text (e.g., "$25-35K" -> use max value)
        ranges = []
        for _, row in subset.iterrows():
            sal = row['rango_salarial']
            nums = [int(s) for s in ''.join(c if c.isdigit() else ' ' for c in sal).split() if s]
            if nums:
                ranges.append(max(nums))

        if ranges:
            plt.subplot(2, 3, i + 1)
            exp_labels = subset['experiencia'].values if len(subset) == len(ranges) else [f'Lvl{j}' for j in range(len(ranges))]
            colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(ranges)))
            bars = plt.barh(range(len(ranges)), ranges, color=colors)
            for j, (b, r) in enumerate(zip(bars, ranges)):
                plt.text(b.get_width() + 1, b.get_y() + b.get_height() / 2,
                         f'{r}K', va='center', fontsize=9)
            if len(subset) == len(ranges):
                plt.yticks(range(len(ranges)), [e[:10] for e in exp_labels], fontsize=8)
            plt.title(rol, fontsize=11, fontweight='bold')
            plt.xlabel('Salario (K EUR)')

    # Add INE reference line
    ine_sector_j = df_es[df_es['fuente'] == 'INE']
    ine_2024 = ine_sector_j[ine_sector_j['experiencia'] == '2024']
    ine_ambos = ine_2024[ine_2024['rol'].str.contains('Ambos sexos', na=False)]
    ine_val = None
    if not ine_ambos.empty:
        sal_str = ine_ambos.iloc[0]['rango_salarial']
        ine_val = int(float(sal_str.replace(' EUR', '').replace(',', '')))

    plt.suptitle('Salarios Tech en Espana por Rol y Experiencia (Manfred 2026 + INE)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(SCREENSHOTS_DIR / 'espana_salarios_por_rol.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  [8/8] Grafico salarios Espana guardado")


def main():
    print("=" * 60)
    print("GENERADOR DE VISUALIZACIONES - PEARSON'S FOUR")
    print("=" * 60)

    print("\n--- Cargando datos LinkedIn ---")
    df = load_linkedin_data()

    print("\n--- Cargando datos Espana ---")
    df_es = load_spain_data()

    if df.empty:
        print("\n⚠ Sin datos LinkedIn. Generando solo graficos de Espana...")
        graph_8_spain_salaries(df_es)
        return

    print(f"\n--- Generando {8 if not df_es.empty else 7} graficos ---\n")
    graph_1_boxplot_linkedin(df)
    graph_2_histogram_kde(df)
    graph_3_salary_spread(df)
    graph_4_top_roles(df)
    graph_5_views_vs_applies(df)
    graph_6_salary_progression(df)
    graph_7_remote_premium(df)
    graph_8_spain_salaries(df_es)

    print(f"\n{'='*60}")
    print(f"Listo. Graficos en: {SCREENSHOTS_DIR}")
    files = list(SCREENSHOTS_DIR.glob('*.png'))
    print(f"Archivos: {len(files)} PNG")
    for f in sorted(files):
        print(f"  - {f.name}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
