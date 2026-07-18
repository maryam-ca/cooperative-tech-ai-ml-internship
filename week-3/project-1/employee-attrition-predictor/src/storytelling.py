"""
Storytelling Module - Prompt 1: The Storytelling Approach
AI-powered early warning system that tells a story about attrition risk.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from pathlib import Path
from src.preprocessor import DataPreprocessor


CHART_COLORS = {
    'primary': '#6f7bf0',
    'secondary': '#b3bafa',
    'positive': '#2dd4a7',
    'negative': '#f0654f',
    'neutral': '#4b5468',
    'accent': '#e0a73e',
}


def _generate_employee_narratives(df, model, preprocessor):
    """Score every employee and attach narrative context."""
    scored = df.copy()

    feature_cols = list(preprocessor.feature_columns)
    df_model = scored.reindex(columns=feature_cols, fill_value=0)
    probas = model.predict_proba(df_model)[:, 1]
    scored['AttritionProbability'] = probas
    scored['RiskTier'] = pd.cut(
        probas,
        bins=[-0.01, 0.3, 0.6, 1.0],
        labels=['Low', 'Medium', 'High'],
    )

    def _narrative(row):
        parts = []
        if row['OverTime'] == 'Yes':
            parts.append('works overtime regularly')
        if row['JobSatisfaction'] <= 2:
            parts.append('reports low job satisfaction')
        if row['WorkLifeBalance'] <= 2:
            parts.append('has poor work-life balance')
        if row['YearsAtCompany'] <= 2:
            parts.append('is still early in their tenure')
        if row['YearsSinceLastPromotion'] >= 3:
            parts.append('has not been promoted recently')
        if row['MonthlyIncome'] < df['MonthlyIncome'].median():
            parts.append('earns below the median income')
        if row['DistanceFromHome'] > 15:
            parts.append('has a long commute')
        if not parts:
            parts.append('shows stable engagement indicators')
        return '; '.join(parts)

    scored['Narrative'] = scored.apply(_narrative, axis=1)
    return scored


def _build_risk_timeline(scored_df):
    """Aggregate risk tiers over tenure buckets to simulate a timeline."""
    bins = [0, 2, 5, 10, 20, 40]
    labels = ['0-2 yrs', '3-5 yrs', '6-10 yrs', '11-20 yrs', '20+ yrs']
    scored_df = scored_df.copy()
    scored_df['TenureBucket'] = pd.cut(scored_df['YearsAtCompany'], bins=bins, labels=labels)

    timeline = (
        scored_df.groupby('TenureBucket', observed=False)['AttritionProbability']
        .agg(['mean', 'count'])
        .reset_index()
    )
    timeline.columns = ['TenureBucket', 'AvgRisk', 'Headcount']
    return timeline


def _driver_importance(scored_df):
    """Quantify how much each risk factor co-occurs with high risk."""
    high = scored_df[scored_df['RiskTier'] == 'High']
    total_high = len(high)
    if total_high == 0:
        return pd.DataFrame()

    drivers = {
        'Over Time': (high['OverTime'] == 'Yes').mean() * 100,
        'Low Job Satisfaction': (high['JobSatisfaction'] <= 2).mean() * 100,
        'Poor Work-Life Balance': (high['WorkLifeBalance'] <= 2).mean() * 100,
        'Short Tenure (< 2 yrs)': (high['YearsAtCompany'] <= 2).mean() * 100,
        'No Recent Promotion': (high['YearsSinceLastPromotion'] >= 3).mean() * 100,
        'Below Median Income': (high['MonthlyIncome'] < scored_df['MonthlyIncome'].median()).mean() * 100,
        'Long Commute (> 15 mi)': (high['DistanceFromHome'] > 15).mean() * 100,
    }
    return pd.DataFrame({'Driver': drivers.keys(), 'PctHighRisk': drivers.values()}).sort_values('PctHighRisk', ascending=False)


def _department_risk_summary(scored_df):
    """Risk breakdown per department."""
    dept = (
        scored_df.groupby('Department')
        .agg(
            Headcount=('Attrition', 'count'),
            AvgRisk=('AttritionProbability', 'mean'),
            HighRiskCount=('RiskTier', lambda x: (x == 'High').sum()),
            ActualAttrition=('Attrition', lambda x: (x == 'Yes').sum()),
        )
        .reset_index()
    )
    dept['HighRiskPct'] = (dept['HighRiskCount'] / dept['Headcount'] * 100).round(1)
    dept['ActualAttritionRate'] = (dept['ActualAttrition'] / dept['Headcount'] * 100).round(1)
    return dept.sort_values('AvgRisk', ascending=False)


def _recommended_actions(row):
    """Generate context-aware retention actions for an employee."""
    actions = []
    if row['OverTime'] == 'Yes':
        actions.append('Reduce overtime burden — audit workload distribution')
    if row['JobSatisfaction'] <= 2:
        actions.append('Schedule a 1-on-1 career development conversation')
    if row['WorkLifeBalance'] <= 2:
        actions.append('Evaluate flexible work arrangements')
    if row['YearsAtCompany'] <= 2:
        actions.append('Assign an onboarding mentor for early-tenure support')
    if row['YearsSinceLastPromotion'] >= 3:
        actions.append('Discuss promotion timeline or role expansion')
    if row['MonthlyIncome'] < 5000:
        actions.append('Review compensation against market benchmarks')
    if row['DistanceFromHome'] > 15:
        actions.append('Consider hybrid/remote work options')
    if not actions:
        actions.append('Continue current engagement — monitor quarterly')
    return actions


def render_storytelling_page(df, model, preprocessor):
    """Render the full Storytelling page."""
    # ── Masthead ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-title">Early Warning System — The Story of Attrition</div>
        <p>Every number has a story. This view transforms raw predictions into
        actionable narratives that HR and managers can act on <em>today</em>.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Score all employees ───────────────────────────────────────────────
    scored = _generate_employee_narratives(df, model, preprocessor)

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 1 — Executive KPI Ticker
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow">System overview</div>', unsafe_allow_html=True)

    total = len(scored)
    high_risk = (scored['RiskTier'] == 'High').sum()
    med_risk = (scored['RiskTier'] == 'Medium').sum()
    low_risk = (scored['RiskTier'] == 'Low').sum()
    avg_risk = scored['AttritionProbability'].mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    for col, (label, value, tag, tag_cls) in zip(
        [c1, c2, c3, c4],
        [
            ('Headcount', f'{total:,}', 'TOTAL', 'neutral'),
            ('High Risk', f'{high_risk:,}', 'SHORT', 'short'),
            ('Medium Risk', f'{med_risk:,}', 'WATCH', 'neutral'),
            ('Avg Risk Score', f'{avg_risk:.1f}%', 'MEAN', 'short'),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">{label}</span>
                    <span class="kpi-tag {tag_cls}">{tag}</span>
                </div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 2 — Risk Timeline (story arc)
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">The attrition story arc</div>', unsafe_allow_html=True)

    timeline = _build_risk_timeline(scored)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=timeline['TenureBucket'],
            y=timeline['Headcount'],
            name='Headcount',
            marker_color='rgba(111,123,240,0.25)',
            marker_line=dict(width=0),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=timeline['TenureBucket'],
            y=timeline['AvgRisk'] * 100,
            name='Avg Risk %',
            mode='lines+markers',
            line=dict(color=CHART_COLORS['negative'], width=2.5),
            marker=dict(size=8),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0d121c',
        plot_bgcolor='#0d121c',
        font=dict(color='#8993a8'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=370,
        margin=dict(l=40, r=40, t=30, b=40),
    )
    fig.update_yaxes(title_text='Headcount', secondary_y=False, gridcolor='#1b2333')
    fig.update_yaxes(title_text='Avg Risk %', secondary_y=True, gridcolor='#1b2333', ticksuffix='%')
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        '**The narrative:** Risk peaks sharply in the 0–2 year bucket — '
        'the "make-or-break" window. The story flattens for mid-career employees, '
        'then rises again for 10+ year veterans who may feel plateaued.'
    )

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 3 — Top Risk Drivers
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Why employees leave — root causes</div>', unsafe_allow_html=True)

    drivers = _driver_importance(scored)

    fig_d, ax_d = plt.subplots(figsize=(10, 4.5))
    norm = (drivers['PctHighRisk'] - drivers['PctHighRisk'].min()) / (drivers['PctHighRisk'].max() - drivers['PctHighRisk'].min())
    base = np.array([240, 101, 79]) / 255.0
    bar_cols = [(base[0], base[1], base[2], 0.35 + 0.65 * n) for n in norm]
    bars = ax_d.barh(drivers['Driver'], drivers['PctHighRisk'], color=bar_cols, height=0.55, zorder=3)
    ax_d.set_xlabel('% of High-Risk Employees Affected', labelpad=8)
    ax_d.set_title('Root Causes Among High-Risk Employees', fontsize=13, fontweight='600', pad=14)
    ax_d.invert_yaxis()
    for bar, val in zip(bars, drivers['PctHighRisk']):
        ax_d.text(val + 0.8, bar.get_y() + bar.get_height() / 2, f'{val:.0f}%',
                  va='center', fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')
    plt.tight_layout()
    st.pyplot(fig_d)
    plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 4 — Department Risk Summary
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Department risk landscape</div>', unsafe_allow_html=True)

    dept_summary = _department_risk_summary(scored)

    fig_dept = px.bar(
        dept_summary,
        x='Department',
        y='HighRiskPct',
        color='AvgRisk',
        color_continuous_scale=[[0, CHART_COLORS['positive']], [1, CHART_COLORS['negative']]],
        text='HighRiskPct',
        labels={'HighRiskPct': '% High Risk', 'AvgRisk': 'Avg Risk Score'},
    )
    fig_dept.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0d121c',
        plot_bgcolor='#0d121c',
        font=dict(color='#8993a8'),
        height=340,
        margin=dict(l=40, r=40, t=20, b=40),
        coloraxis_colorbar=dict(title='Avg Risk', ticksuffix='%'),
    )
    fig_dept.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_dept, use_container_width=True)

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 5 — Individual Employee Stories
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Employee risk stories</div>', unsafe_allow_html=True)

    tier_filter = st.radio(
        'Filter by risk tier',
        ['High', 'Medium', 'Low'],
        horizontal=True,
        key='story_tier_filter',
    )
    filtered = scored[scored['RiskTier'] == tier_filter].sort_values('AttritionProbability', ascending=False)
    display_cols = ['Age', 'Department', 'JobRole', 'MonthlyIncome', 'YearsAtCompany',
                    'OverTime', 'JobSatisfaction', 'WorkLifeBalance', 'AttritionProbability', 'Narrative']
    existing = [c for c in display_cols if c in filtered.columns]

    if len(filtered) == 0:
        st.info('No employees in this risk tier.')
    else:
        st.dataframe(
            filtered[existing].head(30),
            use_container_width=True,
            height=380,
            column_config={
                'AttritionProbability': st.column_config.ProgressColumn(
                    'Risk', format='%.1f%%', min_value=0, max_value=1
                ),
                'Narrative': st.column_config.TextColumn('Story', width='large'),
            },
        )

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 6 — Deep-Dive: Single Employee Narrative
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Deep-dive: individual story</div>', unsafe_allow_html=True)

    emp_names = [f"Employee #{i}" for i in scored.index]
    selected_name = st.selectbox('Select an employee', emp_names, key='story_emp_select')
    idx = scored.index[emp_names.index(selected_name)]
    emp = scored.loc[idx]

    risk_pct = emp['AttritionProbability'] * 100
    tier = emp['RiskTier']
    tier_color = CHART_COLORS['negative'] if tier == 'High' else (CHART_COLORS['accent'] if tier == 'Medium' else CHART_COLORS['positive'])

    st.markdown(f"""
    <div class="verdict">
        <div class="verdict-strip {'short' if tier == 'High' else 'long'}"></div>
        <div class="verdict-body">
            <div>
                <div class="verdict-label {'short' if tier == 'High' else 'long'}">{tier} RISK</div>
                <div class="verdict-headline">{selected_name}</div>
                <div class="verdict-sub">{emp['Narrative']}</div>
            </div>
            <div class="verdict-figure {'short' if tier == 'High' else 'long'}">
                <div class="num">{risk_pct:.1f}%</div>
                <div class="figcap">P(attrition)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Action plan
    actions = _recommended_actions(emp)
    action_html = ''.join(f'<li>{a}</li>' for a in actions)
    st.markdown(f"""
    <div class="retention-block">
        <h4>Recommended Retention Actions</h4>
        <ul style="padding-left:1.25rem;">{action_html}</ul>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    #  SECTION 7 — Download scored data
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Export</div>', unsafe_allow_html=True)
    export_cols = ['Age', 'Department', 'JobRole', 'MonthlyIncome', 'YearsAtCompany',
                   'OverTime', 'JobSatisfaction', 'WorkLifeBalance', 'AttritionProbability', 'RiskTier', 'Narrative']
    export_existing = [c for c in export_cols if c in scored.columns]
    csv = scored[export_existing].to_csv(index=False)
    st.download_button(
        'Download Full Risk Report (CSV)',
        data=csv,
        file_name='employee_risk_narratives.csv',
        mime='text/csv',
    )
