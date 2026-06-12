import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from utils import load_global, get_global_filters, filter_global_df

st.set_page_config(page_title="Global Analysis", page_icon="🌍", layout="wide")

st.markdown('<div class="section-header">🌍 Global Salary Analysis</div>', unsafe_allow_html=True)

df = load_global()

if df.empty:
    st.warning("Global dataset not found.")
    st.stop()

roles, seniorities, countries = get_global_filters(df)

with st.sidebar:
    st.markdown("### 🔍 Filters")
    selected_roles = st.multiselect("Role", roles, default=[])
    selected_seniorities = st.multiselect("Seniority", seniorities, default=[])
    selected_countries = st.multiselect("Country", countries, default=[])

    salary_min = int(df['salary_usd'].min())
    salary_max = int(df['salary_usd'].max())
    salary_range = st.slider(
        "Salary Range (USD)",
        min_value=salary_min,
        max_value=salary_max,
        value=(salary_min, salary_max),
    )

    df_filtered = filter_global_df(df, selected_roles, selected_seniorities, selected_countries, salary_range)

    n_filtered = len(df_filtered)
    total = len(df)
    st.markdown(f"**Showing {n_filtered:,} / {total:,} records**")

    if st.button("📥 Download Filtered CSV"):
        st.download_button(
            "Download",
            df_filtered.to_csv(index=False),
            file_name="datascope_filtered.csv",
            mime="text/csv",
        )

tab1, tab2, tab3 = st.tabs(["💰 Salary by Role", "🌍 By Country", "📊 Seniority Analysis"])

with tab1:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        role_medians = (
            df_filtered.groupby('role_normalized')['salary_usd']
            .median()
            .sort_values(ascending=True)
            .reset_index()
        )
        role_medians['role_normalized'] = role_medians['role_normalized'].str.title()

        fig = px.bar(
            role_medians,
            x='salary_usd',
            y='role_normalized',
            orientation='h',
            title='Median Salary by Role (USD)',
            labels={'salary_usd': 'Median Salary (USD)', 'role_normalized': ''},
            color='salary_usd',
            color_continuous_scale='viridis',
            text='salary_usd',
        )
        fig.update_traces(texttemplate='${:,.0f}', textposition='outside', textfont_size=11)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=500,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, width='stretch')

    with col_right:
        st.markdown("### 📊 Salary Statistics")
        stats = df_filtered['salary_usd'].dropna()
        if len(stats) > 0:
            stats_df = pd.DataFrame({
                'Metric': ['Count', 'Mean', 'Median', 'Std Dev', 'P25', 'P75', 'Min', 'Max'],
                'Value': [
                    f"{len(stats):,}",
                    f"${stats.mean():,.0f}",
                    f"${stats.median():,.0f}",
                    f"${stats.std():,.0f}",
                    f"${stats.quantile(0.25):,.0f}",
                    f"${stats.quantile(0.75):,.0f}",
                    f"${stats.min():,.0f}",
                    f"${stats.max():,.0f}",
                ],
            })
            st.dataframe(stats_df, hide_index=True, width='stretch')

        if not df_filtered.empty:
            top_roles = (
                df_filtered['role_normalized']
                .value_counts()
                .head(8)
                .reset_index()
            )
            top_roles.columns = ['role', 'count']
            fig2 = px.bar(
                top_roles,
                x='count',
                y='role',
                orientation='h',
                title='Most Common Roles',
                color='count',
                color_continuous_scale='tealgrn',
                labels={'count': 'Count', 'role': ''},
            )
            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e2e8f0',
                height=300,
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig2, width='stretch')

with tab2:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        country_medians = df_filtered.groupby('country_name')['salary_usd'].median().reset_index().dropna()

        fig_map = px.choropleth(
            country_medians,
            locations='country_name',
            locationmode='country names',
            color='salary_usd',
            color_continuous_scale='plasma',
            title='Median Salary by Country',
            labels={'salary_usd': 'Median (USD)'},
        )
        fig_map.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=True,
                coastlinecolor='rgba(255,255,255,0.1)',
                projection_type='natural earth',
                bgcolor='rgba(0,0,0,0)',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=500,
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig_map, width='stretch')

    with col_right:
        st.markdown("### 🏆 Top 10 Countries by Salary")
        top_countries = (
            df_filtered.groupby('country_name')['salary_usd']
            .median()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig3 = px.bar(
            top_countries,
            x='salary_usd',
            y='country_name',
            orientation='h',
            color='salary_usd',
            color_continuous_scale='plasma',
            labels={'salary_usd': 'Median Salary (USD)', 'country_name': ''},
            text='salary_usd',
        )
        fig3.update_traces(texttemplate='${:,.0f}', textposition='outside', textfont_size=10)
        fig3.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=400,
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig3, width='stretch')

with tab3:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        sen_order = ['Junior', 'Mid', 'Senior', 'Lead', 'Executive']
        sen_medians = df_filtered.groupby('seniority')['salary_usd'].median()
        sen_medians = sen_medians.reindex([s for s in sen_order if s in sen_medians.index]).dropna()

        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=list(range(len(sen_medians))),
            y=sen_medians.values,
            mode='lines+markers+text',
            text=[f"${v:,.0f}" for v in sen_medians.values],
            textposition='top center',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=14, color='#6366f1', line=dict(color='#a5b4fc', width=2)),
        ))
        fig4.update_layout(
            title='Salary Progression by Seniority',
            xaxis=dict(
                tickvals=list(range(len(sen_medians))),
                ticktext=list(sen_medians.index),
                showgrid=False,
            ),
            yaxis=dict(
                title='Median Salary (USD)',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.05)',
                range=[0, sen_medians.max() * 1.2],
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=400,
        )
        st.plotly_chart(fig4, width='stretch')

    with col_right:
        st.markdown("### 💼 Seniority Premium")
        if not df_filtered.empty:
            sen_stats = df_filtered.groupby('seniority').agg(
                Count=('salary_usd', 'count'),
                Median=('salary_usd', 'median'),
                Mean=('salary_usd', 'mean'),
            ).round(0)
            if 'Senior' in sen_stats.index:
                sen_stats['vs_Senior'] = (
                    (sen_stats['Median'] / sen_stats.loc['Senior', 'Median'] - 1) * 100
                )
            display = sen_stats.copy()
            if 'vs_Senior' in display.columns:
                display['vs_Senior'] = display['vs_Senior'].apply(
                    lambda x: f"{x:+.1f}%" if not np.isnan(x) else "N/A"
                )
            display['Median'] = display['Median'].apply(lambda x: f"${x:,.0f}")
            display['Mean'] = display['Mean'].apply(lambda x: f"${x:,.0f}")
            st.dataframe(display, width='stretch')

        st.markdown("### 📦 Dataset Breakdown")
        src_counts = df_filtered['dataset'].value_counts().reset_index()
        src_counts.columns = ['dataset', 'count']
        fig5 = px.pie(
            src_counts,
            values='count',
            names='dataset',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Prism,
        )
        fig5.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=250,
            showlegend=True,
            legend=dict(orientation='h', y=-0.2, font=dict(size=9)),
        )
        st.plotly_chart(fig5, width='stretch')
