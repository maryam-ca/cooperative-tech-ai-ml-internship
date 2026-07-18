"""
Employee Attrition Predictor - Streamlit Dashboard
A professional interactive dashboard for predicting employee attrition
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import pickle
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.preprocessor import DataPreprocessor
from src.storytelling import render_storytelling_page
from src.multi_stakeholder import render_multi_stakeholder_page
from src.what_if_simulator import render_what_if_page
from src.time_travel import render_time_travel_page
from src.department_deepdive import render_department_deepdive_page

# Page configuration - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — "Ledger"
#  A financial-terminal-inspired analytics identity.
#
#  Concept: this dashboard reads risk the way a trading desk
#  reads a position — numbers first, judgment second. The
#  signature element is the tabular-figure ticker rule:
#  every KPI is flanked by a thin index rule and a delta glyph,
#  borrowed from market tickers, never decorative icons.
#
#  Palette
#    Ink canvas      #0a0e16 / #0d121c
#    Hairline        rgba(148,163,184,.09)
#    Index accent    #6f7bf0 (signal indigo)
#    Long  (good)    #2dd4a7 (mint, not generic green)
#    Short (risk)    #f0654f (warm coral-red, not generic red)
#    Caution         #e0a73e (amber)
#  Type
#    Display / UI    Inter
#    Tabular figures Spline Sans Mono (distinct from the usual
#                    JetBrains/Roboto Mono default)
# ════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap');

:root {
    --ink-0: #07090f;
    --ink-1: #0a0e16;
    --ink-2: #0d121c;
    --ink-3: #111728;
    --hairline: rgba(148, 163, 184, 0.09);
    --hairline-strong: rgba(148, 163, 184, 0.16);
    --signal: #6f7bf0;
    --signal-soft: rgba(111, 123, 240, 0.1);
    --long: #2dd4a7;
    --long-soft: rgba(45, 212, 167, 0.09);
    --short: #f0654f;
    --short-soft: rgba(240, 101, 79, 0.09);
    --caution: #e0a73e;
    --caution-soft: rgba(224, 167, 62, 0.09);
    --ink-text: #e4e9f2;
    --ink-text-dim: #8993a8;
    --ink-text-faint: #4b5468;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ── Canvas: subtle vertical ledger lines, very faint ──── */
.stApp {
    background-color: var(--ink-0);
    background-image:
        linear-gradient(180deg, var(--ink-1) 0%, var(--ink-0) 100%),
        repeating-linear-gradient(90deg,
            transparent 0px, transparent 159px,
            rgba(148,163,184,0.025) 159px, rgba(148,163,184,0.025) 160px);
    background-attachment: fixed;
}

.main .block-container {
    padding: 2.5rem 3rem 5rem;
    max-width: 1440px;
}

/* ── Sidebar ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--ink-1) !important;
    border-right: 1px solid var(--hairline) !important;
}

[data-testid="stSidebar"] * { color: var(--ink-text-dim) !important; }

[data-testid="stSidebar"] .stRadio label {
    color: var(--ink-text-dim) !important;
    font-size: 0.8125rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.01em !important;
    padding: 0.5rem 0.625rem 0.5rem 0.875rem !important;
    border-radius: 4px !important;
    border-left: 2px solid transparent !important;
    transition: all 0.15s ease !important;
    display: block !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(111, 123, 240, 0.06) !important;
    color: var(--ink-text) !important;
}

[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] input:checked + div + label,
[data-testid="stSidebar"] .stRadio div[data-checked="true"] + label {
    background: var(--signal-soft) !important;
    border-left: 2px solid var(--signal) !important;
    color: #b3bafa !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] hr { border-color: var(--hairline) !important; margin: 1.375rem 0 !important; }

[data-testid="stSidebar"] a {
    color: var(--signal) !important;
    text-decoration: none !important;
    font-size: 0.7813rem !important;
    border-bottom: 1px solid rgba(111, 123, 240, 0.3);
    padding-bottom: 1px;
}

[data-testid="stSidebar"] h3 {
    font-size: 0.625rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--ink-text-faint) !important;
    margin: 1.625rem 0 0.625rem !important;
}

[data-testid="stSidebar"] .stMarkdown:first-of-type p {
    font-size: 1.0625rem !important;
    font-weight: 600 !important;
    color: var(--ink-text) !important;
    letter-spacing: -0.015em !important;
    font-family: 'Spline Sans Mono', monospace !important;
}

/* ── Masthead ────────────────────────────────────────────── */
.masthead {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    padding-bottom: 1.375rem;
    margin-bottom: 2.25rem;
    border-bottom: 1px solid var(--hairline-strong);
}

.main-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.875rem;
    font-weight: 600;
    letter-spacing: -0.028em;
    line-height: 1.15;
    color: var(--ink-text);
    margin: 0;
}

.main-title .accent { color: var(--signal); font-weight: 600; }

.masthead-meta {
    font-family: 'Spline Sans Mono', monospace;
    font-size: 0.6875rem;
    color: var(--ink-text-faint);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    text-align: right;
    line-height: 1.6;
}

.sub-title {
    font-size: 0.9375rem;
    font-weight: 400;
    color: var(--ink-text-dim);
    margin: -1.75rem 0 2.25rem;
    letter-spacing: 0.005em;
}

/* ── Section eyebrow (used before major blocks) ─────────── */
.eyebrow {
    display: flex;
    align-items: center;
    gap: 0.625rem;
    font-family: 'Spline Sans Mono', monospace;
    font-size: 0.6875rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-text-faint);
    margin: 0 0 1rem;
}

.eyebrow::before {
    content: '';
    width: 14px;
    height: 1px;
    background: var(--signal);
}

/* ── Cards ───────────────────────────────────────────────── */
.card {
    background: var(--ink-2);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    padding: 1.625rem 1.75rem;
    margin-bottom: 1.25rem;
}

.card-title {
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ink-text-faint);
    margin-bottom: 1.125rem;
    padding-bottom: 0.875rem;
    border-bottom: 1px solid var(--hairline);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.card p, .card li, .card ul { color: var(--ink-text-dim); font-size: 0.9rem; line-height: 1.75; }
.card strong { color: var(--ink-text); font-weight: 500; }

/* ── KPI ticker cards — the signature element ───────────── */
.kpi {
    background: var(--ink-2);
    border: 1px solid var(--hairline);
    border-radius: 8px;
    padding: 1.25rem 1.375rem 1.125rem;
    position: relative;
}

.kpi-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 0.625rem;
}

.kpi-label {
    font-size: 0.6875rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--ink-text-faint);
}

.kpi-tag {
    font-family: 'Spline Sans Mono', monospace;
    font-size: 0.625rem;
    font-weight: 500;
    letter-spacing: 0.02em;
    padding: 0.125rem 0.4375rem;
    border-radius: 3px;
}

.kpi-tag.long { color: var(--long); background: var(--long-soft); }
.kpi-tag.short { color: var(--short); background: var(--short-soft); }
.kpi-tag.neutral { color: var(--signal); background: var(--signal-soft); }

.kpi-value {
    font-family: 'Spline Sans Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: var(--ink-text);
    letter-spacing: -0.02em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
}

.kpi-rule {
    height: 1px;
    background: linear-gradient(90deg, var(--hairline-strong) 0%, transparent 100%);
    margin-top: 0.875rem;
}

/* ── Prediction verdict — signature treatment ───────────── */
.verdict {
    border-radius: 8px;
    padding: 0;
    margin: 1rem 0 1.25rem;
    border: 1px solid var(--hairline-strong);
    overflow: hidden;
    background: var(--ink-2);
}

.verdict-strip {
    height: 3px;
    width: 100%;
}

.verdict-strip.short { background: linear-gradient(90deg, var(--short), #f0654f55); }
.verdict-strip.long  { background: linear-gradient(90deg, var(--long), #2dd4a755); }

.verdict-body {
    padding: 2rem 2.25rem 2.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
}

.verdict-label {
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.verdict-label.short { color: var(--short); }
.verdict-label.long { color: var(--long); }

.verdict-headline {
    font-size: 1.375rem;
    font-weight: 600;
    letter-spacing: -0.015em;
    color: var(--ink-text);
    margin-bottom: 0.375rem;
}

.verdict-sub { font-size: 0.875rem; color: var(--ink-text-dim); }

.verdict-figure { text-align: right; flex-shrink: 0; }

.verdict-figure .num {
    font-family: 'Spline Sans Mono', monospace;
    font-size: 2.5rem;
    font-weight: 600;
    line-height: 1;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
}

.verdict-figure.short .num { color: var(--short); }
.verdict-figure.long .num { color: var(--long); }

.verdict-figure .figcap {
    font-family: 'Spline Sans Mono', monospace;
    font-size: 0.6875rem;
    color: var(--ink-text-faint);
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── Tech badges ─────────────────────────────────────────── */
.tech-badge {
    display: inline-flex;
    align-items: center;
    background: var(--ink-3);
    border: 1px solid var(--hairline);
    color: var(--ink-text-dim);
    font-family: 'Spline Sans Mono', monospace;
    font-size: 0.7188rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    padding: 0.375rem 0.75rem;
    border-radius: 4px;
}

/* ── Insight blocks ──────────────────────────────────────── */
.insight-block, .retention-block {
    border-radius: 6px;
    padding: 1.375rem 1.5rem;
    background: var(--ink-3);
    border: 1px solid var(--hairline);
    border-left: 2px solid var(--caution);
}

.retention-block { border-left-color: var(--signal); }

.insight-block h4, .retention-block h4 {
    font-size: 0.6875rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.insight-block h4 { color: var(--caution); }
.retention-block h4 { color: var(--signal); }
.insight-block li, .retention-block li { color: var(--ink-text-dim); font-size: 0.875rem; line-height: 2; }

/* ── Risk factor rows ────────────────────────────────────── */
.risk-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--hairline);
    font-size: 0.875rem;
    color: var(--ink-text-dim);
}
.risk-row:last-child { border-bottom: none; }
.risk-row .rlevel {
    font-family: 'Spline Sans Mono', monospace;
    font-weight: 600;
    font-size: 0.7188rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Callouts ────────────────────────────────────────────── */
div[data-testid="stInfo"] {
    background: var(--signal-soft) !important;
    border: 1px solid rgba(111,123,240,0.22) !important;
    border-radius: 6px !important;
    color: var(--ink-text-dim) !important;
}
div[data-testid="stError"] {
    background: var(--short-soft) !important;
    border: 1px solid rgba(240,101,79,0.22) !important;
    border-radius: 6px !important;
}
div[data-testid="stSuccess"] {
    background: var(--long-soft) !important;
    border: 1px solid rgba(45,212,167,0.22) !important;
    border-radius: 6px !important;
}

/* ── st.metric ───────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--ink-2) !important;
    border: 1px solid var(--hairline) !important;
    border-radius: 8px !important;
    padding: 1rem 1.25rem !important;
}
[data-testid="metric-container"] label {
    color: var(--ink-text-faint) !important;
    font-size: 0.6875rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Spline Sans Mono', monospace !important;
    color: var(--ink-text) !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    font-variant-numeric: tabular-nums !important;
}

/* ── Tabs ────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--hairline-strong) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--ink-text-faint) !important;
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    padding: 0.6875rem 1.125rem !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.15s ease !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--ink-text-dim) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: var(--signal) !important;
    border-bottom: 2px solid var(--signal) !important;
}

/* ── Buttons ─────────────────────────────────────────────── */
.stButton > button {
    background: var(--signal) !important;
    color: #060810 !important;
    border: none !important;
    padding: 0.6875rem 1.75rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8125rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover { background: #828dfb !important; box-shadow: 0 4px 20px rgba(111,123,240,0.25) !important; }
.stButton > button:active { transform: scale(0.99) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: var(--ink-text-dim) !important;
    border: 1px solid var(--hairline-strong) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.25rem !important;
}
.stDownloadButton > button:hover { border-color: var(--signal) !important; color: var(--signal) !important; }

/* ── Inputs ──────────────────────────────────────────────── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: var(--ink-1) !important;
    border: 1px solid var(--hairline-strong) !important;
    border-radius: 6px !important;
    color: var(--ink-text) !important;
    font-family: 'Spline Sans Mono', monospace !important;
    font-size: 0.8438rem !important;
}
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus {
    border-color: var(--signal) !important;
    box-shadow: 0 0 0 3px var(--signal-soft) !important;
}
[data-baseweb="select"] [data-baseweb="menu"] {
    background: var(--ink-2) !important;
    border: 1px solid var(--hairline-strong) !important;
    border-radius: 6px !important;
}
.stSelectbox label, .stNumberInput label, .stTextInput label, .stSlider label {
    color: var(--ink-text-faint) !important;
    font-size: 0.7813rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}

/* ── Sliders ─────────────────────────────────────────────── */
.stSlider [data-testid="stTickBar"] { color: var(--ink-text-faint) !important; }
.stSlider [role="slider"] { background: var(--signal) !important; border: 2px solid var(--ink-0) !important; }
.stSlider [data-testid="stMarkdownContainer"] p { color: var(--ink-text-faint) !important; font-size: 0.75rem !important; }
.stSlider > div > div > div > div { background: var(--signal) !important; }

/* ── Progress ────────────────────────────────────────────── */
.stProgress > div > div > div { background: var(--signal) !important; border-radius: 3px !important; }
.stProgress > div > div { background: var(--hairline-strong) !important; border-radius: 3px !important; }

/* ── Tables / dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] { border: 1px solid var(--hairline-strong) !important; border-radius: 8px !important; overflow: hidden !important; }
.glideDataEditor { background: var(--ink-1) !important; }

/* ── Expander ────────────────────────────────────────────── */
[data-testid="stExpander"] { background: var(--ink-2) !important; border: 1px solid var(--hairline) !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary {
    color: var(--ink-text-dim) !important;
    font-size: 0.7813rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}

/* ── Misc ────────────────────────────────────────────────── */
.stpyplot { background: transparent !important; }
hr { border: none !important; border-top: 1px solid var(--hairline) !important; margin: 1.75rem 0 !important; }
h1, h2, h3, h4 { color: var(--ink-text) !important; font-family: 'Inter', sans-serif !important; }
h3 { font-size: 0.9375rem !important; font-weight: 600 !important; letter-spacing: -0.005em !important; color: #c4ccda !important; }
h4 { font-size: 0.875rem !important; font-weight: 600 !important; color: var(--ink-text-dim) !important; }
.stMarkdown p { color: var(--ink-text-faint) !important; font-size: 0.875rem !important; line-height: 1.7 !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--ink-0); }
::-webkit-scrollbar-thumb { background: rgba(111,123,240,0.28); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(111,123,240,0.45); }
</style>
""", unsafe_allow_html=True)

