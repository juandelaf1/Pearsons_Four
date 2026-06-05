"""
generate_plotly_viz.py — Interactive Plotly visualizations
Generates interactive HTML charts for the Pearson's Four project.
Replaces static Matplotlib/Seaborn with Plotly for hover, zoom, pan.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PLOTLY_DIR = BASE_DIR / 'screenshots' / 'plotly'
DATA_DIR = BASE_DIR / 'data'
os.makedirs(PLOTLY_DIR, exist_ok=True)


def load_data():
    path = DATA_DIR / 'linkedin_data_roles_procesed.csv'
    if not path.exists():
        print("LinkedIn data not found")
        return pd.DataFrame()

    df = pd.read_csv(path)

    exp_map = {
        0: 'Prácticas', 1: 'Junior', 2: 'Asociado',
        3: 'Mid-Senior', 4: 'Director', 5: 'Ejecutivo',
    }
    df['exp_label'] = df['experience_level_num'].map(exp_map).fillna('No especificado')

    print(f"Dataset: {len(df)} rows")
    return df


def estilo_pro(fig):
    fig.update_layout(
        width=950, height=600,
        template='plotly_white',
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(size=13),
    )
    return fig


def graph_1_violin(df):
    """Violin plot: salary distribution by experience (log scale)."""
    df_v = df.dropna(subset=['normalized_salary', 'exp_label']).copy()
    df_v = df_v[df_v['normalized_salary'] > 1000]

    fig = px.violin(
        df_v,
        y='normalized_salary',
        x='exp_label',
        box=True,
        points='all',
        color='exp_label',
        labels={
            'normalized_salary': 'Salario Normalizado (USD)',
            'exp_label': 'Nivel de Experiencia',
        },
        custom_data=['title', 'formatted_work_type', 'company_name'],
        title='<b>Distribución de Salarios por Experiencia</b><br><sub>Escala log + cuartiles + puntos individuales</sub>',
    )
    fig.update_yaxes(type='log', title='Salario (USD) — Escala Logarítmica')
    fig.update_traces(
        hovertemplate='<br>'.join([
            '<b>%{customdata[0]}</b>',
            'Empresa: %{customdata[2]}',
            'Salario: $%{y:,.0f}',
            'Jornada: %{customdata[1]}',
            '<extra></extra>',
        ])
    )
    fig.update_layout(showlegend=False)
    estilo_pro(fig)
    fig.write_html(PLOTLY_DIR / '01_violin_salarios.html')
    print("  [1/4] Violín salarial guardado")
    return fig


def graph_2_correlation_matrix(df):
    """Correlation matrix with diverging color scale."""
    cols = ['normalized_salary', 'experience_level_num', 'views', 'applies']
    corr = df[cols].dropna().corr()

    labels = {
        'normalized_salary': 'Salario (USD)',
        'experience_level_num': 'Experiencia',
        'views': 'Visualizaciones',
        'applies': 'Postulaciones',
    }
    corr = corr.rename(index=labels, columns=labels)

    fig = px.imshow(
        corr.values,
        x=corr.columns,
        y=corr.columns,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu',
        zmin=-1, zmax=1,
        title='<b>Matriz de Correlación de Variables</b>',
    )
    fig.update_traces(
        hovertemplate='<br>'.join([
            '<b>Correlación</b>',
            'Var 1: %{y}',
            'Var 2: %{x}',
            'Coeficiente: %{z:.3f}',
            '<extra></extra>',
        ])
    )
    estilo_pro(fig)
    fig.write_html(PLOTLY_DIR / '02_matriz_correlacion.html')
    print("  [2/4] Matriz de correlación guardada")
    return fig


def graph_3_bar(df):
    """Bar chart: average salary by experience."""
    df_agg = df.groupby('exp_label')['normalized_salary'].mean().reset_index()

    fig = px.bar(
        df_agg,
        x='exp_label',
        y='normalized_salary',
        text_auto='.3s',
        labels={
            'exp_label': 'Nivel de Experiencia',
            'normalized_salary': 'Salario Promedio (USD)',
        },
        color='normalized_salary',
        color_continuous_scale='Blues',
        title='<b>Salario Promedio por Nivel de Experiencia</b>',
    )
    fig.update_traces(
        hovertemplate='<br>'.join([
            '<b>%{x}</b>',
            'Salario promedio: $%{y:,.0f}',
            '<extra></extra>',
        ])
    )
    fig.update_layout(showlegend=False)
    estilo_pro(fig)
    fig.write_html(PLOTLY_DIR / '03_barras_salario_promedio.html')
    print("  [3/4] Barras salario promedio guardadas")
    return fig


def graph_4_scatter(df):
    """Scatter: salary vs experience colored by work type."""
    df_s = df.dropna(subset=['normalized_salary', 'exp_label']).copy()
    df_s = df_s[df_s['normalized_salary'] > 1000]

    fig = px.scatter(
        df_s,
        x='exp_label',
        y='normalized_salary',
        color='formatted_work_type',
        opacity=0.4,
        custom_data=['title', 'company_name'],
        labels={
            'normalized_salary': 'Salario Normalizado (USD)',
            'exp_label': 'Nivel de Experiencia',
            'formatted_work_type': 'Modalidad',
        },
        title='<b>Salario vs Nivel de Experiencia</b><br><sub>Color por modalidad — escala logarítmica</sub>',
    )
    fig.update_yaxes(type='log')
    fig.update_traces(
        marker=dict(size=6),
        hovertemplate='<br>'.join([
            '<b>%{customdata[0]}</b>',
            'Empresa: %{customdata[1]}',
            'Salario: $%{y:,.0f}',
            '<extra></extra>',
        ])
    )
    fig.update_layout(hovermode='closest')
    estilo_pro(fig)
    fig.write_html(PLOTLY_DIR / '04_scatter_salario_vs_experiencia.html')
    print("  [4/4] Scatter salario vs experiencia guardado")
    return fig


def graph_5_spain_salaries():
    """Spain salary comparison by role (if Spain data available)."""
    spain_path = DATA_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'
    if not spain_path.exists():
        print("  [5] Saltado: sin datos España")
        return

    df = pd.read_csv(spain_path, encoding='utf-8-sig')
    manfred = df[df['fuente'] == 'Manfred 2026'].copy()
    if manfred.empty:
        print("  [5] Saltado: sin datos Manfred")
        return

    data_roles = ['Data Engineer', 'Data Scientist', 'Data Analyst', 'MLOps Engineer', 'Data Architect']
    plot_data = manfred[manfred['rol'].isin(data_roles)].copy()

    fig = go.Figure()
    for rol in data_roles:
        subset = plot_data[plot_data['rol'] == rol]
        if subset.empty:
            continue
        ranges = []
        for _, row in subset.iterrows():
            sal = row['rango_salarial']
            nums = [int(s) for s in ''.join(c if c.isdigit() else ' ' for c in sal).split() if s]
            if nums:
                ranges.append(max(nums))
        if ranges:
            exp_labels = subset['experiencia'].values if len(subset) == len(ranges) else [f'Lvl{j}' for j in range(len(ranges))]
            fig.add_trace(go.Bar(
                name=rol,
                x=list(exp_labels),
                y=ranges,
                text=[f'{r}K' for r in ranges],
                textposition='outside',
            ))

    fig.update_layout(
        title='<b>Salarios Tech en España por Rol (Manfred 2026)</b>',
        xaxis_title='Nivel de Experiencia',
        yaxis_title='Salario (K EUR)',
        barmode='group',
        template='plotly_white',
        width=1000, height=600,
    )
    fig.write_html(PLOTLY_DIR / '05_spain_salaries.html')
    print("  [5/5] Salarios España guardados")
    return fig


def main():
    print("=" * 60)
    print("GENERADOR DE VISUALIZACIONES PLOTLY - PEARSON'S FOUR")
    print("=" * 60)

    df = load_data()
    if df.empty:
        return

    print(f"\nGenerando {4} gráficos interactivos...\n")
    graph_1_violin(df)
    graph_2_correlation_matrix(df)
    graph_3_bar(df)
    graph_4_scatter(df)
    graph_5_spain_salaries()

    print(f"\n{'='*60}")
    print(f"Listo. HTML interactivos en: {PLOTLY_DIR}")
    files = list(PLOTLY_DIR.glob('*.html'))
    for f in sorted(files):
        print(f"  OK {f.name} ({f.stat().st_size / 1e6:.1f} MB)")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
