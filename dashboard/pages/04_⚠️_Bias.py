import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import load_linkedin

st.set_page_config(page_title="Bias Analysis", page_icon="⚠️", layout="wide")

df_linkedin = load_linkedin()

st.markdown('<div class="section-header">⚠️ Bias & Data Quality Analysis</div>', unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<h4>Why This Matters</h4>
<p>
Understanding biases in salary data is critical for accurate market analysis.
This section quantifies known biases in the LinkedIn dataset and their impact
on salary estimates.
</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📉 Missing Data", "🎯 Selection Bias", "🔬 Statistical Tests"])

with tab1:
    st.markdown("### 📉 Missing Data Analysis")

    if not df_linkedin.empty:
        missing = df_linkedin.isnull().mean().sort_values(ascending=False) * 100
        missing_df = missing.reset_index()
        missing_df.columns = ['Column', 'Missing %']
        missing_df = missing_df[missing_df['Missing %'] > 0].head(15)

        col_left, col_right = st.columns([3, 2])

        with col_left:
            fig = px.bar(
                missing_df,
                x='Missing %',
                y='Column',
                orientation='h',
                title='Missing Values by Column (%)',
                color='Missing %',
                color_continuous_scale='reds',
                text='Missing %',
                labels={'Missing %': 'Missing (%)', 'Column': ''},
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e2e8f0',
                height=400,
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 110]),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig, width='stretch')

        with col_right:
            st.markdown("### Key Findings")
            st.markdown(f"""
            <div class="insight-box">
            <h4>Salary MNAR</h4>
            <p>
            <strong>70.87%</strong> of salaries are missing.
            This is <strong>Missing Not At Random (MNAR)</strong> —
            lower salaries are more likely to be hidden.
            </p>
            </div>
            """, unsafe_allow_html=True)

            if 'formatted_experience_level' in df_linkedin.columns:
                st.markdown("### Missing Salary by Experience")
                missing_by_exp = (
                    df_linkedin.groupby('formatted_experience_level')['normalized_salary']
                    .apply(lambda x: x.isnull().mean() * 100)
                    .sort_values(ascending=False)
                )
                fig2 = px.bar(
                    x=missing_by_exp.values,
                    y=missing_by_exp.index,
                    orientation='h',
                    color=missing_by_exp.values,
                    color_continuous_scale='reds',
                    text=missing_by_exp,
                    labels={'x': 'Missing Rate (%)', 'y': ''},
                )
                fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#e2e8f0',
                    height=250,
                    xaxis=dict(range=[0, 100]),
                )
                st.plotly_chart(fig2, width='stretch')

with tab2:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 🎯 Experience Level Distribution")

        if not df_linkedin.empty and 'formatted_experience_level' in df_linkedin.columns:
            exp_order = ['Entry level', 'Associate', 'Mid-Senior level', 'Director', 'Executive']
            exp_counts = df_linkedin['formatted_experience_level'].value_counts()
            exp_counts = exp_counts.reindex([e for e in exp_order if e in exp_counts.index])

            colors = {'Entry level': '#ef4444', 'Associate': '#f97316',
                      'Mid-Senior level': '#eab308', 'Director': '#6366f1',
                      'Executive': '#8b5cf6'}

            fig = go.Figure()
            for level in exp_counts.index:
                fig.add_trace(go.Bar(
                    name=level,
                    x=[level],
                    y=[exp_counts[level]],
                    marker_color=colors.get(level, '#6366f1'),
                    text=[f"{exp_counts[level]:,} ({exp_counts[level]/exp_counts.sum()*100:.1f}%)"],
                    textposition='outside',
                ))
            fig.update_layout(
                title='Distribution of Job Postings by Experience Level',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#e2e8f0',
                height=400,
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='Count'),
                xaxis=dict(showgrid=False),
                showlegend=False,
                bargap=0.3,
            )
            st.plotly_chart(fig, width='stretch')

    with col_right:
        st.markdown("### Selection Bias")
        st.markdown("""
        <div class="insight-box">
        <h4>Seniority Overrepresentation</h4>
        <p>
        <strong>83.81%</strong> of postings target Senior/Experienced roles,
        vs only <strong>16.19%</strong> for Junior/Early-Career.
        This skews median salary estimates upward.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Geographic Bias")
        st.markdown("""
        <div class="insight-box">
        <h4>US/UK Centric</h4>
        <p>
        US and UK are heavily overrepresented.
        <strong>0 postings from Spain</strong> in the LinkedIn data,
        despite being a major EU data market.
        </p>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📊 Conditional Probabilities")

        st.markdown("""
        <div class="insight-box">
        <h4>Stack Overflow Analysis</h4>
        <p>
        • P(High Salary | Senior/Experienced) = <strong>53.42%</strong><br>
        • P(High Salary | Junior/Early-Career) = <strong>22.57%</strong><br>
        • Senior professionals are <strong>2.4× more likely</strong>
          to earn a high salary
        </p>
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Senior/Experienced',
            x=['P(High Salary | Level)'],
            y=[53.42],
            marker_color='#6366f1',
            text=['53.42%'],
            textposition='outside',
        ))
        fig.add_trace(go.Bar(
            name='Junior/Early-Career',
            x=['P(High Salary | Level)'],
            y=[22.57],
            marker_color='#f59e0b',
            text=['22.57%'],
            textposition='outside',
        ))
        fig.update_layout(
            title='Probability of High Salary by Experience',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0',
            height=350,
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)',
                       title='Probability (%)', range=[0, 70]),
            legend=dict(orientation='h', y=1.1),
        )
        st.plotly_chart(fig, width='stretch')

    with col_right:
        st.markdown("### 🔬 Cross-Dataset Comparison")

        st.markdown("""
        <div class="insight-box">
        <h4>Stack Overflow vs LinkedIn</h4>
        <p>
        <strong>Key differences in perspective:</strong>
        </p>
        </div>
        """, unsafe_allow_html=True)

        comparison = pd.DataFrame({
            'Metric': ['Median Salary', 'Perspective', 'Sample Size'],
            'Stack Overflow': ['$85,000', 'Developer self-reported', '~20K respondents'],
            'LinkedIn': ['$135,588', 'Corporate real offers', '1,831 data roles'],
        })
        st.dataframe(comparison, hide_index=True, width='stretch')

        st.markdown("""
        <div class="insight-box">
        <h4>Key Insight</h4>
        <p>
        LinkedIn offers reflect <strong>real market rates</strong>
        (<strong>+59%</strong> median vs Stack Overflow).
        The gap reflects differences in methodology
        (self-reported vs actual offers) and population
        (global developers vs specialized data roles).
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Methodological Correction")
        st.markdown("""
        <div class="insight-box">
        <h4>Initial vs Corrected</h4>
        <p>
        Initial analysis used <strong>all LinkedIn professions</strong>
        (~75K salaries). After isolating <strong>Data Roles only</strong>
        (1,831 records):
        </p>
        </div>
        """, unsafe_allow_html=True)

        correction = pd.DataFrame({
            'Metric': ['Remote Premium', 'Views → Applies (r)', 'Experience → Salary (r)'],
            'All Professions': ['+45.1%', '0.62', '0.43'],
            'Data Roles Only': ['−1.2% (p=0.46)', '0.91', '0.49'],
        })
        st.dataframe(correction, hide_index=True, width='stretch')

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
    Bias quantification is essential for accurate market analysis.
    Always consider data limitations when interpreting salary benchmarks.
</div>
""", unsafe_allow_html=True)
