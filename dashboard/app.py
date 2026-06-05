import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))

st.set_page_config(
    page_title="Pearson's Four — Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Pearsons Four — EDA Data Science Job Salaries")
st.markdown("""
Exploratory Data Analysis: LinkedIn job postings + Stack Overflow bias analysis + Spain market study.
""")

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / 'data'


@st.cache_data
def load_linkedin():
    path = DATA_DIR / 'linkedin_data_roles_procesed.csv'
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data
def load_spain():
    path = DATA_DIR / 'espana' / 'spain_tech_salaries_scraped.csv'
    if path.exists():
        return pd.read_csv(path, encoding='utf-8-sig')
    return pd.DataFrame()


@st.cache_data
def load_ine():
    path = DATA_DIR / 'espana' / 'spain_tech_salaries_real.csv'
    if path.exists():
        return pd.read_csv(path, encoding='utf-8-sig')
    return pd.DataFrame()


df_linkedin = load_linkedin()
df_spain = load_spain()
df_ine = load_ine()

col1, col2, col3 = st.columns(3)
col1.metric("LinkedIn Data Roles", f"{len(df_linkedin):,}" if not df_linkedin.empty else "N/A")
col2.metric("Spain Salary Records", f"{len(df_spain):,}" if not df_spain.empty else "N/A")
col3.metric("Spain INE Estimates", f"{len(df_ine):,}" if not df_ine.empty else "N/A")

tab1, tab2, tab3, tab4 = st.tabs([
    "💰 LinkedIn Salaries", "🌍 Spain Market", "📈 Correlations", "⚠️ Bias Analysis"
])

with tab1:
    if not df_linkedin.empty:
        st.subheader("Salary Distribution by Experience Level")

        exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
        fig = px.box(
            df_linkedin,
            x='formatted_experience_level',
            y='normalized_salary',
            category_orders={'formatted_experience_level': exp_order},
            color='formatted_experience_level',
            title='Salary Distribution by Experience Level (LinkedIn)',
            labels={'formatted_experience_level': 'Experience Level', 'normalized_salary': 'Salary (USD)'},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top 10 Most Demanded Roles")
        top_roles = df_linkedin['title'].value_counts().head(10)
        fig2 = px.bar(
            x=top_roles.values, y=top_roles.index, orientation='h',
            title='Top 10 Data Roles',
            labels={'x': 'Number of Postings', 'y': 'Role'},
            color=top_roles.values,
            color_continuous_scale='viridis',
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Salary Statistics")
        sal = df_linkedin['normalized_salary'].dropna()
        stats = pd.DataFrame({
            'Metric': ['Mean', 'Median', 'Std Dev', 'Q1', 'Q3', 'Min', 'Max'],
            'Value (USD)': [
                f"${sal.mean():,.0f}",
                f"${sal.median():,.0f}",
                f"${sal.std():,.0f}",
                f"${sal.quantile(0.25):,.0f}",
                f"${sal.quantile(0.75):,.0f}",
                f"${sal.min():,.0f}",
                f"${sal.max():,.0f}",
            ],
        })
        st.dataframe(stats, hide_index=True, use_container_width=True)

with tab2:
    if not df_spain.empty:
        st.subheader("Spain Tech Salaries by Source")

        fig3 = px.box(
            df_spain,
            x='fuente',
            y='rango_salarial',
            color='fuente',
            title='Salary Distribution by Source (Spain)',
            labels={'fuente': 'Source', 'rango_salarial': 'Salary Range'},
        )
        st.plotly_chart(fig3, use_container_width=True)

        if not df_ine.empty:
            st.subheader("Regional Salary Estimates (INE)")

            if 'comunidad_autonoma' in df_ine.columns and 'salario_bruto_anual_est' in df_ine.columns:
                region_data = df_ine.groupby('comunidad_autonoma')['salario_bruto_anual_est'].mean().round(0).sort_values(ascending=False)
                fig4 = px.bar(
                    x=region_data.values, y=region_data.index, orientation='h',
                    title='Estimated Salary by Region (Spain)',
                    labels={'x': 'Avg Annual Salary (EUR)', 'y': 'Region'},
                    color=region_data.values,
                    color_continuous_scale='blues',
                )
                st.plotly_chart(fig4, use_container_width=True)

        st.subheader("Sources")
        src_counts = df_spain['fuente'].value_counts()
        st.dataframe(
            src_counts.reset_index().rename(columns={'index': 'Source', 'fuente': 'Records'}),
            hide_index=True, use_container_width=True,
        )

with tab3:
    st.subheader("Key Correlations (LinkedIn Data Roles)")
    st.markdown("""
    | Variable Pair | Pearson r | Interpretation |
    |--------------|-----------|----------------|
    | Experience → Salary | **0.49** | Moderate-strong positive. Main finding. |
    | Remote → Salary | **0.04** | Near zero. No relationship for Data Roles. |
    | Views → Applies | **0.91** | Strong positive. More views = more apps. |
    | Views → Salary | **-0.15** | Very weak negative. Traffic ≠ salary. |
    """)

    st.subheader("Experience vs Salary (Median)")
    if not df_linkedin.empty:
        exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
        exp_medians = df_linkedin.groupby('formatted_experience_level')['normalized_salary'].median()
        exp_medians = exp_medians.reindex(exp_order).dropna()

        fig5 = go.Figure()
        fig5.add_trace(go.Scatter(
            x=list(range(len(exp_medians))),
            y=exp_medians.values,
            mode='lines+markers+text',
            text=[f"${v:,.0f}" for v in exp_medians.values],
            textposition='top center',
            line=dict(color='royalblue', width=3),
            marker=dict(size=12),
        ))
        fig5.update_layout(
            title='Salary Progression by Experience',
            xaxis=dict(tickvals=list(range(len(exp_medians))), ticktext=list(exp_medians.index)),
            yaxis_title='Median Salary (USD)',
            yaxis=dict(range=[0, exp_medians.max() * 1.25]),
        )
        st.plotly_chart(fig5, use_container_width=True)

with tab4:
    st.subheader("Bias Analysis — Stack Overflow + LinkedIn")
    st.markdown("""
    | Bias Type | Finding |
    |-----------|---------|
    | **Geographic** | US/UK overrepresented; 0 postings from Spain in LinkedIn data |
    | **Salary MNAR** | 70.87% missing salaries; 47.33% juniors hide salary vs 23.86% seniors |
    | **Selection Bias** | 83.81% Senior/Experienced vs 16.19% Junior/Early-Career |
    | **Skills sparsity** | 98.03% missing `skills_desc` column |
    """)

    st.subheader("Conditional Probability (Stack Overflow)")
    st.markdown("""
    - P(High Salary | Senior/Experienced) = **53.42%**
    - P(High Salary | Junior/Early-Career) = **22.57%**
    """)

    st.subheader("Cross-Dataset Comparison")
    st.markdown("""
    | Metric | Stack Overflow | LinkedIn |
    |--------|---------------|----------|
    | Median salary | $85,000 | **$135,588** |
    | Perspective | Developer self-reported | Corporate real offers |

    **Key insight:** LinkedIn offers reflect real market rates (+59% median vs SO).
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 Project")
st.sidebar.markdown("[📄 README](README.md)")
st.sidebar.markdown("[📓 Notebooks](notebooks/)")
st.sidebar.markdown("[📊 Screenshots](screenshots/)")
st.sidebar.markdown("[🐙 GitHub](https://github.com/juandelaf1/Pearsons_Four)")