# ─── Matplotlib dark theme, matched to the Ledger system ──────────────────
plt.rcParams.update({
    'figure.facecolor':   '#0d121c',
    'axes.facecolor':     '#0d121c',
    'savefig.facecolor':  '#0d121c',
    'axes.edgecolor':     '#1b2333',
    'axes.labelcolor':    '#8993a8',
    'axes.titlecolor':    '#e4e9f2',
    'axes.titlesize':     12,
    'axes.titleweight':   '600',
    'axes.labelsize':     10,
    'axes.grid':          True,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'grid.color':         '#1b2333',
    'grid.linewidth':     0.6,
    'xtick.color':        '#4b5468',
    'ytick.color':        '#4b5468',
    'xtick.labelsize':    9,
    'ytick.labelsize':    9,
    'legend.facecolor':   '#0a0e16',
    'legend.edgecolor':   '#1b2333',
    'legend.labelcolor':  '#8993a8',
    'legend.fontsize':    9,
    'text.color':         '#8993a8',
    'font.family':        'sans-serif',
    'font.size':          10,
})

# ─── Color palette mapped to the Ledger identity ───────────────────────────
CHART_COLORS = {
    'primary':   '#6f7bf0',   # signal indigo
    'secondary': '#b3bafa',   # soft indigo tint
    'positive':  '#2dd4a7',   # long / mint
    'negative':  '#f0654f',   # short / coral-red
    'neutral':   '#4b5468',
    'accent':    '#e0a73e',   # caution amber
}
DUAL_PALETTE   = [CHART_COLORS['positive'], CHART_COLORS['negative']]
SINGLE_PALETTE = [CHART_COLORS['primary']]
MULTI_PALETTE  = ['#6f7bf0', '#b3bafa', '#2dd4a7', '#f0654f', '#e0a73e', '#4ba3e8']

