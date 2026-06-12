import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import load_spain, load_global

st.set_page_config(page_title="Spain Analysis", page_icon="🇪🇸", layout="wide")

df_spain = load_spain()
df_global = load_global()

st.markdown('<div class="section-header">🇪🇸 Spain 2026 — Multi-Source Salary Analysis</div>', unsafe_allow_html=True)

if df_spain.empty:
    st.warning("Spain dataset not found.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

with col1:
    total = len(df_spain)
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Spain Records</div>
        <div class="kpi-value">{total:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    median_eur = df_spain['salary_eur'].median()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Median Salary (EUR)</div>
        <div class="kpi-value">€{median_eur:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    median_usd = df_spain['salary_usd'].median()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Median Salary (USD)</div>
        <div class="kpi-value">${median_usd:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    n_sources = df_spain['source'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Data Sources</div>
        <div class="kpi-value">{n_sources}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["💰 Salary by Source", "📊 By Role & Seniority", "📈 Market Insights"])

with tab1:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig = px.box(
            df_spain,
            x='source',
            y='salary_eur',
            color='source',
            title='Salary Distribution by Source (Spain)',
            labels={'source': 'Source', 'salary_eur': 'Salary (EUR)'},
            color_discrete_sequence=px.colors.qualitative.Prism,
            points='outliers',
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=500,
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            showlegend=False,
        )
        st.plotly_chart(fig, width='stretch')

    with col_right:
        st.markdown("### 📊 Source Comparison")
        src_stats = df_spain.groupby('source').agg(
            Records=('salary_eur', 'count'),
            Mean_EUR=('salary_eur', 'mean'),
            Median_EUR=('salary_eur', 'median'),
            Min_EUR=('salary_eur', 'min'),
            Max_EUR=('salary_eur', 'max'),
        ).round(0)
        display = src_stats.copy()
        for c in ['Mean_EUR', 'Median_EUR', 'Min_EUR', 'Max_EUR']:
            display[c] = display[c].apply(lambda x: f"€{x:,.0f}")
        st.dataframe(display, width='stretch')

        st.markdown("### 📦 Dataset Composition")
        src_counts = df_spain['source'].value_counts()
        fig2 = px.pie(
            values=src_counts.values,
            names=src_counts.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Prism,
            title='Records by Source',
        )
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=300,
            legend=dict(orientation='h', y=-0.2, font=dict(size=9)),
        )
        fig2.update_traces(textposition='outside', textinfo='percent+label')
        st.plotly_chart(fig2, width='stretch')

with tab2:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        role_medians = df_spain.groupby('role_normalized')['salary_eur'].median().sort_values(ascending=True).reset_index()

        fig3 = px.bar(
            role_medians,
            x='salary_eur',
            y='role_normalized',
            orientation='h',
            title='Median Salary by Role (EUR)',
            labels={'salary_eur': 'Median Salary (EUR)', 'role_normalized': ''},
            color='salary_eur',
            color_continuous_scale='tealgrn',
            text='salary_eur',
        )
        fig3.update_traces(texttemplate='€{:,.0f}', textposition='outside', textfont_size=11)
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=450,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig3, width='stretch')

    with col_right:
        sen_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Executive']
        sen_medians = df_spain.groupby('seniority')['salary_eur'].median()
        sen_medians = sen_medians.reindex([s for s in sen_order if s in sen_medians.index]).dropna()

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=list(range(len(sen_medians))),
            y=sen_medians.values,
            mode='lines+markers+text',
            text=[f"€{v:,.0f}" for v in sen_medians.values],
            textposition='top center',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=14, color='#6366f1', line=dict(color='#a5b4fc', width=2)),
        ))
        fig4.update_layout(
            title='Salary Progression by Seniority (Spain)',
            xaxis=dict(
                tickvals=list(range(len(sen_medians))),
                ticktext=list(sen_medians.index),
                showgrid=False,
            ),
            yaxis=dict(
                title='Median Salary (EUR)',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                range=[0, sen_medians.max() * 1.2],
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=350,
        )
        st.plotly_chart(fig4, width='stretch')

with tab3:
    st.markdown('<div class="section-header">🌍 Spain vs Global</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        if not df_global.empty:
            spain_global = df_global[df_global['country_name'].str.contains('Spain', case=False, na=False)]
            if not spain_global.empty:
                spain_median_usd = spain_global['salary_usd'].median()
                global_median_usd = df_global['salary_usd'].median()

                comparison = pd.DataFrame({
                    'Metric': ['Median Salary (USD)', 'Records', 'Senior Premium'],
                    'Spain': [
                        f"${spain_median_usd:,.0f}",
                        f"{len(spain_global):,}",
                        "~+60%",
                    ],
                    'Global': [
                        f"${global_median_usd:,.0f}",
                        f"{len(df_global):,}",
                        "~+53%",
                    ],
                })
                st.markdown("### Spain vs Global Benchmark")
                st.dataframe(comparison, hide_index=True, width='stretch')

                fig5 = go.Figure()
                fig5.add_trace(go.Bar(
                    name='Spain',
                    x=['Median Salary'],
                    y=[spain_median_usd],
                    marker_color='#6366f1',
                    text=[f"${spain_median_usd:,.0f}"],
                    textposition='outside',
                ))
                fig5.add_trace(go.Bar(
                    name='Global',
                    x=['Median Salary'],
                    y=[global_median_usd],
                    marker_color='#f59e0b',
                    text=[f"${global_median_usd:,.0f}"],
                    textposition='outside',
                ))
                fig5.update_layout(
                    title='Spain vs Global — Median Salary',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    height=350,
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    legend=dict(orientation='h', y=1.1),
                )
                st.plotly_chart(fig5, width='stretch')

    with col_right:
        st.markdown("### 🇪🇸 Spain Market Insights")
        st.markdown("""
        <div class="insight-box">
        <h4>Key Findings</h4>
        <p>
        • <strong>Data Scientist</strong> is Spain's best-paid data role
          (Senior median: <strong>€61.5K</strong>)<br>
        • Spain median salary: <strong>€43,200/yr</strong> raw →
          <strong>$66,683 USD</strong> PPP-adjusted (+54% vs EU average)<br>
        • <strong>Manfred 2026</strong> dominates the Spain dataset (92%)
          but is also the most current and Spain-specific<br>
        • Spain's data market shows <strong>+60% senior premium</strong>,
          consistent with global patterns
        </p>
        </div>
        """, unsafe_allow_html=True)

        src_detail = df_spain['source'].value_counts().reset_index()
        src_detail.columns = ['Source', 'Records']
        st.markdown("### Sources Detail")
        st.dataframe(src_detail, hide_index=True, width='stretch')

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    Data sources: Manfred 2026 Salary Guide · Glassdoor ES · Kaggle DS Salaries (Spain)
</div>
""", unsafe_allow_html=True)
