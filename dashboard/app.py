import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_global, load_spain, load_linkedin, load_ppp
from style import apply_custom_css

st.set_page_config(
    page_title="DataScope — Multi-Source Salary Analytics",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

df_global = load_global()
df_spain = load_spain()
df_linkedin = load_linkedin()
df_ppp = load_ppp()

st.markdown('<div class="section-header">📡 DataScope — Multi-Source Salary Analytics</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<h4>Executive Summary</h4>
<p>
<strong>5,370</strong> unified salary records across <strong>50 countries</strong>,
integrating LinkedIn Job Postings, Kaggle DS Salaries, and Spain multi-source
(Manfred 2026, Glassdoor ES, Kaggle ES). DuckDB analytics engine with
Eurostat PPP-adjusted comparisons.
</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total = len(df_global) if not df_global.empty else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Records</div>
        <div class="kpi-value">{total:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    countries = df_global['country_name'].nunique() if not df_global.empty else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Countries</div>
        <div class="kpi-value">{countries}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    median_global = df_global['salary_usd'].median() if not df_global.empty else 0
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Global Median Salary</div>
        <div class="kpi-value">${median_global:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if not df_spain.empty:
        median_spain_eur = df_spain['salary_eur'].median()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Spain Median (EUR)</div>
            <div class="kpi-value">€{median_spain_eur:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Spain Median (EUR)</div>
            <div class="kpi-value">N/A</div>
        </div>
        """, unsafe_allow_html=True)

with col5:
    if not df_linkedin.empty:
        median_linkedin = df_linkedin['normalized_salary'].median()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">LinkedIn Median (USD)</div>
            <div class="kpi-value">${median_linkedin:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">LinkedIn Median (USD)</div>
            <div class="kpi-value">N/A</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="section-header">🌍 Global Salary Map</div>', unsafe_allow_html=True)

    if not df_global.empty:
        country_medians = (
            df_global.groupby('country_name')['salary_usd']
            .median()
            .reset_index()
            .dropna()
        )

        fig_map = px.choropleth(
            country_medians,
            locations='country_name',
            locationmode='country names',
            color='salary_usd',
            color_continuous_scale='plasma',
            title='Median Salary by Country (USD)',
            labels={'salary_usd': 'Median Salary (USD)'},
            range_color=[country_medians['salary_usd'].quantile(0.05),
                         country_medians['salary_usd'].quantile(0.95)],
        )
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor='rgba(255,255,255,0.1)',
                projection_type='equirectangular',
                bgcolor='rgba(0,0,0,0)',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            margin=dict(l=0, r=0, t=40, b=0),
            height=400,
        )
        fig_map.update_coloraxes(colorbar_orientation='h', colorbar_y=-0.15)
        st.plotly_chart(fig_map, width='stretch')

with col_right:
    st.markdown('<div class="section-header">📊 Dataset Composition</div>', unsafe_allow_html=True)

    if not df_global.empty:
        src_counts = df_global['dataset'].value_counts().reset_index()
        src_counts.columns = ['Dataset', 'Records']

        fig_pie = px.pie(
            src_counts,
            values='Records',
            names='Dataset',
            title='Records by Source',
            color_discrete_sequence=px.colors.qualitative.Prism,
            hole=0.4,
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            margin=dict(l=0, r=0, t=40, b=0),
            height=300,
            showlegend=True,
            legend=dict(orientation='h', y=-0.15, font=dict(size=10)),
        )
        fig_pie.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig_pie, width='stretch')

    if not df_ppp.empty:
        st.markdown(f"""
        <div class="kpi-card" style="margin-top: 0.5rem; padding: 1rem;">
            <div class="kpi-label">Eurostat PPP Coverage</div>
            <div class="kpi-value" style="font-size:1.5rem;">{df_ppp['country_name'].nunique()} countries</div>
            <div class="kpi-delta positive">1960–2025 GDP + population data</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown('<div class="section-header">📈 Key Correlations</div>', unsafe_allow_html=True)

corr_cols = st.columns(4)
corr_data = [
    ("Experience → Salary", "r = 0.49", "Moderate-strong positive", "positive"),
    ("Remote → Salary", "r = 0.04", "Near zero. No relationship", "negative"),
    ("Views → Applies", "r = 0.91", "Strong positive correlation", "positive"),
    ("Salary MNAR", "70.87%", "Missing not at random", "negative"),
]

for i, (label, value, desc, delta_type) in enumerate(corr_data):
    with corr_cols[i]:
        st.markdown(f"""
        <div class="kpi-card" style="padding: 1.25rem;">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="font-size: 1.3rem;">{value}</div>
            <div class="kpi-delta {delta_type}">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 2rem 0;">
    <strong>DataScope</strong> — Built with Streamlit + Plotly + DuckDB &nbsp;·&nbsp;
    <a href="https://github.com/juandelaf1/Pearsons_Four" style="color: #6366f1;">GitHub</a> &nbsp;·&nbsp;
    <a href="https://hub.docker.com/r/juandelaf/datascope" style="color: #6366f1;">DockerHub</a> &nbsp;·&nbsp;
    <a href="https://www.kaggle.com/datasets/juandelaf/datascope-salary-analytics" style="color: #6366f1;">Kaggle</a>
</div>
""", unsafe_allow_html=True)