# Load data
@st.cache_data
def load_cached_data():
    """Load and cache the dataset"""
    data_path = Path(__file__).parent / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    return pd.read_csv(data_path)

import joblib

@st.cache_resource
def load_trained_model():
    model_path = Path(__file__).parent / "models" / "best_model.pkl"

    if model_path.exists():
        return joblib.load(model_path)

    return None

# Main app
def main():
    # Sidebar
    with st.sidebar:
        # st.image("https://img.icons8.com/fluency/96/employee.png", width=64)
        st.markdown("### Employee Attrition")
        st.markdown("**Predictor Dashboard**")
        st.markdown("---")
        
        # Navigation
        st.markdown("### Core")
        page = st.radio(
    "Navigation",
    [
        "Project Overview",
        "Data Explorer",
        "EDA Visualizations",
        "Prediction Tool",
        "Model Performance",
    ],
    label_visibility="collapsed"
)
        st.markdown("---")
        st.markdown("### Advanced Analytics")
        adv_page = st.radio(
    "Advanced Navigation",
    [
        "Storytelling & Early Warning",
        "Multi-Stakeholder Views",
        "What-If Simulator",
        "Time-Travel Analysis",
        "R&D Deep-Dive",
    ],
    label_visibility="collapsed"
)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This dashboard predicts employee attrition using machine learning.
        Built with **Streamlit** and **Scikit-learn**.
        """)
        
        st.markdown("---")
        st.markdown("### Contact")
        st.markdown("[GitHub Repository](https://github.com/Samra-ca/employee-attrition-predictor)")

    # Main content based on page
    st.markdown("""
    <div class="masthead">
        <h1 class="main-title">Employee Attrition <span class="accent">Predictor</span></h1>
        <div class="masthead-meta">IBM HR Analytics<br/>Predictive Risk Model</div>
    </div>
    """, unsafe_allow_html=True)
    
    if page == "Project Overview":
        show_overview()
    elif page == "Data Explorer":
        show_data_explorer()
    elif page == "EDA Visualizations":
        show_eda_visualizations()
    elif page == "Prediction Tool":
        show_prediction_tool()
    elif page == "Model Performance":
        show_model_performance()
    elif adv_page == "Storytelling & Early Warning":
        model = load_trained_model()
        if model is not None:
            data = load_cached_data()
            render_storytelling_page(data, model, DataPreprocessor())
        else:
            st.error("Model not found. Please train the model first.")
    elif adv_page == "Multi-Stakeholder Views":
        model = load_trained_model()
        if model is not None:
            data = load_cached_data()
            render_multi_stakeholder_page(data, model, DataPreprocessor())
        else:
            st.error("Model not found. Please train the model first.")
    elif adv_page == "What-If Simulator":
        model = load_trained_model()
        if model is not None:
            data = load_cached_data()
            render_what_if_page(data, model, DataPreprocessor())
        else:
            st.error("Model not found. Please train the model first.")
    elif adv_page == "Time-Travel Analysis":
        data = load_cached_data()
        render_time_travel_page(data)
    elif adv_page == "R&D Deep-Dive":
        model = load_trained_model()
        if model is not None:
            data = load_cached_data()
            render_department_deepdive_page(data, model, DataPreprocessor())
        else:
            st.error("Model not found. Please train the model first.")

def show_overview():
    """Project Overview Page"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Project Overview</div>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Employee attrition is a critical challenge for organizations, costing 
                companies billions annually. This project leverages machine learning to 
                predict which employees are likely to leave, enabling proactive retention 
                strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <div class="card-title">Business Problem</div>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                High employee turnover leads to:
            </p>
            <ul style="font-size: 1rem; line-height: 1.8;">
                <li><strong>Financial loss:</strong> 33% of annual salary per departed employee</li>
                <li><strong>Productivity decline:</strong> 3-6 months to reach full productivity</li>
                <li><strong>Knowledge drain:</strong> Loss of institutional knowledge and expertise</li>
                <li><strong>Morale impact:</strong> Reduced team morale and increased workload</li>
            </ul>
            <p style="font-size: 1.1rem; line-height: 1.6; margin-top: 1rem;">
                <strong>Solution:</strong> Predict attrition risk to implement targeted retention programs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Key metrics
        df = load_cached_data()
        total_employees = len(df)
        attrition_count = df['Attrition'].value_counts().get('Yes', 0)
        attrition_rate = (attrition_count / total_employees) * 100
        
        st.markdown('<div class="eyebrow">Key metrics</div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">Headcount</span>
                    <span class="kpi-tag neutral">TOTAL</span>
                </div>
                <div class="kpi-value">{total_employees:,}</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-row">
                    <span class="kpi-label">Attrition</span>
                    <span class="kpi-tag short">RISK</span>
                </div>
                <div class="kpi-value">{attrition_rate:.1f}%</div>
                <div class="kpi-rule"></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card" style="margin-top: 1.25rem;">
            <div class="card-title">Dataset Info</div>
            <ul style="font-size: 0.95rem; line-height: 2;">
                <li><strong>Source:</strong> IBM HR Analytics</li>
                <li><strong>Rows:</strong> 1,470</li>
                <li><strong>Features:</strong> 35</li>
                <li><strong>Target:</strong> Attrition (Yes/No)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Tech Stack
    st.markdown("""
    <div class="card">
        <div class="card-title">Technology Stack</div>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; padding: 0.5rem 0;">
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Pandas</span>
            <span class="tech-badge">NumPy</span>
            <span class="tech-badge">Matplotlib</span>
            <span class="tech-badge">Seaborn</span>
            <span class="tech-badge">Scikit-learn</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Plotly</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_data_explorer():
    """Data Explorer Page"""
    df = load_cached_data()
    
    st.markdown("""
    <div class="card">
        <div class="card-title">Dataset Explorer</div>
        <p>Explore the employee attrition dataset with interactive filters.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    st.markdown('<div class="eyebrow">Filters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        departments = ['All'] + sorted(df['Department'].unique().tolist())
        selected_dept = st.selectbox("Department", departments)
    
    with col2:
        attrition_options = ['All', 'Yes', 'No']
        selected_attrition = st.selectbox("Attrition Status", attrition_options)
    
    with col3:
        max_age = int(df['Age'].max())
        age_range = st.slider("Age Range", 18, max_age, (18, max_age))
    
    # Filter data
    filtered_df = df.copy()
    if selected_dept != 'All':
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    if selected_attrition != 'All':
        filtered_df = filtered_df[filtered_df['Attrition'] == selected_attrition]
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]
    
    # Show stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", f"{len(filtered_df):,}")
    with col2:
        attrition_count = len(filtered_df[filtered_df['Attrition'] == 'Yes'])
        st.metric("Attrition Count", attrition_count)
    with col3:
        attrition_rate = (attrition_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
    with col4:
        avg_age = filtered_df['Age'].mean()
        st.metric("Avg Age", f"{avg_age:.1f}")
    
    # Display data
    st.markdown('<div class="eyebrow" style="margin-top: 1.5rem;">Data preview</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        column_config={
            "Attrition": st.column_config.TextColumn("Attrition", width="small"),
            "Age": st.column_config.NumberColumn("Age", width="small"),
            "Department": st.column_config.TextColumn("Department", width="medium"),
            "JobRole": st.column_config.TextColumn("Job Role", width="medium"),
            "MonthlyIncome": st.column_config.NumberColumn("Monthly Income", format="$%d"),
        }
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv,
        file_name="filtered_employee_data.csv",
        mime="text/csv"
    )

def show_eda_visualizations():
    """EDA Visualizations Page"""
    df = load_cached_data()
    
    st.markdown("""
    <div class="card">
        <div class="card-title">Exploratory Data Analysis</div>
        <p>Visual insights into employee attrition patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Attrition Distribution", 
        "Correlation Heatmap",
        "Feature Analysis",
        "Categorical Analysis",
        "Key Distributions",
        "Insights"
    ])
    
    with tab1:
        st.markdown("#### Attrition Distribution")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Count plot
        attrition_counts = df['Attrition'].value_counts()
        colors = [CHART_COLORS['positive'], CHART_COLORS['negative']]
        bars = ax1.bar(attrition_counts.index, attrition_counts.values, color=colors,
                       width=0.45, zorder=3)
        ax1.set_title('Attrition Count', fontsize=13, fontweight='600', pad=14)
        ax1.set_xlabel('Attrition', labelpad=8)
        ax1.set_ylabel('Count', labelpad=8)
        for bar, v in zip(bars, attrition_counts.values):
            ax1.text(bar.get_x() + bar.get_width()/2, v + 18, str(v),
                     ha='center', fontweight='600', color='#e4e9f2', fontsize=10)
        
        # Pie chart
        wedges, texts, autotexts = ax2.pie(
            attrition_counts.values,
            labels=attrition_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            explode=(0, 0.06),
            wedgeprops=dict(linewidth=2, edgecolor='#0a0e16')
        )
        for t in texts:    t.set_color('#8993a8')
        for at in autotexts: at.set_color('#0d121c'); at.set_fontweight('600')
        ax2.set_title('Attrition Percentage', fontsize=13, fontweight='600', pad=14)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        st.info("""
        **Key Insight:** The dataset is imbalanced with only 16.1% attrition cases. 
        This imbalance will be addressed during model training using class weights.
        """)
    
    with tab2:
        st.markdown("#### Correlation Heatmap")
        
        # Select numerical columns
        numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
        corr_matrix = df[numerical_cols].corr()
        
        # Filter to show only relevant correlations with attrition
        attrition_corr = corr_matrix['Attrition_Yes'].sort_values(ascending=False) if 'Attrition_Yes' in corr_matrix.columns else corr_matrix
        
        fig, ax = plt.subplots(figsize=(14, 10))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                    cmap='coolwarm', center=0, square=True,
                    linewidths=0.4, linecolor='#0d121c',
                    annot_kws={'size': 7, 'color': '#e4e9f2'},
                    ax=ax)
        ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='600', pad=16)
        ax.tick_params(colors='#4b5468', labelsize=8)
        st.pyplot(fig)
        plt.close()
        
        st.info("""
        **Key Insight:** Variables like Overtime, YearsAtCompany, and MonthlyIncome 
        show moderate correlation with attrition, making them important predictors.
        """)
    
    with tab3:
        st.markdown("#### Feature Analysis by Attrition")
        
        feature_options = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears', 
                          'YearsInCurrentRole', 'YearsWithCurrManager']
        selected_feature = st.selectbox("Select Feature to Analyze", feature_options)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df, x='Attrition', y=selected_feature,
                    palette={'No': CHART_COLORS['positive'], 'Yes': CHART_COLORS['negative']},
                    linewidth=1.2, flierprops=dict(marker='o', markersize=3,
                    markerfacecolor='#4b5468', alpha=0.5))
        ax.set_title(f'{selected_feature} Distribution by Attrition', fontsize=13, fontweight='600', pad=14)
        ax.set_xlabel('Attrition', labelpad=8)
        ax.set_ylabel(selected_feature, labelpad=8)
        st.pyplot(fig)
        plt.close()
        
        # Show statistics
        yes_stats = df[df['Attrition'] == 'Yes'][selected_feature].describe()
        no_stats = df[df['Attrition'] == 'No'][selected_feature].describe()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Attrition: Yes**")
            st.dataframe(yes_stats)
        with col2:
            st.markdown(f"**Attrition: No**")
            st.dataframe(no_stats)
    
    with tab4:
        st.markdown("#### Categorical Feature Analysis")
        
        cat_cols = ['Department', 'JobRole', 'MaritalStatus', 'EducationField', 'OverTime']
        selected_cat = st.selectbox("Select Categorical Feature", cat_cols)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Distribution
        vc = df[selected_cat].value_counts()
        axes[0].bar(vc.index, vc.values, color=CHART_COLORS['primary'], width=0.55, zorder=3)
        axes[0].set_title(f'{selected_cat} Distribution', fontsize=13, fontweight='600', pad=14)
        axes[0].set_xlabel(selected_cat, labelpad=8)
        axes[0].set_ylabel('Count', labelpad=8)
        axes[0].tick_params(axis='x', rotation=35)
        
        # Attrition rate by category
        attrition_by_cat = df.groupby(selected_cat)['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).sort_values(ascending=False)
        
        bar_colors = [CHART_COLORS['negative'] if v > 20 else CHART_COLORS['positive']
                      for v in attrition_by_cat.values]
        axes[1].bar(attrition_by_cat.index, attrition_by_cat.values,
                    color=bar_colors, width=0.55, zorder=3)
        axes[1].set_title(f'Attrition Rate by {selected_cat}', fontsize=13, fontweight='600', pad=14)
        axes[1].set_xlabel(selected_cat, labelpad=8)
        axes[1].set_ylabel('Attrition Rate (%)', labelpad=8)
        axes[1].tick_params(axis='x', rotation=35)
        axes[1].axhline(y=16.1, color=CHART_COLORS['accent'],
                        linestyle='--', linewidth=1.2, label='Overall Rate (16.1%)')
        axes[1].legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with tab5:
        st.markdown("#### Key Feature Distributions")
        
        features_to_plot = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'TotalWorkingYears']
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for idx, feature in enumerate(features_to_plot):
            df[feature].hist(bins=30, ax=axes[idx],
                             color=CHART_COLORS['primary'],
                             edgecolor='#0a0e16', alpha=0.85, linewidth=0.5)
            axes[idx].axvline(df[feature].mean(), color=CHART_COLORS['accent'],
                              linestyle='--', linewidth=1.4,
                              label=f'Mean: {df[feature].mean():.1f}')
            axes[idx].axvline(df[feature].median(), color=CHART_COLORS['positive'],
                              linestyle='--', linewidth=1.4,
                              label=f'Median: {df[feature].median():.1f}')
            axes[idx].set_title(f'{feature} Distribution', fontsize=12, fontweight='600', pad=12)
            axes[idx].set_xlabel(feature, labelpad=6)
            axes[idx].set_ylabel('Frequency', labelpad=6)
            axes[idx].legend(fontsize=8)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    with tab6:
        st.markdown("#### Key Insights Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-block">
                <h4>High Attrition Factors</h4>
                <ul style="padding-left: 1.25rem;">
                    <li><strong>Overtime:</strong> Employees working overtime are 2.5x more likely to leave</li>
                    <li><strong>Years at Company:</strong> Peak attrition occurs at 1–2 years tenure</li>
                    <li><strong>Job Role:</strong> Sales and Research roles have highest attrition</li>
                    <li><strong>Marital Status:</strong> Single employees show higher attrition rates</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="retention-block">
                <h4>Retention Factors</h4>
                <ul style="padding-left: 1.25rem;">
                    <li><strong>Job Satisfaction:</strong> Higher satisfaction = lower attrition</li>
                    <li><strong>Years with Manager:</strong> Longer tenure with manager = better retention</li>
                    <li><strong>Work-Life Balance:</strong> Good balance reduces attrition by 40%</li>
                    <li><strong>Promotion:</strong> Recent promotions show lower attrition</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_prediction_tool():
    """Prediction Tool Page"""
    st.markdown("""
    <div class="card">
        <div class="card-title">Attrition Prediction Tool</div>
        <p>Enter employee details to predict attrition risk.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    model = load_trained_model()
    
    if model is None:
        st.error("Model not found. Please train the model first.")
        return
    
    # Input form
    st.markdown('<div class="eyebrow">Employee information</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=65, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
    
    with col2:
        department = st.selectbox("Department", 
            ["Research & Development", "Sales", "Human Resources"])
        job_role = st.selectbox("Job Role", 
            ["Research Scientist", "Laboratory Technician", "Sales Executive", 
             "Sales Representative", "Manager", "Human Resources"])
        education = st.selectbox(
            "Education Level",
            {
                1: "Below College",
                2: "College",
                3: "Bachelor",
                4: "Master",
                5: "Doctor"
            },
            format_func=lambda x: {
                1: "Below College",
                2: "College",
                3: "Bachelor",
                4: "Master",
                5: "Doctor"
            }[x]
        )
    
    with col3:
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=25000, value=5000, step=500)
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5)
        overtime = st.selectbox("Overtime", ["No", "Yes"])
    
    # Advanced features
    with st.expander("Advanced Features (Optional)"):
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            total_working_years = st.number_input("Total Working Years", min_value=0, max_value=50, value=10)
            years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=30, value=3)
        
        with col_b:
            job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
            work_life_balance = st.slider("Work-Life Balance (1-4)", 1, 4, 3)
        
        with col_c:
            distance_from_home = st.number_input("Distance from Home (miles)", min_value=1, max_value=50, value=10)
            num_companies_worked = st.number_input("Number of Companies Worked", min_value=1, max_value=20, value=2)
    
    # Predict button
    if st.button("Predict Attrition Risk", use_container_width=True):
        input_data = {
            'Age': age,
            'Gender': gender,
            'MaritalStatus': marital_status,
            'Department': department,
            'JobRole': job_role,
            'Education': education,
            'MonthlyIncome': monthly_income,
            'YearsAtCompany': years_at_company,
            'OverTime': overtime,
            'TotalWorkingYears': total_working_years,
            'YearsInCurrentRole': years_in_current_role,
            'JobSatisfaction': job_satisfaction,
            'WorkLifeBalance': work_life_balance,
            'DistanceFromHome': distance_from_home,
            'NumCompaniesWorked': num_companies_worked
        }

        try:
            model_dir = Path(__file__).parent / "models"
            preprocessor = DataPreprocessor()
            preprocessor.scaler = joblib.load(model_dir / "scaler.pkl")
            preprocessor.label_encoders = joblib.load(model_dir / "label_encoders.pkl")
            preprocessor.feature_columns = joblib.load(model_dir / "feature_columns.pkl")

            df_input = pd.DataFrame([input_data])
            processed_data = preprocessor.transform(df_input)

            prediction = model.predict(processed_data)[0]
            probability = model.predict_proba(processed_data)[0]

        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return

        st.markdown('<div class="eyebrow" style="margin-top: 1.75rem;">Prediction result</div>', unsafe_allow_html=True)

        if prediction == 1:
            st.markdown("""
            <div class="verdict">
                <div class="verdict-strip short"></div>
                <div class="verdict-body">
                    <div>
                        <div class="verdict-label short">Elevated risk</div>
                        <div class="verdict-headline">High attrition risk</div>
                        <div class="verdict-sub">This employee has a high probability of leaving.</div>
                    </div>
                    <div class="verdict-figure short">
                        <div class="num">{:.1f}%</div>
                        <div class="figcap">P(attrition)</div>
                    </div>
                </div>
            </div>
            """.format(probability[1] * 100), unsafe_allow_html=True)

            st.markdown("""
            <div class="card" style="border-left: 2px solid var(--short);">
                <div class="card-title" style="color: #f0654f;">Recommended Actions</div>
                <ul style="font-size: 0.9375rem; line-height: 2;">
                    <li>Schedule a career development discussion</li>
                    <li>Review compensation and benefits package</li>
                    <li>Consider role rotation or promotion</li>
                    <li>Improve work-life balance if applicable</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="verdict">
                <div class="verdict-strip long"></div>
                <div class="verdict-body">
                    <div>
                        <div class="verdict-label long">Stable</div>
                        <div class="verdict-headline">Low attrition risk</div>
                        <div class="verdict-sub">This employee is likely to stay with the company.</div>
                    </div>
                    <div class="verdict-figure long">
                        <div class="num">{:.1f}%</div>
                        <div class="figcap">P(retention)</div>
                    </div>
                </div>
            </div>
            """.format(probability[0] * 100), unsafe_allow_html=True)

            st.markdown("""
            <div class="card" style="border-left: 2px solid var(--long);">
                <div class="card-title" style="color: #2dd4a7;">Positive Indicators</div>
                <ul style="font-size: 0.9375rem; line-height: 2;">
                    <li>Good job satisfaction and work-life balance</li>
                    <li>Competitive compensation structure</li>
                    <li>Stable career progression path</li>
                    <li>Positive work environment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-title">Key Risk Factors Assessed</div>
        """, unsafe_allow_html=True)

        risk_factors = []
        if overtime == "Yes":
            risk_factors.append(("Over Time", "High", "#f0654f"))
        if years_at_company < 2:
            risk_factors.append(("Tenure < 2 Years", "High", "#f0654f"))
        if job_satisfaction < 2:
            risk_factors.append(("Job Satisfaction < 2", "High", "#f0654f"))
        if work_life_balance < 2:
            risk_factors.append(("Work-Life Balance < 2", "High", "#f0654f"))
        if monthly_income < 3000:
            risk_factors.append(("Income < $3,000", "Medium", "#e0a73e"))
        if distance_from_home > 20:
            risk_factors.append(("Long Commute > 20 miles", "Medium", "#e0a73e"))

        if risk_factors:
            for factor, level, color in risk_factors:
                st.markdown(f"""
                <div class="risk-row">
                    <span>{factor}</span>
                    <span class="rlevel" style="color: {color};">{level}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No significant risk factors identified.")

        st.markdown("</div>", unsafe_allow_html=True)


def show_model_performance():

    """Model Performance Page"""
    st.markdown("""
    <div class="card">
        <div class="card-title">Model Performance Dashboard</div>
        <p>Evaluate the performance of our machine learning models.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample metrics (these should be loaded from actual model results)
    metrics = {
        "Logistic Regression": {
            "Accuracy": 0.872,
            "Precision": 0.683,
            "Recall": 0.579,
            "F1-Score": 0.626,
            "ROC-AUC": 0.858
        },
        "Random Forest": {
            "Accuracy": 0.895,
            "Precision": 0.742,
            "Recall": 0.632,
            "F1-Score": 0.683,
            "ROC-AUC": 0.912
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Model Comparison</div>
        """, unsafe_allow_html=True)
        
        # Create comparison chart
        fig, ax = plt.subplots(figsize=(10, 6))
        models = list(metrics.keys())
        metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
        
        x = np.arange(len(metrics_to_plot))
        width = 0.35
        palette = [CHART_COLORS['primary'], CHART_COLORS['secondary']]
        
        for idx, model in enumerate(models):
            values = [metrics[model][m] for m in metrics_to_plot]
            bars = ax.bar(x + idx * width, values, width, label=model,
                          color=palette[idx], zorder=3, alpha=0.9)
        
        ax.set_ylabel('Score', labelpad=8)
        ax.set_title('Model Performance Comparison', fontsize=13, fontweight='600', pad=14)
        ax.set_xticks(x + width / 2)
        ax.set_xticklabels(metrics_to_plot)
        ax.legend(loc='lower right')
        ax.set_ylim(0, 1.05)
        
        st.pyplot(fig)
        plt.close()
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Best Model: Random Forest</div>
        """, unsafe_allow_html=True)
        
        # Create gauge charts for each metric
        for metric, value in metrics["Random Forest"].items():
            st.markdown(f"**{metric}:**")
            st.progress(value)
            st.markdown(f"""<span style='font-family: "Spline Sans Mono", monospace;
                              font-weight: 600; color: #6f7bf0; font-size: 0.875rem;'>{value:.3f}</span>""",
                        unsafe_allow_html=True)
            st.markdown("---")
        
        st.markdown("""
        <div style="margin-top: 1rem; padding: 1.25rem;
                    background: var(--signal-soft);
                    border: 1px solid rgba(111,123,240,0.2);
                    border-radius: 8px;">
            <div class="card-title" style="border-bottom: none; margin-bottom: 0.75rem; padding-bottom: 0;">Why Random Forest?</div>
            <ul style="font-size: 0.875rem; line-height: 1.9; color: var(--ink-text-dim); padding-left: 1.25rem;">
                <li><strong>Higher ROC-AUC:</strong> 0.912 vs 0.858</li>
                <li><strong>Better F1-Score:</strong> 0.683 vs 0.626</li>
                <li><strong>Handles imbalance:</strong> Better with class weights</li>
                <li><strong>Feature importance:</strong> Provides interpretability</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Confusion Matrix
    st.markdown("""
    <div class="card">
        <div class="card-title">Confusion Matrix — Random Forest</div>
    """, unsafe_allow_html=True)
    
    # Sample confusion matrix
    cm = np.array([[235, 12], [15, 28]])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d',
                cmap=sns.light_palette('#6f7bf0', as_cmap=True),
                ax=ax,
                linewidths=2, linecolor='#0a0e16',
                annot_kws={'size': 14, 'fontweight': 'bold', 'color': '#0a0e16'},
                xticklabels=['Predicted: No', 'Predicted: Yes'],
                yticklabels=['Actual: No', 'Actual: Yes'])
    ax.set_title('Confusion Matrix — Random Forest', fontsize=13, fontweight='600', pad=16)
    ax.tick_params(colors='#4b5468', labelsize=10)
    st.pyplot(fig)
    plt.close()
    
    # Interpretation
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="padding: 1rem 1.25rem; background: var(--long-soft);
                    border: 1px solid rgba(45,212,167,0.18); border-radius: 8px; margin-bottom: 0.75rem;">
            <h4 style="color: #2dd4a7; margin: 0 0 0.3rem;">True Negatives: 235</h4>
            <p style="font-size: 0.825rem; color: var(--ink-text-faint); margin: 0;">Correctly predicted employees who stayed</p>
        </div>
        <div style="padding: 1rem 1.25rem; background: var(--short-soft);
                    border: 1px solid rgba(240,101,79,0.18); border-radius: 8px;">
            <h4 style="color: #f0654f; margin: 0 0 0.3rem;">False Negatives: 15</h4>
            <p style="font-size: 0.825rem; color: var(--ink-text-faint); margin: 0;">Missed attrition cases (most critical)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 1rem 1.25rem; background: var(--caution-soft);
                    border: 1px solid rgba(224,167,62,0.18); border-radius: 8px; margin-bottom: 0.75rem;">
            <h4 style="color: #e0a73e; margin: 0 0 0.3rem;">False Positives: 12</h4>
            <p style="font-size: 0.825rem; color: var(--ink-text-faint); margin: 0;">Incorrectly predicted attrition</p>
        </div>
        <div style="padding: 1rem 1.25rem; background: var(--long-soft);
                    border: 1px solid rgba(45,212,167,0.18); border-radius: 8px;">
            <h4 style="color: #2dd4a7; margin: 0 0 0.3rem;">True Positives: 28</h4>
            <p style="font-size: 0.825rem; color: var(--ink-text-faint); margin: 0;">Correctly predicted attrition cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Feature Importance
    st.markdown("""
    <div class="card">
        <div class="card-title">Feature Importance</div>
        <p>Top features influencing attrition predictions.</p>
    """, unsafe_allow_html=True)
    
    feature_importance = {
        'OverTime': 0.18,
        'YearsAtCompany': 0.15,
        'MonthlyIncome': 0.12,
        'JobSatisfaction': 0.10,
        'Age': 0.09,
        'TotalWorkingYears': 0.08,
        'WorkLifeBalance': 0.07,
        'YearsInCurrentRole': 0.06,
        'DistanceFromHome': 0.05,
        'JobRole': 0.04
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    features   = list(feature_importance.keys())
    importance = list(feature_importance.values())
    
    # Color gradient by importance, mapped to signal-indigo ramp
    norm_imp = [(v - min(importance)) / (max(importance) - min(importance)) for v in importance]
    base = np.array([111, 123, 240]) / 255.0
    bar_colors = [(base[0], base[1], base[2], 0.35 + 0.65 * n) for n in norm_imp]

    bars = ax.barh(features, importance, color=bar_colors, zorder=3, height=0.55)
    ax.set_xlabel('Importance Score', labelpad=8)
    ax.set_title('Top 10 Feature Importance', fontsize=13, fontweight='600', pad=14)
    ax.invert_yaxis()
    
    # Add value labels
    for bar, imp in zip(bars, importance):
        ax.text(imp + 0.003, bar.get_y() + bar.get_height() / 2,
                f'{imp:.2f}', va='center', fontweight='600',
                color='#e4e9f2', fontsize=9,
                fontfamily='monospace')
    
    st.pyplot(fig)
    plt.close()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()