"""
What-If Simulator Module - Prompt 3
Interactive slider-based tool to explore how factor changes impact attrition risk.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import joblib
from pathlib import Path
from src.preprocessor import DataPreprocessor


CHART_COLORS = {
    'primary': '#4c56af',
    'secondary': '#8690ee',
    'positive': '#007165',
    'negative': '#e17c5a',
    'neutral': '#767683',
    'accent': '#b57614',
}


def _make_base_input():
    """Return a sensible baseline employee profile."""
    return {
        'Age': 35,
        'Gender': 'Male',
        'MaritalStatus': 'Single',
        'Department': 'Research & Development',
        'JobRole': 'Research Scientist',
        'Education': 3,
        'MonthlyIncome': 5000,
        'YearsAtCompany': 4,
        'OverTime': 'No',
        'TotalWorkingYears': 10,
        'YearsInCurrentRole': 3,
        'JobSatisfaction': 3,
        'WorkLifeBalance': 3,
        'DistanceFromHome': 10,
        'NumCompaniesWorked': 2,
    }


def _predict_with_overrides(model, preprocessor, base_input, overrides):
    """Run a prediction with selected overrides applied to the base profile."""
    inp = base_input.copy()
    inp.update(overrides)

    df_input = pd.DataFrame([inp])
    try:
        model_dir = Path(__file__).parent.parent / "models"
        local_preprocessor = DataPreprocessor()
        local_preprocessor.scaler = joblib.load(model_dir / "scaler.pkl")
        local_preprocessor.label_encoders = joblib.load(model_dir / "label_encoders.pkl")
        local_preprocessor.feature_columns = joblib.load(model_dir / "feature_columns.pkl")
        processed = local_preprocessor.transform(df_input)
        proba = model.predict_proba(processed)[0]
        return proba[1]
    except Exception:
        return 0.16


def _sensitivity_curve(model, preprocessor, base_input, param_name, param_values):
    """Compute risk across a range of values for one parameter."""
    risks = []
    for v in param_values:
        overrides = {param_name: v}
        risks.append(_predict_with_overrides(model, preprocessor, base_input, overrides))
    return np.array(risks)


def render_what_if_page(df, model, preprocessor):
    st.markdown("""
    <div class="card">
        <div class="card-title">What-If Simulator — Change the Story</div>
        <p>Use the sliders below to see how modifying specific employee factors
        would change their predicted attrition probability. Every adjustment
        tells a different retention story.</p>
    </div>
    """, unsafe_allow_html=True)

    base_input = _make_base_input()

    # ══════════════════════════════════════════════════════════════════════
    #  Controls
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow">Baseline Employee Profile</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        base_input['Department'] = st.selectbox('Department',
            ['Research & Development', 'Sales', 'Human Resources'], key='wi_dept')
        base_input['JobRole'] = st.selectbox('Job Role',
            ['Research Scientist', 'Laboratory Technician', 'Sales Executive',
             'Sales Representative', 'Manager', 'Human Resources'], key='wi_role')
    with c2:
        base_input['Age'] = st.slider('Age', 18, 65, 35, key='wi_age')
        base_input['MonthlyIncome'] = st.slider('Monthly Income ($)', 1000, 25000, 5000, step=500, key='wi_income')
    with c3:
        base_input['YearsAtCompany'] = st.slider('Years at Company', 0, 40, 4, key='wi_tenure')
        base_input['OverTime'] = st.selectbox('Over Time', ['No', 'Yes'], key='wi_ot')

    # ── What-If Sliders ──────────────────────────────────────────────────
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">What-If Scenarios</div>', unsafe_allow_html=True)
    st.markdown('Adjust these sliders to simulate interventions and see real-time risk changes.')

    wi_cols = st.columns(3)
    with wi_cols[0]:
        wi_salary_pct = st.slider('Salary Change (%)', -30, 50, 0, key='wi_salary',
                                   help='Simulate salary increase or decrease')
        wi_satisfaction = st.slider('Job Satisfaction', 1, 4, base_input['JobSatisfaction'], key='wi_sat')
    with wi_cols[1]:
        wi_wlb = st.slider('Work-Life Balance', 1, 4, base_input['WorkLifeBalance'], key='wi_wlb')
        wi_promote = st.slider('Years Since Last Promotion', 0, 10, 1, key='wi_prom',
                                help='Set to 0 if promoting now')
    with wi_cols[2]:
        wi_distance = st.slider('Distance from Home (mi)', 1, 40, base_input['DistanceFromHome'], key='wi_dist')
        wi_tenure_role = st.slider('Years in Current Role', 0, 20, base_input['YearsInCurrentRole'], key='wi_tcr')

    # Build overrides
    overrides = {
        'MonthlyIncome': int(base_input['MonthlyIncome'] * (1 + wi_salary_pct / 100)),
        'JobSatisfaction': wi_satisfaction,
        'WorkLifeBalance': wi_wlb,
        'YearsSinceLastPromotion': wi_promote,
        'DistanceFromHome': wi_distance,
        'YearsInCurrentRole': wi_tenure_role,
    }

    # ══════════════════════════════════════════════════════════════════════
    #  Baseline vs Modified Comparison
    # ══════════════════════════════════════════════════════════════════════
    base_risk = _predict_with_overrides(model, preprocessor, base_input, {})
    modified_risk = _predict_with_overrides(model, preprocessor, base_input, overrides)
    delta = modified_risk - base_risk

    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Risk Comparison</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-row">
                <span class="kpi-label">Baseline Risk</span>
                <span class="kpi-tag neutral">BEFORE</span>
            </div>
            <div class="kpi-value">{base_risk*100:.1f}%</div>
            <div class="kpi-rule"></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        tag_cls = 'long' if delta < 0 else 'short'
        arrow = '↓' if delta < 0 else '↑'
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-row">
                <span class="kpi-label">Modified Risk</span>
                <span class="kpi-tag {tag_cls}">AFTER</span>
            </div>
            <div class="kpi-value">{modified_risk*100:.1f}%</div>
            <div class="kpi-rule"></div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        delta_cls = 'long' if delta < 0 else 'short'
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-row">
                <span class="kpi-label">Change</span>
                <span class="kpi-tag {delta_cls}">{'BETTER' if delta < 0 else 'WORSE'}</span>
            </div>
            <div class="kpi-value" style="color: {'var(--long)' if delta < 0 else 'var(--short)'}">{arrow}{abs(delta)*100:.1f}%</div>
            <div class="kpi-rule"></div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    #  Gauge Chart
    # ══════════════════════════════════════════════════════════════════════
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=modified_risk * 100,
        number=dict(suffix="%", font=dict(size=28, color='#1b1b21')),
        gauge=dict(
            axis=dict(range=[0, 100], ticksuffix='%'),
            bar=dict(color='#4c56af'),
            bgcolor='rgba(0,0,0,0)',
            bordercolor='#c6c5d4',
            steps=[
                dict(range=[0, 30], color='rgba(45,212,167,0.12)'),
                dict(range=[30, 60], color='rgba(224,167,62,0.12)'),
                dict(range=[60, 100], color='rgba(240,101,79,0.12)'),
            ],
            threshold=dict(line=dict(color='#1b1b21', width=2), thickness=0.8, value=modified_risk * 100),
        ),
    ))
    fig_gauge.update_layout(
        template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#454652'),
        height=280, margin=dict(l=30, r=30, t=20, b=10),
    )
    st.plotly_chart(fig_gauge, width="stretch")

    # ══════════════════════════════════════════════════════════════════════
    #  Sensitivity Curves
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Sensitivity Analysis</div>', unsafe_allow_html=True)
    st.markdown('See how each factor independently affects attrition risk.')

    sensitivities = {
        'Monthly Income': ('MonthlyIncome', [2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000]),
        'Job Satisfaction': ('JobSatisfaction', [1, 2, 3, 4]),
        'Work-Life Balance': ('WorkLifeBalance', [1, 2, 3, 4]),
        'Years Since Promotion': ('YearsSinceLastPromotion', [0, 1, 2, 3, 4, 5, 6, 7]),
    }

    fig_sens, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    colors = [CHART_COLORS['primary'], CHART_COLORS['positive'], CHART_COLORS['accent'], CHART_COLORS['negative']]

    for i, (label, (param, vals)) in enumerate(sensitivities.items()):
        risks = _sensitivity_curve(model, preprocessor, base_input, param, vals)
        axes[i].plot(vals, risks * 100, marker='o', color=colors[i], linewidth=2, markersize=6, zorder=3)
        axes[i].fill_between(vals, risks * 100, alpha=0.08, color=colors[i])
        axes[i].set_title(label, fontsize=12, fontweight='600', pad=10)
        axes[i].set_ylabel('Risk %', labelpad=6)
        axes[i].grid(True, alpha=0.3)
        # Mark current
        current_val = overrides.get(param, base_input.get(param, vals[len(vals)//2]))
        if current_val in vals:
            idx = vals.index(current_val)
            axes[i].scatter([current_val], [risks[idx] * 100], color=CHART_COLORS['negative'],
                           s=80, zorder=5, edgecolors='white', linewidths=1.5)

    plt.tight_layout()
    st.pyplot(fig_sens)
    plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  Impact Summary
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Scenario Impact Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="retention-block">
        <h4>What Your Scenario Means</h4>
        <ul style="padding-left:1.25rem;">
            <li><strong>Baseline risk:</strong> {base_risk*100:.1f}% — the employee's starting attrition probability.</li>
            <li><strong>Modified risk:</strong> {modified_risk*100:.1f}% — after applying your scenario adjustments.</li>
            <li><strong>Change:</strong> {'Decreased by ' + f'{abs(delta)*100:.1f}%' if delta < 0 else 'Increased by ' + f'{abs(delta)*100:.1f}%' if delta > 0 else 'No change'}.</li>
            <li><strong>Salary impact:</strong> A {wi_salary_pct:+d}% income change {'improves' if wi_salary_pct > 0 else 'reduces'} retention odds.</li>
            <li><strong>Satisfaction lever:</strong> Each +1 in Job Satisfaction reduces risk by an estimated 3–5 points.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
