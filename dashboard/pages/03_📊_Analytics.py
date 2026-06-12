import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import load_analytics, load_global

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.markdown('<div class="section-header">📊 DuckDB Analytics Engine</div>', unsafe_allow_html=True)

queries = {
    "01_median_salary_by_role": "Median Salary by Role",
    "02_median_salary_by_country": "Median Salary by Country",
    "03_seniority_premium": "Seniority Premium Analysis",
    "04_top_roles_by_country": "Top Roles by Country",
    "05_market_sizing": "Market Sizing",
}

tab_labels = list(queries.values())
tabs = st.tabs(tab_labels)

for idx, (filename, title) in enumerate(queries.items()):
    with tabs[idx]:
        df = load_analytics(f"{filename}.csv")

        if df.empty:
            st.warning(f"Analytics file {filename}.csv not found.")
            continue

        st.markdown(f"### {title}")

        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        text_cols = df.select_dtypes(exclude='number').columns.tolist()

        col_left, col_right = st.columns([3, 2])

        with col_left:
            if len(numeric_cols) == 1 and len(text_cols) >= 1:
                val_col = numeric_cols[0]
                cat_col = text_cols[0]

                sorted_df = df.sort_values(val_col, ascending=True)

                fig = px.bar(
                    sorted_df,
                    x=val_col,
                    y=cat_col,
                    orientation='h',
                    title=title,
                    color=val_col,
                    color_continuous_scale='viridis',
                    text=val_col,
                    labels={val_col: val_col.replace('_', ' ').title(), cat_col: cat_col.replace('_', ' ').title()},
                )
                fig.update_traces(
                    texttemplate='%{text:,.0f}',
                    textposition='outside',
                    textfont_size=10,
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    height=max(400, 30 * len(sorted_df)),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(showgrid=False),
                )
                st.plotly_chart(fig, width='stretch')

            elif len(numeric_cols) >= 2 and len(text_cols) >= 1:
                fig = px.scatter(
                    df,
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    color=text_cols[0] if len(text_cols) > 0 else None,
                    hover_data=text_cols,
                    title=title,
                    labels={c: c.replace('_', ' ').title() for c in df.columns},
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    height=500,
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                )
                st.plotly_chart(fig, width='stretch')

            else:
                fig = px.line(
                    df,
                    x=df.columns[0],
                    y=df.columns[1] if len(df.columns) > 1 else None,
                    title=title,
                    markers=True,
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    height=400,
                )
                st.plotly_chart(fig, width='stretch')

        with col_right:
            st.markdown("### 📋 Data Table")
            display_df = df.copy()
            for c in numeric_cols:
                if display_df[c].dtype in ['float64', 'float32']:
                    display_df[c] = display_df[c].apply(lambda x: f"{x:,.2f}")
            st.dataframe(display_df, hide_index=True, width='stretch')

            st.markdown("### 📥 Download")
            csv = df.to_csv(index=False)
            st.download_button(
                f"Download {filename}.csv",
                csv,
                file_name=f"{filename}.csv",
                mime="text/csv",
            )

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    Powered by <strong>DuckDB</strong> — 5 analytical queries on the unified global dataset
</div>
""", unsafe_allow_html=True)
