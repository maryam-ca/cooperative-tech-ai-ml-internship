"""
Lumina Insights — Employee Attrition Predictor
A glassmorphism re-skin of the Streamlit dashboard. Analytical navy ->
predictive purple (Material 3). Live model evaluation, real predictions,
analytics, and advanced stakeholder views.
"""

import sys
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parent
sys.path.append(str(ROOT))

from src.ui_components import (
    ensure_assets,
    icon,
    eyebrow,
    page_header,
    status_chip,
    kpi_card,
    bar_row,
    cm_grid,
    lumina_table,
    load_config,
    save_config,
    DATA_FILE,
    load_cached_data,
    load_pipeline,
    artifact_mtime,
    model_type_label,
    risk_tier,
    risk_chip,
    score_dataframe,
    COLORS,
)
from src import charts
from src import eval_utils
from src.preprocessor import DataPreprocessor

from src.storytelling import render_storytelling_page
from src.multi_stakeholder import render_multi_stakeholder_page
from src.what_if_simulator import render_what_if_page
from src.time_travel import render_time_travel_page
from src.department_deepdive import render_department_deepdive_page

st.set_page_config(
    page_title="Lumina Insights · Employee Attrition",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

ensure_assets()

CORE_NAV = [
    "Dashboard",
    "Prediction Tool",
    "Analytics",
    "Reports",
    "Settings",
]
ADV_NAV = [
    "Data Explorer",
    "EDA Visualizations",
    "Storytelling & Early Warning",
    "Multi-Stakeholder Views",
    "What-If Simulator",
    "Time-Travel Analysis",
    "R&D Deep-Dive",
]
RESOURCES = {
    "Codex": ("https://openai.com", "companion code", "g_automation"),
    "Gemini": ("https://gemini.google.com", "parallel thinking", "auto_awesome"),
    "GitLab": (
        "https://github.com/Samra-ca/employee-attrition-predictor",
        "version control",
        "cloud_queue",
    ),
}


def build_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand">'
            '<div class="brand-avatar">' + icon("visible", size=22) + "</div>"
            '<div><div class="brand-title">Lumina</div>'
            '<div class="brand-sub">Insights Dashboard</div></div>'
            "</div>",
            unsafe_allow_html=True,
        )

        def _cb_core():
            st.session_state["_nav_origin"] = "core"

        def _cb_adv():
            st.session_state["_nav_origin"] = "adv"

        st.markdown('<div class="sidebar-section-label">Analytics</div>', unsafe_allow_html=True)
        core = st.radio(
            "Primary navigation",
            CORE_NAV,
            key="nav_core",
            on_change=_cb_core,
            label_visibility="collapsed",
        )
        st.markdown('<div class="sidebar-section-label">Workbench</div>', unsafe_allow_html=True)
        adv = st.radio(
            "Advanced navigation",
            ADV_NAV,
            key="nav_adv",
            on_change=_cb_adv,
            label_visibility="collapsed",
        )

        origin = st.session_state.get("_nav_origin", "core")
        active = core if origin == "core" else adv

        st.markdown('<div class="sidebar-section-label">Linked digital resources</div>', unsafe_allow_html=True)
        resources_html = "".join(
            f'<div style="padding:6px 24px;display:flex;align-items:center;gap:10px;'
            f'font-size:0.85rem;">{icon(ic, size=18)}'
            f'<a href="{url}" target="_blank">{name}</a></div>'
            for name, (url, _hint, ic) in RESOURCES.items()
        )
        st.markdown(resources_html, unsafe_allow_html=True)

        meta = eval_utils.load_metadata()
        trained = (meta.get("trained_at") or "after first run")[:10]
        st.markdown("---")
        st.markdown(
            '<div class="sidebar-footer">'
            '<div class="sidebar-footer-item">'
            f'<span class="sf-label">Model:</span> '
            f'<span class="sf-value">{meta.get("algorithm", "Logistic Regression")}</span>'
            "</div>"
            '<div class="sidebar-footer-item">'
            '<span class="sf-label">Refreshed:</span> '
            f'<span class="sf-value">{trained}</span>'
            "</div>"
            '<div class="sidebar-footer-item">'
            '<span class="sf-value">IBM HR Analytics · 1,470 records</span>'
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    return active


def render_topbar(title: str, subtitle: str = ""):
    sub_html = (
        f'<span style="opacity:0.5;margin-left:10px;font-size:0.85em;">{subtitle}</span>'
        if subtitle else ""
    )
    st.markdown(
        f'<div class="lumina-topbar">'
        f'<div class="tb-title">{icon("auto_awesome", size=22)}&nbsp;Lumina Insights</div>'
        f'<div style="font-family:var(--lumina-font-display);font-size:var(--lumina-label-md);'
        f'font-weight:500;color:var(--lumina-on-surface-variant);letter-spacing:0.03em;">'
        f'{title}{sub_html}</div>'
        f'<div class="tb-icons">'
        f'<div class="tb-icon-btn">{icon("notifications")}<span class="dot"></span></div>'
        f'<div class="tb-icon-btn tb-search-hide">{icon("help")}</div>'
        f'<div class="tb-icon-btn tb-search-hide">{icon("settings")}</div>'
        f"</div></div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════
#  Dashboard
# ═══════════════════════════════════════════════════════════════════════
def show_dashboard():
    df = load_cached_data(DATA_FILE.stat().st_mtime)
    model, pre = eval_utils.ensure_deployed()
    eval_res = eval_utils.compute_evaluation(artifact_mtime())
    scored = score_dataframe(df, model, pre)
    cfg = load_config()

    total = int(len(df))
    high = int((scored["RiskTier"] == "High").sum())
    medium = int((scored["RiskTier"] == "Medium").sum())
    rate = float((df["Attrition"] == "Yes").mean() * 100)
    accuracy = eval_res["metrics"]["accuracy"] * 100

    role_counts = df.groupby("JobRole").size()
    dept_counts = df.groupby("Department").size()
    dept_rate = df.groupby("Department")["Attrition"].apply(lambda s: (s == "Yes").mean() * 100)
    imp = eval_res["importance"][:8]

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(
        kpi_card(
            "Employees", f"{total:,}", icon_name="group", ic_class="ic-tint",
            delta="workforce", delta_kind="neutral", delta_icon="groups",
            sparkline=charts.sparkline_svg(list(role_counts.sort_values(ascending=False).values)),
        ),
        unsafe_allow_html=True,
    )
    k2.markdown(
        kpi_card(
            "At-risk now", f"{high:,}", icon_name="warning", ic_class="ic-mid",
            delta=f"+{medium} watchlist", delta_kind="bad", delta_icon="notifications_active",
            sparkline=charts.sparkline_svg(list(dept_counts.values), color=COLORS["risk_mid"]),
        ),
        unsafe_allow_html=True,
    )
    k3.markdown(
        kpi_card(
            "Attrition rate", f"{rate:.1f}%", icon_name="trending_up", ic_class="ic-error",
            delta="12-mo view", delta_kind="neutral", delta_icon="calendar_today",
            sparkline=charts.sparkline_svg(list(dept_rate.sort_values(ascending=False).values), color=COLORS["risk_high"]),
        ),
        unsafe_allow_html=True,
    )
    k4.markdown(
        kpi_card(
            "Model accuracy", f"{accuracy:.1f}%", icon_name="tune", ic_class="ic-primary",
            delta=f"AUC {eval_res['metrics']['roc_auc']:.2f}", delta_kind="good", delta_icon="trending_up",
            sparkline=charts.sparkline_svg([v["value"] for v in imp], color=COLORS["primary"]),
        ),
        unsafe_allow_html=True,
    )

    st.markdown(eyebrow("Risk snapshot"), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.6])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(
            charts.donut(
                ["High", "Medium", "Low"],
                [high, medium, total - high - medium],
                title="Predicted risk distribution",
            ),
            width="stretch",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        d = pd.DataFrame(
            {
                "Department": dept_rate.index,
                "Attrition %": dept_rate.values,
                "Headcount": dept_counts.reindex(dept_rate.index).values,
            }
        ).sort_values("Attrition %", ascending=False)
        st.plotly_chart(
            charts.hbar(d, "Attrition %", "Department", title="Attrition rate by department", height=260, marker_color=COLORS["risk_high"]),
            width="stretch",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        top = scored.sort_values("AttritionProbability", ascending=False).head(5)
        rows = [
            [
                int(r.EmployeeNumber),
                r.Department,
                r.JobRole,
                risk_chip(float(r.AttritionProbability), cfg),
                f"{r.AttritionProbability * 100:.1f}%",
            ]
            for r in top.itertuples()
        ]
        st.markdown(
            lumina_table(
                ["ID", "Department", "Role", "Tier", "P(churn)"], rows,
                aligns=["", "", "", "center", "right"],
            ),
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">What&#8217;s moving the model</div>', unsafe_allow_html=True)
        for it in imp[:5]:
            v = abs(it["value"])
            direction = "increases risk" if it["value"] > 0 else "lowers risk"
            st.markdown(
                bar_row(it["feature"], v, direction, fill_class="fill-error" if it["value"] > 0 else "fill-sec"),
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(eyebrow("Bookmarked AI resources"), unsafe_allow_html=True)
    rc = st.columns(3)
    for col, (name, (url, hint, ic)) in zip(rc, RESOURCES.items()):
        col.markdown(
            f'<a href="{url}" target="_blank" style="text-decoration:none;color:inherit;">'
            f'<div class="glass-card">'
            f'<div class="card-title">{icon(ic, size=18)}&nbsp;{name}</div>'
            f'<p style="color:var(--lumina-on-surface-variant);font-size:0.875rem;">{hint} — '
            f"opens in a new tab.</p></div></a>",
            unsafe_allow_html=True,
        )

    with st.expander("How predictions are produced"):
        st.markdown(
            "Raw HR records are cleaned, engineered (tenure ratio, overtime-income ratio, "
            "tenure grouping), encoded with the saved label / one-hot scheme, and scaled with "
            f"the fitted standard scaler. The deployed **{model_type_label(model)}** scores "
            f"all {total:,} employees to power this view."
        )


# ═══════════════════════════════════════════════════════════════════════
#  Prediction tool
# ═══════════════════════════════════════════════════════════════════════
def show_prediction_tool():
    cfg = load_config()
    model, pre = eval_utils.ensure_deployed()

    with st.form(key="predict_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3, gap="medium")
        with c1:
            age = st.number_input("Age", min_value=18, max_value=65, value=30, step=1)
            gender = st.selectbox("Gender", ["Male", "Female"])
            marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            department = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"])
        with c2:
            job_role = st.selectbox(
                "Job Role",
                ["Research Scientist", "Laboratory Technician", "Sales Executive",
                 "Sales Representative", "Manager", "Human Resources"],
            )
            education = st.selectbox(
                "Education Level",
                [1, 2, 3, 4, 5],
                format_func={1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}.get,
            )
            monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=5000, step=500)
            overtime = st.selectbox("Overtime", ["No", "Yes"])
        with c3:
            years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5, step=1)
            total_working_years = st.number_input("Total Working Years", min_value=0, max_value=50, value=10, step=1)
            years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=30, value=3, step=1)
            job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
            wlb = st.slider("Work-Life Balance (1-4)", 1, 4, 3)
            distance = st.number_input("Distance from Home (miles)", min_value=1, max_value=50, value=10, step=1)
            num_companies = st.number_input("Companies Worked", min_value=0, max_value=20, value=2, step=1)

        submitted = st.form_submit_button("Predict attrition risk", width="stretch")

    if submitted:
        data = {
            "Age": age,
            "Gender": gender,
            "MaritalStatus": marital,
            "Department": department,
            "JobRole": job_role,
            "Education": education,
            "MonthlyIncome": monthly_income,
            "YearsAtCompany": years_at_company,
            "OverTime": overtime,
            "TotalWorkingYears": total_working_years,
            "YearsInCurrentRole": years_in_current_role,
            "JobSatisfaction": job_satisfaction,
            "WorkLifeBalance": wlb,
            "DistanceFromHome": distance,
            "NumCompaniesWorked": num_companies,
        }
        try:
            pred, proba, _ = eval_utils.predict_row(data, model, pre)
            factors = eval_utils.row_factor_breakdown(data, model, pre, top_n=6)
        except Exception as exc:
            st.error(f"Prediction failed: {exc}")
            return

        tier = risk_tier(proba, cfg)
        tier_kind = {"High": "high", "Medium": "medium", "Low": "low"}[tier]
        headline = {
            "High": "This employee shows elevated churn signals",
            "Medium": "Moderate churn indicators detected",
            "Low": "Low churn risk — stable engagement",
        }[tier]
        decision = "flagged for retention outreach" if pred == 1 else "no intervention needed"

        st.markdown(eyebrow("Prediction result"), unsafe_allow_html=True)
        st.markdown(
            '<div class="verdict">'
            f'<div class="verdict-strip {tier_kind}"></div>'
            '<div class="verdict-body"><div>'
            f'<div class="verdict-label {tier_kind}">{tier} risk</div>'
            f'<div class="verdict-headline">{headline}</div>'
            f'<div class="verdict-sub">Model decision: {decision}.</div>'
            "</div>"
            f'<div class="verdict-figure {tier_kind}"><div class="num">{proba * 100:.1f}%</div>'
            '<div class="figcap">P(attrition)</div></div>'
            "</div></div>",
            unsafe_allow_html=True,
        )

        cL, cR = st.columns([1.3, 1])
        with cL:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Why this score</div>', unsafe_allow_html=True)
            for f in factors[:5]:
                direction = "raises risk" if f["value"] > 0 else "lowers risk"
                st.markdown(
                    bar_row(f["feature"], min(abs(f["value"]), 1.0), direction,
                            fill_class="fill-error" if f["value"] > 0 else "fill-sec"),
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        with cR:
            actions = [
                ("restore", "Reduce mandatory overtime for 2 quarters"),
                ("favorite", "Schedule engagement check-in with manager"),
                ("balance", "Review workload and work-life balance plan"),
                ("payments", "Benchmark compensation against market band"),
                ("school", "Provide growth / promotion roadmap"),
                ("home", "Consider hybrid or remote flexibility"),
            ]
            if tier == "High":
                actions = actions[:5]
            elif tier == "Medium":
                actions = actions[:3]

            st.markdown('<div class="glass-card" style="border-left:4px solid var(--lumina-alert);">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Recommended actions</div>', unsafe_allow_html=True)
            for r_ic, txt in actions:
                st.markdown(
                    f'<div style="display:flex;gap:10px;align-items:flex-start;padding:9px 0;'
                    f'font-size:0.9rem;color:var(--lumina-on-surface);">{icon(r_ic, size=18)}<span>{txt}</span></div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        history = st.session_state.setdefault("pred_history", [])
        history.insert(
            0,
            {
                "ts": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "role": job_role,
                "dept": department,
                "prob": round(proba, 4),
                "tier": tier,
            },
        )
        st.session_state["pred_history"] = history[:10]

    history = st.session_state.get("pred_history", [])
    if history:
        st.markdown(eyebrow("Recent predictions"), unsafe_allow_html=True)
        hcols = st.columns(2)
        for i, h in enumerate(history):
            col = hcols[i % 2]
            col.markdown(
                f'<div class="glass-panel" style="padding:12px 16px;display:flex;'
                f'align-items:center;gap:10px;justify-content:space-between;">'
                f'<div><div style="font-size:0.8rem;color:var(--lumina-outline);">{h["ts"]}</div>'
                f'<div style="font-weight:600;">{h["role"]} · {h["dept"]}</div></div>'
                f'{risk_chip(h["prob"], cfg)}'
                f'<span style="font-weight:700;font-variant-numeric:tabular-nums;">{h["prob"] * 100:.1f}%</span></div>',
                unsafe_allow_html=True,
            )
        if st.button("Clear history"):
            st.session_state["pred_history"] = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
#  Analytics
# ═══════════════════════════════════════════════════════════════════════
def show_analytics():
    df = load_cached_data(DATA_FILE.stat().st_mtime)
    model, pre = eval_utils.ensure_deployed()
    eval_res = eval_utils.compute_evaluation(artifact_mtime())
    scored = score_dataframe(df, model, pre)

    c1, c2 = st.columns([1, 1.6])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = go.Figure(
            go.Histogram(
                x=scored["AttritionProbability"],
                nbinsx=24,
                marker=dict(color=COLORS["surface_tint"], line=dict(color="rgba(255,255,255,0.6)", width=1)),
            )
        )
        fig.update_layout(
            **charts.BASE_LAYOUT,
            title=dict(text="Probability distribution", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)),
            yaxis_title="Employees",
            xaxis_title="P(attrition)",
        )
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tier_counts = scored["RiskTier"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)
        st.plotly_chart(
            charts.donut(
                tier_counts.index.tolist(),
                tier_counts.values,
                hole=0.55,
            ),
            width="stretch",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        role_risk = (
            scored.groupby("JobRole")["AttritionProbability"]
            .agg(["mean", "count"])
            .reset_index()
            .sort_values("mean", ascending=False)
        )
        fig = charts.vbar(role_risk, "JobRole", "mean", title="Average predicted risk by role", height=360)
        fig.update_yaxes(tickformat=".0%", ticksuffix=" ")
        st.plotly_chart(fig, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        ot = (
            scored.groupby(["OverTime", "RiskTier"]).size()
            .unstack(fill_value=0)
            .reindex(columns=["High", "Medium", "Low"], fill_value=0)
        )
        ot["Employees"] = ot.sum(axis=1)
        ot = ot.sort_values("Employees", ascending=False)
        st.markdown('<div class="card-title">Overtime vs. predicted risk</div>', unsafe_allow_html=True)
        for otv, row in ot.iterrows():
            st.markdown(
                bar_row(
                    f"Overtime: {otv}",
                    row["Employees"] / ot["Employees"].sum(),
                    f'{int(row["Employees"]):,} · {int(row["High"]):,} high',
                    fill_class="fill-error" if otv == "Yes" else "fill-sec",
                ),
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(eyebrow("Drivers of attrition"), unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        imp = eval_res["importance"][:10]
        st.plotly_chart(
            charts.feature_importance_bars(
                [i["feature"] for i in imp],
                [i["value"] for i in imp],
                title="Feature attribution (deployed model)",
            ),
            width="stretch",
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        contrib = scored.groupby("Department")["RiskTier"].apply(lambda s: (s == "High").mean() * 100).sort_values(ascending=False)
        for idx, v in contrib.items():
            st.markdown(bar_row(idx, v / 100, f"{v:.1f}%", fill_class="fill-error"), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Top at-risk employees (full list)"):
        cols = ["EmployeeNumber", "Department", "JobRole", "OverTime", "MonthlyIncome", "AttritionProbability", "RiskTier"]
        st.dataframe(scored.sort_values("AttritionProbability", ascending=False)[cols].head(25), width="stretch")


# ═══════════════════════════════════════════════════════════════════════
#  Reports
# ═══════════════════════════════════════════════════════════════════════
def show_reports():
    eval_res = eval_utils.compute_evaluation(artifact_mtime())
    met = eval_res["metrics"]
    cm = eval_res["confusion_matrix"]

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.markdown(kpi_card("Accuracy", f'{met["accuracy"] * 100:.1f}%', "check_circle", "ic-primary"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Precision", f'{met["precision"] * 100:.1f}%', "verified", "ic-tint"), unsafe_allow_html=True)
    k3.markdown(kpi_card("Recall", f'{met["recall"] * 100:.1f}%', "target", "ic-mid"), unsafe_allow_html=True)
    k4.markdown(kpi_card("F1 Score", f'{met["f1"] * 100:.1f}%', "rate_review", "ic-sec"), unsafe_allow_html=True)
    k5.markdown(kpi_card("ROC-AUC", f'{met["roc_auc"]:.2f}', "show_chart", "ic-error"), unsafe_allow_html=True)

    st.markdown(eyebrow("Model comparison"), unsafe_allow_html=True)
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        comp = eval_res["comparison"]
        data = {
            "Model": list(comp.keys()) + [f"Deployed ({eval_res['deployed_type']})"],
            "Accuracy": [m["accuracy"] for m in comp.values()] + [met["accuracy"]],
            "Precision": [m["precision"] for m in comp.values()] + [met["precision"]],
            "Recall": [m["recall"] for m in comp.values()] + [met["recall"]],
            "F1 Score": [m["f1"] for m in comp.values()] + [met["f1"]],
            "ROC-AUC": [m["roc_auc"] for m in comp.values()] + [met["roc_auc"]],
        }
        df_comp = pd.DataFrame(data)
        rows = []
        for rec in df_comp.to_dict("records"):
            rows.append(
                [
                    f"<strong>{rec['Model']}</strong>",
                    f"{rec['Accuracy'] * 100:.1f}%",
                    f"{rec['Precision'] * 100:.1f}%",
                    f"{rec['Recall'] * 100:.1f}%",
                    f"{rec['F1 Score'] * 100:.1f}%",
                    f"{rec['ROC-AUC']:.3f}",
                ]
            )
        st.markdown(
            lumina_table(
                ["Model", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
                rows,
                aligns=["", "right", "right", "right", "right", "right"],
            ),
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download comparison (CSV)",
            df_comp.to_csv(index=False).encode("utf-8"),
            file_name="model_comparison.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Confusion matrix</div>', unsafe_allow_html=True)
        st.markdown(cm_grid(int(cm[0][0]), int(cm[0][1]), int(cm[1][0]), int(cm[1][1])), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(eyebrow("Discrimination & drivers"), unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.plotly_chart(
            charts.roc_curve(eval_res["roc"]["fpr"], eval_res["roc"]["tpr"], eval_res["roc"]["auc"]),
            width="stretch", theme=None,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        imp = eval_res["importance"][:10]
        st.plotly_chart(
            charts.feature_importance_bars([i["feature"] for i in imp], [i["value"] for i in imp], title="Feature attribution"),
            width="stretch", theme=None,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Evaluation context"):
        st.markdown(
            f"Evaluated on **{eval_res['n_rows']:,}** scored records — **{eval_res['n_test']:,}** "
            f"held-out test records, **{eval_res['n_pos_test']:,}** actual churn cases in the test set."
        )
        st.dataframe(pd.DataFrame(comp).T, width="stretch")


# ═══════════════════════════════════════════════════════════════════════
#  Settings
# ═══════════════════════════════════════════════════════════════════════
def show_settings():
    from src.ui_components import SENSITIVITY_PRESETS

    cfg = load_config()

    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Risk configuration</div>', unsafe_allow_html=True)
        sensitivity_options = list(SENSITIVITY_PRESETS.keys())
        current_sens = cfg.get("sensitivity", "Balanced")
        sens_index = sensitivity_options.index(current_sens) if current_sens in sensitivity_options else 0
        sensitivity = st.radio("Sensitivity profile", sensitivity_options, index=sens_index, key="cfg_sensitivity")
        default_threshold = SENSITIVITY_PRESETS[sensitivity]
        threshold = st.slider(
            "High-risk threshold (P ≥ value)", 0.30, 0.70,
            float(cfg.get("risk_threshold", default_threshold)), 0.05, key="cfg_threshold",
        )
        low_factor = st.slider(
            "Medium band multiplier", 0.40, 0.90,
            float(cfg.get("low_bound_factor", 0.6)), 0.05, key="cfg_low_factor",
        )

        st.markdown('<div class="card-title" style="margin-top:1.25rem;">Deployed model</div>', unsafe_allow_html=True)
        algorithm = st.radio(
            "Algorithm",
            ["Logistic Regression", "Random Forest"],
            index=["Logistic Regression", "Random Forest"].index(cfg.get("algorithm", "Logistic Regression")),
            key="cfg_algorithm",
        )
        n_trees = 100
        if algorithm == "Random Forest":
            n_trees = st.slider("Trees (Random Forest)", 50, 500, int(cfg.get("n_estimators", 100)), 50)

        if st.button("Save configuration", width="stretch"):
            new_cfg = {
                **cfg,
                "sensitivity": sensitivity if threshold == default_threshold else "Custom",
                "risk_threshold": float(threshold),
                "low_bound_factor": float(low_factor),
                "algorithm": algorithm,
                "n_estimators": int(n_trees),
            }
            save_config(new_cfg)
            st.toast("Configuration saved")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card" style="border-left:4px solid var(--lumina-primary);">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Retrain model</div>', unsafe_allow_html=True)
        meta = eval_utils.load_metadata()
        st.markdown(
            "<p>Retrains on the full dataset with the current algorithm, evaluates on a "
            "held-out split, and replaces the deployed artifacts.</p>"
            f"<p>Current deployment: <strong>{meta.get('algorithm', 'Logistic Regression')}</strong>"
            f" · last trained <strong>{(meta.get('trained_at') or 'unknown')[:19]}</strong></p>",
            unsafe_allow_html=True,
        )
        if st.button("Retrain and deploy", width="stretch", type="primary"):
            with st.spinner("Training on the full dataset…"):
                try:
                    new_meta = eval_utils.retrain_and_save(load_config())
                    st.toast(f"Deployed {new_meta.get('algorithm')} — accuracy "
                             f"{new_meta['performance']['accuracy'] * 100:.1f}%")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Retraining failed: {exc}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">About</div>', unsafe_allow_html=True)
        st.markdown(
            "<p>Lumina Insights — an internship design system applied to the Employee "
            "Attrition Predictor. Built with Streamlit, scikit-learn, pandas and Plotly. "
            "Glass surfaces, analytical-navy to predictive-purple.</p>",
            unsafe_allow_html=True,
        )
        for name, (url, _hint, ic) in RESOURCES.items():
            st.markdown(f'<a href="{url}" target="_blank">{icon(ic, size=14)}&nbsp;{name}</a><br/>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  Data Explorer / EDA
# ═══════════════════════════════════════════════════════════════════════
def show_data_explorer():
    df = load_cached_data(DATA_FILE.stat().st_mtime)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card("Rows", f"{len(df):,}", "table_rows", "ic-primary"), unsafe_allow_html=True)
    k2.markdown(kpi_card("Columns", f"{len(df.columns):,}", "view_column", "ic-tint"), unsafe_allow_html=True)
    missing = int(df.isna().sum().sum())
    k3.markdown(kpi_card("Missing cells", f"{missing:,}", "highlight_off", "ic-error"), unsafe_allow_html=True)
    dups = int(df.duplicated().sum())
    k4.markdown(kpi_card("Duplicate rows", f"{dups:,}", "merge", "ic-mid"), unsafe_allow_html=True)

    st.markdown(eyebrow("Schema"), unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    schema = pd.DataFrame(
        {
            "Column": df.columns,
            "Type": df.dtypes.astype(str).values,
            "Nulls": df.isna().sum().values,
            "Unique": df.nunique().values,
        }
    )
    rows = [[c, t, str(n), str(u)] for c, t, n, u in
            zip(schema["Column"], schema["Type"], schema["Nulls"], schema["Unique"])]
    st.markdown(lumina_table(["Column", "Type", "Nulls", "Unique"], rows, aligns=["", "", "right", "right"]), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Numeric summary</div>', unsafe_allow_html=True)
        st.dataframe(df.describe().T, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Categorical profile</div>', unsafe_allow_html=True)
        cat_columns = df.select_dtypes(include="object").columns.tolist()
        cat_col = st.selectbox("Column", cat_columns)
        vc = df[cat_col].value_counts().head(12).reset_index()
        vc.columns = ["Value", "Records"]
        st.plotly_chart(
            charts.hbar(vc, "Records", "Value", title=f"Value counts — {cat_col}", height=320, marker_color=COLORS["surface_tint"]),
            width="stretch",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "Download dataset (CSV)",
        df.to_csv(index=False).encode("utf-8"),
        file_name="employee_attrition.csv",
        mime="text/csv",
    )


def show_eda_visualizations():
    df = load_cached_data(DATA_FILE.stat().st_mtime)

    tab_dist, tab_rel, tab_corr = st.tabs(["Distributions", "Relationships", "Correlation"])

    with tab_dist:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.plotly_chart(
                charts.donut(
                    df["Attrition"].value_counts().index.tolist(),
                    df["Attrition"].value_counts().values,
                    title="Attrition balance",
                ),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig = px.histogram(df, x="Age", color="Attrition", barmode="overlay", opacity=0.6)
            fig.update_layout(**charts.BASE_LAYOUT, title=dict(text="Age distribution", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)))
            fig.update_xaxes(gridcolor="rgba(198,197,212,0.35)")
            st.plotly_chart(fig, width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig = px.box(df, x="Attrition", y="MonthlyIncome", color="Attrition")
            fig.update_layout(**charts.BASE_LAYOUT, title=dict(text="Income vs attrition", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)), showlegend=False)
            st.plotly_chart(fig, width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig = px.histogram(df, x="YearsAtCompany", color="Attrition", barmode="overlay", opacity=0.6)
            fig.update_layout(**charts.BASE_LAYOUT, title=dict(text="Tenure distribution", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)))
            fig.update_xaxes(gridcolor="rgba(198,197,212,0.35)")
            st.plotly_chart(fig, width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_rel:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            rate_by_ot = df.groupby("OverTime")["Attrition"].apply(lambda s: (s == "Yes").mean() * 100).reset_index()
            st.plotly_chart(
                charts.hbar(rate_by_ot, "Attrition", "OverTime", title="Attrition rate by overtime", height=280, marker_color=COLORS["risk_high"]),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig = px.scatter(df, x="MonthlyIncome", y="JobSatisfaction", color="Attrition", size="YearsAtCompany")
            fig.update_layout(**charts.BASE_LAYOUT, title=dict(text="Income vs satisfaction", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)))
            st.plotly_chart(fig, width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            rate_by_role = df.groupby("JobRole")["Attrition"].apply(lambda s: (s == "Yes").mean() * 100).sort_values(ascending=False).reset_index()
            st.plotly_chart(
                charts.hbar(rate_by_role, "Attrition", "JobRole", title="Attrition rate by job role", height=360, marker_color=COLORS["primary"]),
                width="stretch",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig = px.box(df, x="Department", y="MonthlyIncome", color="Attrition")
            fig.update_layout(**charts.BASE_LAYOUT, title=dict(text="Income by department", font=dict(size=15, color=COLORS["on_surface"], family=charts.FONT_STACK)), showlegend=False)
            fig.update_xaxes(gridcolor="rgba(198,197,212,0.35)")
            st.plotly_chart(fig, width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_corr:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        import matplotlib.pyplot as plt
        import seaborn as sns

        numeric = df.select_dtypes(include=np.number).columns.tolist()
        corr = df[numeric].corr()
        plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white"})
        fig_m, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            corr,
            annot=False,
            cmap="Spectral_r",
            linewidths=0.4,
            linecolor="white",
            square=True,
            ax=ax,
            cbar_kws={"shrink": 0.85},
        )
        ax.set_title("Feature correlation (numeric)", fontsize=13, color=COLORS["on_surface"])
        ax.tick_params(colors=COLORS["on_surface"], labelsize=9)
        fig_m.patch.set_facecolor("white")
        st.pyplot(fig_m)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  Advanced modules with loaded pipeline
# ═══════════════════════════════════════════════════════════════════════
def _advanced_with_pipeline(page_name: str):
    df = load_cached_data(DATA_FILE.stat().st_mtime)
    model, pre = eval_utils.ensure_deployed()

    if page_name == "Storytelling & Early Warning":
        render_storytelling_page(df, model, pre)
    elif page_name == "Multi-Stakeholder Views":
        render_multi_stakeholder_page(df, model, pre)
    elif page_name == "What-If Simulator":
        render_what_if_page(df, model, pre)
    elif page_name == "Time-Travel Analysis":
        render_time_travel_page(df)
    elif page_name == "R&D Deep-Dive":
        render_department_deepdive_page(df, model, pre)
    else:
        st.error(f"Module {page_name} not supported.")


# ═══════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════
def main():
    active = build_sidebar()

    subtitle_map = {
        "Dashboard": "Workforce risk at a glance",
        "Prediction Tool": "Score one employee",
        "Analytics": "Organization-wide signals",
        "Reports": "Model performance & explainability",
        "Settings": "Configuration & retraining",
        "Data Explorer": "Raw dataset inspection",
        "EDA Visualizations": "Distributions & relationships",
    }
    render_topbar(active, subtitle_map.get(active, "Advanced analytics"))
    st.markdown(page_header(active, subtitle_map.get(active, "")), unsafe_allow_html=True)

    if active == "Dashboard":
        show_dashboard()
    elif active == "Prediction Tool":
        show_prediction_tool()
    elif active == "Analytics":
        show_analytics()
    elif active == "Reports":
        show_reports()
    elif active == "Settings":
        show_settings()
    elif active == "Data Explorer":
        show_data_explorer()
    elif active == "EDA Visualizations":
        show_eda_visualizations()
    else:
        _advanced_with_pipeline(active)


if __name__ == "__main__":
    main()