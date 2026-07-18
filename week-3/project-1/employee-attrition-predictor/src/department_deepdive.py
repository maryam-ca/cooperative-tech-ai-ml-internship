"""
Department Deep-Dive Module - Prompt 5
Specialized analysis for R&D department with detailed employee profiles,
cross-team comparison, and department-specific retention recommendations.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.preprocessor import DataPreprocessor
import joblib
from pathlib import Path


CHART_COLORS = {
    'primary': '#6f7bf0',
    'secondary': '#b3bafa',
    'positive': '#2dd4a7',
    'negative': '#f0654f',
    'neutral': '#4b5468',
    'accent': '#e0a73e',
}

TARGET_DEPT = 'Research & Development'


def _score_dept(df, model, preprocessor):
    """Score all R&D employees."""
    dept_df = df[df['Department'] == TARGET_DEPT].copy()
    feature_cols = list(preprocessor.feature_columns)
    df_model = dept_df.reindex(columns=feature_cols, fill_value=0)
    dept_df['AttritionProbability'] = model.predict_proba(df_model)[:, 1]
    dept_df['RiskTier'] = pd.cut(
        dept_df['AttritionProbability'],
        bins=[-0.01, 0.3, 0.6, 1.0],
        labels=['Low', 'Medium', 'High'],
    )
    return dept_df


def _role_breakdown(dept_df):
    return (
        dept_df.groupby('JobRole')
        .agg(
            Count=('Attrition', 'count'),
            AvgRisk=('AttritionProbability', 'mean'),
            MedianIncome=('MonthlyIncome', 'median'),
            AvgTenure=('YearsAtCompany', 'mean'),
            AvgSatisfaction=('JobSatisfaction', 'mean'),
            HighPct=('RiskTier', lambda x: (x == 'High').mean() * 100),
            ActualAttrition=('Attrition', lambda x: (x == 'Yes').sum()),
        )
        .reset_index()
        .sort_values('AvgRisk', ascending=False)
    )


def _tenure_risk_profile(dept_df):
    bins = [0, 2, 5, 10, 20, 40]
    labels = ['0-2 yrs', '3-5 yrs', '6-10 yrs', '11-20 yrs', '20+ yrs']
    dept_df = dept_df.copy()
    dept_df['TenureBucket'] = pd.cut(dept_df['YearsAtCompany'], bins=bins, labels=labels)
    return (
        dept_df.groupby('TenureBucket', observed=False)
        .agg(Count=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'))
        .reset_index()
    )


def _age_risk_profile(dept_df):
    bins = [18, 25, 35, 45, 55, 65]
    labels = ['18-25', '26-35', '36-45', '46-55', '56+']
    dept_df = dept_df.copy()
    dept_df['AgeBucket'] = pd.cut(dept_df['Age'], bins=bins, labels=labels)
    return (
        dept_df.groupby('AgeBucket', observed=False)
        .agg(Count=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'))
        .reset_index()
    )


def _income_distribution(dept_df):
    return dept_df.groupby('JobRole').agg(
        Q25=('MonthlyIncome', lambda x: x.quantile(0.25)),
        Median=('MonthlyIncome', 'median'),
        Q75=('MonthlyIncome', lambda x: x.quantile(0.75)),
    ).reset_index()


def _driver_analysis(dept_df):
    high = dept_df[dept_df['RiskTier'] == 'High']
    total_high = len(high)
    if total_high == 0:
        return pd.DataFrame()
    drivers = {
        'Over Time': (high['OverTime'] == 'Yes').mean() * 100,
        'Low Job Satisfaction (<=2)': (high['JobSatisfaction'] <= 2).mean() * 100,
        'Poor Work-Life Balance (<=2)': (high['WorkLifeBalance'] <= 2).mean() * 100,
        'Short Tenure (< 2 yrs)': (high['YearsAtCompany'] <= 2).mean() * 100,
        'No Recent Promotion (>=3 yrs)': (high['YearsSinceLastPromotion'] >= 3).mean() * 100,
        'Below Median Income': (high['MonthlyIncome'] < dept_df['MonthlyIncome'].median()).mean() * 100,
        'Long Commute (>15 mi)': (high['DistanceFromHome'] > 15).mean() * 100,
    }
    return pd.DataFrame({'Driver': drivers.keys(), 'PctHighRisk': drivers.values()}).sort_values('PctHighRisk', ascending=False)


def _retention_recommendations(dept_df, role_breakdown):
    recommendations = []
    avg_ot = (dept_df['OverTime'] == 'Yes').mean() * 100
    avg_sat = dept_df['JobSatisfaction'].mean()
    avg_wlb = dept_df['WorkLifeBalance'].mean()
    avg_tenure = dept_df['YearsAtCompany'].mean()
    avg_promo_wait = dept_df['YearsSinceLastPromotion'].mean()

    if avg_ot > 30:
        recommendations.append(('Overtime Reduction', f'{avg_ot:.0f}% of R&D works overtime — implement workload audit and redistribute tasks.', 'high'))
    elif avg_ot > 15:
        recommendations.append(('Overtime Monitoring', f'{avg_ot:.0f}% overtime rate — monitor and set quarterly reviews.', 'medium'))

    if avg_sat < 2.5:
        recommendations.append(('Engagement Initiative', f'Average satisfaction is {avg_sat:.2f}/4 — launch career development and mentorship programs.', 'high'))

    if avg_wlb < 2.5:
        recommendations.append(('Work-Life Balance', f'Average WLB score is {avg_wlb:.2f}/4 — introduce flexible hours and remote work options.', 'high'))

    if avg_promo_wait > 3:
        recommendations.append(('Promotion Pathway', f'Average time since last promotion is {avg_promo_wait:.1f} years — create clear advancement tracks.', 'high'))

    # Role-specific
    top_risk_role = role_breakdown.iloc[0]
    recommendations.append((
        f'Focus: {top_risk_role["JobRole"]}',
        f'{top_risk_role["JobRole"]} has the highest risk at {top_risk_role["AvgRisk"]*100:.1f}% — prioritize retention actions for this group.',
        'high' if top_risk_role['AvgRisk'] > 0.3 else 'medium',
    ))

    if avg_tenure < 3:
        recommendations.append(('Early Tenure Support', f'Average tenure is {avg_tenure:.1f} years — strengthen onboarding and early-career programs.', 'medium'))

    return recommendations


def render_department_deepdive_page(df, model, preprocessor):
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Department Deep-Dive — {TARGET_DEPT}</div>
        <p>Specialized analysis of the R&D department: employee profiles,
        cross-team risk comparison, and tailored retention strategies.</p>
    </div>
    """, unsafe_allow_html=True)

    dept_df = _score_dept(df, model, preprocessor)
    total = len(dept_df)
    high = (dept_df['RiskTier'] == 'High').sum()
    med = (dept_df['RiskTier'] == 'Medium').sum()
    avg_risk = dept_df['AttritionProbability'].mean() * 100
    actual_attrition = (dept_df['Attrition'] == 'Yes').sum()
    avg_income = dept_df['MonthlyIncome'].median()

    # ══════════════════════════════════════════════════════════════════════
    #  KPIs
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="eyebrow">{TARGET_DEPT} — Key Metrics</div>', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    for col, (lbl, val, tag, cls) in zip(
        [c1, c2, c3, c4, c5],
        [
            ('Headcount', f'{total}', 'TOTAL', 'neutral'),
            ('High Risk', f'{high}', 'SHORT', 'short'),
            ('Medium Risk', f'{med}', 'WATCH', 'neutral'),
            ('Avg Risk', f'{avg_risk:.1f}%', 'DEPT', 'short' if avg_risk > 25 else 'long'),
            ('Median Income', f'${avg_income:,.0f}', 'INCOME', 'neutral'),
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

    # ══════════════════════════════════════════════════════════════════════
    #  ROLE BREAKDOWN
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Risk by Role within {TARGET_DEPT}</div>', unsafe_allow_html=True)
    rb = _role_breakdown(dept_df)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: avg risk by role
    norm = (rb['AvgRisk'] - rb['AvgRisk'].min()) / max(rb['AvgRisk'].max() - rb['AvgRisk'].min(), 0.001)
    base = np.array([240, 101, 79]) / 255.0
    cols = [(base[0], base[1], base[2], 0.3 + 0.7 * n) for n in norm]
    axes[0].barh(rb['JobRole'], rb['AvgRisk'] * 100, color=cols, height=0.55, zorder=3)
    axes[0].set_xlabel('Avg Risk %', labelpad=8)
    axes[0].set_title('Average Attrition Risk by Role', fontsize=13, fontweight='600', pad=14)
    for i, (_, r) in enumerate(rb.iterrows()):
        axes[0].text(r['AvgRisk'] * 100 + 0.3, i, f"{r['AvgRisk']*100:.1f}%", va='center',
                     fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')

    # Right: headcount vs high-risk %
    axes[1].bar(rb['JobRole'], rb['Count'], color=CHART_COLORS['primary'], alpha=0.3, zorder=3, label='Headcount')
    ax2 = axes[1].twinx()
    ax2.plot(rb['JobRole'], rb['HighPct'], color=CHART_COLORS['negative'], marker='o', linewidth=2, label='% High Risk')
    axes[1].set_ylabel('Headcount', labelpad=8, color='#8993a8')
    ax2.set_ylabel('% High Risk', labelpad=8, color='#8993a8')
    axes[1].set_title('Team Size vs Risk Concentration', fontsize=13, fontweight='600', pad=14)
    axes[1].tick_params(axis='x', rotation=25)
    axes[1].legend(loc='upper left', fontsize=8)
    ax2.legend(loc='upper right', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  TENURE & AGE PROFILES
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Demographic Risk Profiles</div>', unsafe_allow_html=True)

    tab_tenure, tab_age, tab_income = st.tabs(['Tenure Profile', 'Age Profile', 'Income Distribution'])

    with tab_tenure:
        tb = _tenure_risk_profile(dept_df)
        fig_t, ax_t = plt.subplots(figsize=(10, 4))
        ax_t.bar(tb['TenureBucket'].astype(str), tb['Count'], color=CHART_COLORS['primary'], alpha=0.3, zorder=3)
        ax2 = ax_t.twinx()
        ax2.plot(tb['TenureBucket'].astype(str), tb['AvgRisk'] * 100, color=CHART_COLORS['negative'],
                 marker='o', linewidth=2.5, zorder=5)
        ax_t.set_ylabel('Headcount', labelpad=8, color='#8993a8')
        ax2.set_ylabel('Avg Risk %', labelpad=8, color='#8993a8')
        ax_t.set_title('Risk by Tenure', fontsize=13, fontweight='600', pad=14)
        plt.tight_layout()
        st.pyplot(fig_t)
        plt.close()

    with tab_age:
        ab = _age_risk_profile(dept_df)
        fig_a, ax_a = plt.subplots(figsize=(10, 4))
        ax_a.bar(ab['AgeBucket'].astype(str), ab['Count'], color=CHART_COLORS['accent'], alpha=0.3, zorder=3)
        ax2 = ax_a.twinx()
        ax2.plot(ab['AgeBucket'].astype(str), ab['AvgRisk'] * 100, color=CHART_COLORS['negative'],
                 marker='s', linewidth=2.5, zorder=5)
        ax_a.set_ylabel('Headcount', labelpad=8, color='#8993a8')
        ax2.set_ylabel('Avg Risk %', labelpad=8, color='#8993a8')
        ax_a.set_title('Risk by Age Group', fontsize=13, fontweight='600', pad=14)
        plt.tight_layout()
        st.pyplot(fig_a)
        plt.close()

    with tab_income:
        inc = _income_distribution(dept_df)
        fig_i, ax_i = plt.subplots(figsize=(10, 4))
        x = np.arange(len(inc))
        ax_i.bar(x - 0.15, inc['Q25'], 0.3, label='25th pctl', color=CHART_COLORS['positive'], alpha=0.6, zorder=3)
        ax_i.bar(x, inc['Median'], 0.3, label='Median', color=CHART_COLORS['primary'], zorder=3)
        ax_i.bar(x + 0.15, inc['Q75'], 0.3, label='75th pctl', color=CHART_COLORS['accent'], alpha=0.6, zorder=3)
        ax_i.set_xticks(x)
        ax_i.set_xticklabels(inc['JobRole'], rotation=25, ha='right')
        ax_i.set_ylabel('Monthly Income ($)', labelpad=8)
        ax_i.set_title('Income Distribution by Role', fontsize=13, fontweight='600', pad=14)
        ax_i.legend(fontsize=8)
        ax_i.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
        plt.tight_layout()
        st.pyplot(fig_i)
        plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  DRIVER ANALYSIS
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">Root Cause Analysis — R&D</div>', unsafe_allow_html=True)
    drivers = _driver_analysis(dept_df)

    fig_d, ax_d = plt.subplots(figsize=(10, 4.5))
    norm_d = (drivers['PctHighRisk'] - drivers['PctHighRisk'].min()) / max(drivers['PctHighRisk'].max() - drivers['PctHighRisk'].min(), 0.001)
    base_d = np.array([240, 101, 79]) / 255.0
    cols_d = [(base_d[0], base_d[1], base_d[2], 0.3 + 0.7 * n) for n in norm_d]
    ax_d.barh(drivers['Driver'], drivers['PctHighRisk'], color=cols_d, height=0.55, zorder=3)
    ax_d.set_xlabel('% of High-Risk R&D Employees', labelpad=8)
    ax_d.set_title('Risk Drivers in R&D Department', fontsize=13, fontweight='600', pad=14)
    ax_d.invert_yaxis()
    for bar, val in zip(ax_d.patches, drivers['PctHighRisk']):
        ax_d.text(val + 0.8, bar.get_y() + bar.get_height() / 2, f'{val:.0f}%',
                  va='center', fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')
    plt.tight_layout()
    st.pyplot(fig_d)
    plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  TOP 15 EMPLOYEE PROFILES
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Top 15 At-Risk R&D Employees</div>', unsafe_allow_html=True)
    top15 = dept_df.nlargest(15, 'AttritionProbability')
    show_cols = ['Age', 'JobRole', 'MonthlyIncome', 'YearsAtCompany', 'OverTime',
                 'JobSatisfaction', 'WorkLifeBalance', 'YearsSinceLastPromotion', 'AttritionProbability']
    existing = [c for c in show_cols if c in top15.columns]
    st.dataframe(
        top15[existing], use_container_width=True, height=450,
        column_config={'AttritionProbability': st.column_config.ProgressColumn('Risk', format='%.1f%%', min_value=0, max_value=1)},
    )

    # ══════════════════════════════════════════════════════════════════════
    #  CROSS-DEPARTMENT COMPARISON
    # ══════════════════════════════════════════════════════════════════════
    st.markdown('<div class="eyebrow" style="margin-top:2rem;">How R&D Compares to Other Departments</div>', unsafe_allow_html=True)
    all_scored = df.copy()
    feature_cols = list(preprocessor.feature_columns)
    df_model = all_scored.reindex(columns=feature_cols, fill_value=0)
    all_scored['AttritionProbability'] = model.predict_proba(df_model)[:, 1]

    dept_comp = (
        all_scored.groupby('Department')
        .agg(Headcount=('Attrition', 'count'), AvgRisk=('AttritionProbability', 'mean'))
        .reset_index()
    )
    dept_comp['IsTarget'] = dept_comp['Department'] == TARGET_DEPT

    fig_c, ax_c = plt.subplots(figsize=(10, 4))
    bar_colors = [CHART_COLORS['primary'] if is_t else CHART_COLORS['neutral'] for is_t in dept_comp['IsTarget']]
    ax_c.bar(dept_comp['Department'], dept_comp['AvgRisk'] * 100, color=bar_colors, zorder=3)
    ax_c.set_ylabel('Avg Risk %', labelpad=8)
    ax_c.set_title('Average Risk by Department (R&D Highlighted)', fontsize=13, fontweight='600', pad=14)
    for i, (_, r) in enumerate(dept_comp.iterrows()):
        ax_c.text(i, r['AvgRisk'] * 100 + 0.3, f"{r['AvgRisk']*100:.1f}%", ha='center',
                  fontweight='600', color='#e4e9f2', fontsize=9, fontfamily='monospace')
    plt.tight_layout()
    st.pyplot(fig_c)
    plt.close()

    # ══════════════════════════════════════════════════════════════════════
    #  RETENTION RECOMMENDATIONS
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Retention Strategy — {TARGET_DEPT}</div>', unsafe_allow_html=True)
    recs = _retention_recommendations(dept_df, rb)

    for title, detail, priority in recs:
        p_color = CHART_COLORS['negative'] if priority == 'high' else CHART_COLORS['accent']
        p_label = 'HIGH' if priority == 'high' else 'MEDIUM'
        st.markdown(f"""
        <div class="insight-block" style="border-left-color: {p_color};">
            <h4 style="color: {p_color};">
                {title}
                <span style="float:right; font-size:0.6rem; letter-spacing:0.08em; padding:0.1rem 0.4rem;
                             border-radius:3px; background:rgba({','.join(str(int(c)) for c in ([240,101,79] if priority=='high' else [224,167,62]))},0.15);">
                    {p_label}
                </span>
            </h4>
            <p style="font-size:0.875rem; color: var(--ink-text-dim);">{detail}</p>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════
    #  DOWNLOAD
    # ══════════════════════════════════════════════════════════════════════
    st.markdown(f'<div class="eyebrow" style="margin-top:2rem;">Export {TARGET_DEPT} Report</div>', unsafe_allow_html=True)
    export_cols = ['Age', 'JobRole', 'MonthlyIncome', 'YearsAtCompany', 'OverTime',
                   'JobSatisfaction', 'WorkLifeBalance', 'YearsSinceLastPromotion',
                   'AttritionProbability', 'RiskTier']
    export_existing = [c for c in export_cols if c in dept_df.columns]
    csv = dept_df[export_existing].to_csv(index=False)
    st.download_button(
        f'Download {TARGET_DEPT} Risk Report (CSV)',
        data=csv,
        file_name='rd_department_risk_report.csv',
        mime='text/csv',
    )
