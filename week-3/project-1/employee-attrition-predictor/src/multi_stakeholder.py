"""
Multi-Stakeholder Module - Prompt 2
Role-based dashboard views for HR Managers, Department Heads, and Individual Contributors.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.preprocessor import DataPreprocessor


CHART_COLORS = {
    'primary': '#6f7bf0',
    'secondary': '#b3bafa',
    'positive': '#2dd4a7',
    'negative': '#f0654f',
    'neutral': '#4b5468',
    'accent': '#e0a73e',
}


def _score_employees(df, model, preprocessor):
    scored = df.copy()
    feature_cols = list(preprocessor.feature_columns)
    df_model = scored.reindex(columns=feature_cols, fill_value=0)
    scored['AttritionProbability'] = model.predict_proba(df_model)[:, 1]
    scored['RiskTier'] = pd.cut(
        scored['AttritionProbability'],
        bins=[-0.01, 0.3, 0.6, 1.0],
        labels=['Low', 'Medium', 'High'],
    )
    return scored


# ════════════════════════════════════════════════════════════════════════════
#  HR MANAGER VIEW
# ════════════════════════════════════════════════════════════════════════════

def _render_hr_view(scored):
    st.markdown("""
    <div class="card">
        <div class="card-title">HR Manager View — Organizational Attrition Intelligence</div>
        <p>High-level trends, workforce health metrics, and organization-wide risk signals.</p>
    </div>
    """, unsafe_allow_html=True)

    total = len(scored)
    high = (scored['RiskTier'] == 'High').sum()
    med = (scored['RiskTier'] == 'Medium').sum()
    low = (scored['RiskTier'] == 'Low').sum()
    actual_attrition = (scored['Attrition'] == 'Yes').sum() if 'Attrition' in scored.columns else 0

    # ── KPI row ───────────────────────────────────────────────────────────
    st.markdown('<div class="eyebrow">Organization Health</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, (lbl, val, tag, cls) in zip(
        [c1, c2, c3, c4, c5],
        [
            ('Headcount', f'{total:,}', 'TOTAL', 'neutral'),
            ('High Risk', f'{high:,}', 'SHORT', 'short'),
            ('Medium Risk', f'{med:,}', 'WATCH', 'neutral'),
            ('Low Risk', f'{low:,}', 'LONG', 'long'),
            ('Historical Attrition', f'{actual_attrition}', 'ACTUAL', 'short'),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">{lbl}</span>
                    <span class="kpi-tag {cls}">{tag}</span>
                </div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)

    # ── Trend: Risk by department ──────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Risk by Department</div>', unsafe_allow_html=True)
    dept = (
        scored.groupby('Department')
        .agg(Headcount=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'),
             HighPct=('RiskTier', lambda x: (x == 'High').mean() * 100))
        .reset_index()
    )
    fig = px.bar(dept, x='Department', y='HighPct', color='AvgRisk', text='HighPct',
                 color_continuous_scale=[[0, CHART_COLORS['positive']], [1, CHART_COLORS['negative']]],
                 labels={'HighPct': '% High Risk'})
    fig.update_layout(template='plotly_dark', paper_bgcolor='#0d121c', plot_bgcolor='#0d121c',
                      font=dict(color='#8993a8'), height=340, margin=dict(l=40, r=40, t=20, b=40))
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # ── Risk by job role ──────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Risk by Job Role</div>', unsafe_allow_html=True)
    role = (
        scored.groupby('JobRole')
        .agg(Headcount=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'),
             HighPct=('RiskTier', lambda x: (x == 'High').mean() * 100))
        .reset_index().sort_values('AvgRisk', ascending=True)
    )
    fig_r, ax_r = plt.subplots(figsize=(10, 5))
    norm = (role['AvgRisk'] - role['AvgRisk'].min()) / (role['AvgRisk'].max() - role['AvgRisk'].min())
    base = np.array([111, 123, 240]) / 255.0
    cols = [(base[0], base[1], base[2], 0.3 + 0.7 * n) for n in norm]
    ax_r.barh(role['JobRole'], role['AvgRisk'] * 100, color=cols, height=0.55, zorder=3)
    ax_r.set_xlabel('Avg Risk %', labelpad=8)
    ax_r.set_title('Average Attrition Risk by Job Role', fontsize=13, fontweight='600', pad=14)
    for i, (_, r) in enumerate(role.iterrows()):
        ax_r.text(r['AvgRisk'] * 100 + 0.3, i, f"{r['AvgRisk']*100:.1f}%", va='center',
                  fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')
    plt.tight_layout()
    st.pyplot(fig_r)
    plt.close()

    # ── Top 20 highest risk employees ────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Top At-Risk Employees (Priority Action)</div>', unsafe_allow_html=True)
    top = scored.nlargest(20, 'AttritionProbability')
    show = ['Age', 'Department', 'JobRole', 'MonthlyIncome', 'YearsAtCompany', 'OverTime', 'AttritionProbability', 'RiskTier']
    existing = [c for c in show if c in top.columns]
    st.dataframe(top[existing], use_container_width=True, height=420,
                 column_config={'AttritionProbability': st.column_config.ProgressColumn('Risk', format='%.1f%%', min_value=0, max_value=1)})

    # ── Key Insights ──────────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Key Insights</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-block">
        <h4>Strategic Observations</h4>
        <ul style="padding-left:1.25rem;">
            <li><strong>{high}</strong> employees ({high/total*100:.1f}%) are at high risk — prioritize retention actions immediately.</li>
            <li><strong>{med}</strong> employees are in the watch zone — early intervention can prevent escalation.</li>
            <li>Department <strong>{dept.iloc[0]['Department']}</strong> has the highest average risk ({dept.iloc[0]['AvgRisk']*100:.1f}%).</li>
            <li>Overtime is a consistent predictor across all departments.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  DEPARTMENT HEAD VIEW
# ════════════════════════════════════════════════════════════════════════════

def _render_dept_head_view(scored):
    st.markdown("""
    <div class="card">
        <div class="card-title">Department Head View — Team Risk & Action Plan</div>
        <p>Drill into your department's attrition risk and get a prioritized action plan.</p>
    </div>
    """, unsafe_allow_html=True)

    departments = sorted(scored['Department'].unique())
    selected_dept = st.selectbox('Select Department', departments, key='dh_dept_select')
    dept_df = scored[scored['Department'] == selected_dept].copy()

    total = len(dept_df)
    high = (dept_df['RiskTier'] == 'High').sum()
    med = (dept_df['RiskTier'] == 'Medium').sum()
    avg_risk = dept_df['AttritionProbability'].mean() * 100

    st.markdown(f'<div class="eyebrow">{selected_dept} — Workforce Health</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, (lbl, val, tag, cls) in zip(
        [c1, c2, c3, c4],
        [
            ('Team Size', f'{total}', 'TOTAL', 'neutral'),
            ('High Risk', f'{high}', 'SHORT', 'short'),
            ('Medium Risk', f'{med}', 'WATCH', 'neutral'),
            ('Avg Risk', f'{avg_risk:.1f}%', 'DEPT', 'short' if avg_risk > 25 else 'long'),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">{lbl}</span>
                    <span class="kpi-tag {cls}">{tag}</span>
                </div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)

    # ── Risk by role within department ─────────────────────────────────────
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Risk by Role — {selected_dept}</div>', unsafe_allow_html=True)
    role = (
        dept_df.groupby('JobRole')
        .agg(Count=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'),
             HighPct=('RiskTier', lambda x: (x == 'High').mean() * 100))
        .reset_index().sort_values('AvgRisk', ascending=True)
    )
    fig, ax = plt.subplots(figsize=(10, max(3, len(role) * 0.6)))
    norm = (role['AvgRisk'] - role['AvgRisk'].min()) / max(role['AvgRisk'].max() - role['AvgRisk'].min(), 0.001)
    base = np.array([240, 101, 79]) / 255.0
    cols = [(base[0], base[1], base[2], 0.3 + 0.7 * n) for n in norm]
    ax.barh(role['JobRole'], role['AvgRisk'] * 100, color=cols, height=0.55, zorder=3)
    ax.set_xlabel('Avg Risk %', labelpad=8)
    ax.set_title(f'Attrition Risk by Role — {selected_dept}', fontsize=13, fontweight='600', pad=14)
    for i, (_, r) in enumerate(role.iterrows()):
        ax.text(r['AvgRisk'] * 100 + 0.3, i, f"{r['AvgRisk']*100:.1f}%", va='center',
                fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ── Top risk employees in this department ──────────────────────────────
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Priority Action List — {selected_dept}</div>', unsafe_allow_html=True)
    top = dept_df.nlargest(min(15, total), 'AttritionProbability')
    show = ['Age', 'JobRole', 'MonthlyIncome', 'YearsAtCompany', 'OverTime', 'JobSatisfaction', 'WorkLifeBalance', 'AttritionProbability']
    existing = [c for c in show if c in top.columns]
    st.dataframe(top[existing], use_container_width=True, height=400,
                 column_config={'AttritionProbability': st.column_config.ProgressColumn('Risk', format='%.1f%%', min_value=0, max_value=1)})

    # ── Department Action Plan ─────────────────────────────────────────────
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Action Plan — {selected_dept}</div>', unsafe_allow_html=True)
    ot_pct = (dept_df['OverTime'] == 'Yes').mean() * 100
    low_sat = (dept_df['JobSatisfaction'] <= 2).mean() * 100
    low_wlb = (dept_df['WorkLifeBalance'] <= 2).mean() * 100

    actions_html = f"""
    <div class="retention-block">
        <h4>Department-Specific Retention Strategy</h4>
        <ul style="padding-left:1.25rem;">
            <li><strong>Overtime Audit:</strong> {ot_pct:.0f}% of your team works overtime — redistribute workload to reduce burnout.</li>
            <li><strong>Satisfaction Pulse:</strong> {low_sat:.0f}% report low satisfaction — schedule 1-on-1 check-ins.</li>
            <li><strong>Work-Life Balance:</strong> {low_wlb:.0f}% report poor WLB — explore flexible scheduling.</li>
            <li><strong>High-Risk Priority:</strong> Focus retention conversations on the top {high} high-risk employees first.</li>
        </ul>
    </div>
    """
    st.markdown(actions_html, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  INDIVIDUAL CONTRIBUTOR VIEW
# ════════════════════════════════════════════════════════════════════════════

def _render_ic_view(scored):
    st.markdown("""
    <div class="card">
        <div class="card-title">Individual Contributor View — Your Career Health Check</div>
        <p>Understand your engagement profile and discover personalized career insights.</p>
    </div>
    """, unsafe_allow_html=True)

    n = len(scored)
    emp_idx = st.number_input('Enter your Employee Index (0 – {})'.format(n - 1), min_value=0, max_value=n - 1, value=0, key='ic_idx')
    emp = scored.iloc[emp_idx]

    risk = emp['AttritionProbability'] * 100
    tier = emp['RiskTier']
    tier_cls = 'short' if tier == 'High' else ('long' if tier == 'Low' else '')

    st.markdown(f"""
    <div class="verdict">
        <div class="verdict-strip {tier_cls}"></div>
        <div class="verdict-body">
            <div>
                <div class="verdict-label {tier_cls}">{tier} RISK</div>
                <div class="verdict-headline">Your Engagement Profile</div>
                <div class="verdict-sub">{emp.get('Department', '')} / {emp.get('JobRole', '')} — {emp.get('YearsAtCompany', 0)} years at company</div>
            </div>
            <div class="verdict-figure {tier_cls}">
                <div class="num">{risk:.1f}%</div>
                <div class="figcap">P(leaving)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Personal metrics ──────────────────────────────────────────────────
    st.markdown('<div class="eyebrow">Your Key Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, (lbl, val, tag, cls) in zip(
        [c1, c2, c3, c4],
        [
            ('Job Satisfaction', f"{emp.get('JobSatisfaction', 'N/A')}/4", 'SAT', 'long' if emp.get('JobSatisfaction', 3) >= 3 else 'short'),
            ('Work-Life Balance', f"{emp.get('WorkLifeBalance', 'N/A')}/4", 'WLB', 'long' if emp.get('WorkLifeBalance', 3) >= 3 else 'short'),
            ('Overtime', emp.get('OverTime', 'N/A'), 'OT', 'short' if emp.get('OverTime') == 'Yes' else 'long'),
            ('Monthly Income', f"${emp.get('MonthlyIncome', 0):,.0f}", 'INCOME', 'neutral'),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">{lbl}</span>
                    <span class="kpi-tag {cls}">{tag}</span>
                </div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)

    # ── Radar chart ───────────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Your Engagement Radar</div>', unsafe_allow_html=True)
    metrics_radar = ['JobSatisfaction', 'WorkLifeBalance', 'EnvironmentSatisfaction', 'JobInvolvement']
    vals = []
    for m in metrics_radar:
        v = emp.get(m, 3)
        if pd.isna(v):
            v = 3
        vals.append(float(v))
    avg_vals = [scored[m].mean() if m in scored.columns else 3 for m in metrics_radar]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=metrics_radar + [metrics_radar[0]],
                                  fill='toself', name='You',
                                  line=dict(color=CHART_COLORS['primary']),
                                  fillcolor='rgba(111,123,240,0.15)'))
    fig.add_trace(go.Scatterpolar(r=avg_vals + [avg_vals[0]], theta=metrics_radar + [metrics_radar[0]],
                                  fill='toself', name='Company Avg',
                                  line=dict(color=CHART_COLORS['accent'], dash='dot'),
                                  fillcolor='rgba(224,167,62,0.08)'))
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='#0d121c', plot_bgcolor='#0d121c',
        font=dict(color='#8993a8'), polar=dict(bgcolor='#0d121c', radialaxis=dict(range=[0, 4])),
        height=380, margin=dict(l=60, r=60, t=30, b=30),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Career Insights ───────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Personalized Career Insights</div>', unsafe_allow_html=True)
    insights = []
    if emp.get('YearsSinceLastPromotion', 0) >= 3:
        insights.append(('Career Growth', f"You haven't been promoted in {int(emp['YearsSinceLastPromotion'])} years. Consider discussing advancement opportunities with your manager.", 'accent'))
    if emp.get('OverTime') == 'Yes':
        insights.append(('Workload', 'Regular overtime may indicate burnout risk. Explore workload redistribution.', 'short'))
    if emp.get('JobSatisfaction', 3) <= 2:
        insights.append(('Engagement', 'Your satisfaction score is below average. A career development conversation may help.', 'short'))
    if emp.get('WorkLifeBalance', 3) <= 2:
        insights.append(('Balance', 'Work-life balance could be improved. Flexible arrangements may be available.', 'short'))
    if emp.get('MonthlyIncome', 0) < scored['MonthlyIncome'].median():
        insights.append(('Compensation', 'Your income is below the company median. A compensation review is recommended.', 'accent'))
    if emp.get('DistanceFromHome', 0) > 15:
        insights.append(('Commute', f"You travel {int(emp['DistanceFromHome'])} miles daily. Hybrid work could ease this.", 'accent'))
    if not insights:
        insights.append(('Stable', 'Your engagement profile is healthy. Keep up the great work!', 'long'))

    for title, text, color in insights:
        border_cls = 'short' if color == 'short' else ('long' if color == 'long' else '')
        st.markdown(f"""
        <div class="insight-block" style="border-left-color: var(--{color});">
            <h4 style="color: var(--{color});">{title}</h4>
            <p style="font-size:0.9rem;">{text}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── What you can do ──────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Steps You Can Take</div>', unsafe_allow_html=True)
    steps = []
    if emp.get('OverTime') == 'Yes':
        steps.append('Speak with your manager about workload balancing')
    if emp.get('JobSatisfaction', 3) <= 2:
        steps.append('Request a role rotation or new project assignment')
        steps.append('Discuss career goals with your team lead')
    if emp.get('WorkLifeBalance', 3) <= 2:
        steps.append('Explore flexible work or remote options')
    if emp.get('YearsSinceLastPromotion', 0) >= 3:
        steps.append('Prepare a promotion readiness document')
        steps.append('Seek a mentor outside your immediate team')
    if not steps:
        steps.append('Continue building on your strengths')
        steps.append('Consider mentoring junior colleagues')
    steps_html = ''.join(f'<li>{s}</li>' for s in steps)
    st.markdown(f"""
    <div class="retention-block">
        <h4>Your Action Items</h4>
        <ul style="padding-left:1.25rem;">{steps_html}</ul>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
#  MAIN RENDERER
# ════════════════════════════════════════════════════════════════════════════

def render_multi_stakeholder_page(df, model, preprocessor):
    scored = _score_employees(df, model, preprocessor)

    role = st.radio(
        'Select your role',
        ['HR Manager', 'Department Head', 'Individual Contributor'],
        horizontal=True,
        key='stakeholder_role',
    )

    if role == 'HR Manager':
        _render_hr_view(scored)
    elif role == 'Department Head':
        _render_dept_head_view(scored)
    else:
        _render_ic_view(scored)
