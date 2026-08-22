"""
Lumina Charts
Light-theme Plotly figure builders and lightweight SVG helpers.
All figures are tuned for the glass / analytical-navy design system.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from src.ui_components import COLORS, PIE_PALETTE, BAR_PALETTE, MODELS_DIR

FONT_STACK = "Inter, 'Roboto Flex', -apple-system, sans-serif"

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=FONT_STACK, color="#1a1a2e", size=13),
    margin=dict(l=8, r=8, t=36, b=8),
    colorway=BAR_PALETTE,
)


def style_fig(fig: go.Figure, title: str = "", height: int = 360) -> go.Figure:
    fig.update_layout(**BASE_LAYOUT, title=dict(text=title, font=dict(size=16, color="#1a1a2e", family=FONT_STACK)), height=height)
    fig.update_xaxes(
        gridcolor="rgba(198,197,212,0.35)", linecolor="rgba(198,197,212,0.6)",
        zeroline=False, tickfont=dict(size=12, color="#1a1a2e"),
    )
    fig.update_yaxes(
        gridcolor="rgba(198,197,212,0.35)", linecolor="rgba(198,197,212,0.6)",
        zeroline=False, tickfont=dict(size=12, color="#1a1a2e"),
    )
    return fig


def donut(labels, values, title="", height=320, palette=None, hole=0.62):
    palette = palette or PIE_PALETTE
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=hole,
            textinfo="label",
            textposition="outside",
            marker=dict(colors=palette, line=dict(color=COLORS["surface"], width=2)),
            hovertemplate="%{label}<br>%{value:,} · %{percent}<extra></extra>",
        )
    )
    fig.update_layout(**BASE_LAYOUT, title=dict(text=title, font=dict(size=15, color="#1a1a2e", family=FONT_STACK)), height=height, showlegend=False)
    fig.update_traces(textfont=dict(family=FONT_STACK, size=13))
    return fig


def hbar(df, x, y, title="", height=None, marker_color=None, ascending=False):
    d = df.sort_values(x, ascending=ascending)
    fig = go.Figure(
        go.Bar(
            x=d[x],
            y=d[y].astype(str),
            orientation="h",
            marker=dict(
                color=marker_color or COLORS["primary"],
                line=dict(color="rgba(255,255,255,0.6)", width=1),
            ),
            hovertemplate="%{y}: %{x:,}<extra></extra>",
        )
    )
    return style_fig(fig, title=title, height=height or (38 * len(d) + 120))


def vbar(df, x, y, title="", height=360, color=None):
    d = df.sort_values(x, ascending=False)
    fig = go.Figure(
        go.Bar(
            x=d[x],
            y=d[y],
            marker=dict(color=color or COLORS["surface_tint"], line=dict(color="rgba(255,255,255,0.6)", width=1)),
            hovertemplate="%{x}: %{y:,}<extra></extra>",
        )
    )
    return style_fig(fig, title=title, height=height)


def roc_curve(fpr, tpr, auc, title=""):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=fpr, y=tpr, mode="lines", name=f"AUC = {auc:.3f}",
            line=dict(color=COLORS["primary"], width=3, shape="spline"),
            fill="tozeroy", fillcolor="rgba(0,6,102,0.06)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines", name="Chance",
            line=dict(color="rgba(118,118,131,0.5)", width=1.5, dash="dash"),
        )
    )
    fig.update_layout(
        **BASE_LAYOUT,
        title=dict(text=title or "ROC Curve", font=dict(size=15, color="#1a1a2e", family=FONT_STACK)),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(title="False positive rate", range=[0, 1], tickfont=dict(size=12, color="#1a1a2e"), titlefont=dict(size=13, color="#1a1a2e"))
    fig.update_yaxes(title="True positive rate", range=[0, 1], tickfont=dict(size=12, color="#1a1a2e"), titlefont=dict(size=13, color="#1a1a2e"))
    return fig


def feature_importance_bars(features, values, title="Top contributing factors", top_n=10):
    d = pd.DataFrame({"f": features[:top_n], "v": values[:top_n]})
    colors = [
        COLORS["risk_high"] if v > 0 else COLORS["retain"]
        for v in d["v"]
    ]
    fig = go.Figure(
        go.Bar(
            x=d["f"],
            y=d["v"],
            marker=dict(color=colors, line=dict(color="rgba(255,255,255,0.6)", width=1)),
            hovertemplate="%{x}: %{y:.3f}<extra></extra>",
        )
    )
    fig.update_layout(**BASE_LAYOUT, title=dict(text=title, font=dict(size=15, color="#1a1a2e", family=FONT_STACK)), height=400)
    fig.update_xaxes(tickangle=-35, tickfont=dict(size=12, color="#1a1a2e"))
    fig.update_yaxes(tickfont=dict(size=12, color="#1a1a2e"))
    return fig


def sparkline_svg(series, color="#4c56af", width=140, height=36, fill_color="rgba(0,6,102,0.10)"):
    """Inline SVG sparkline for KPI cards (no JS / plotly dependency)."""
    series = np.asarray(series, dtype=float)
    if len(series) < 2:
        series = [0, 0]
    vmin, vmax = float(series.min()), float(series.max())
    span = (vmax - vmin) or 1.0
    px_w, px_h = width, height
    pad = 3
    step = (px_w - 2 * pad) / (len(series) - 1)
    pts = []
    for i, v in enumerate(series):
        x = pad + i * step
        y = pad + (px_h - 2 * pad) * (1 - (v - vmin) / span)
        pts.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(pts)
    area_pts = f"{pad},{px_h} {polyline} {px_w - pad},{px_h}"
    return (
        f'<svg width="{px_w}" height="{px_h}" viewBox="0 0 {px_w} {px_h}" '
        f'xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;max-width:{px_w}px;height:auto;">'
        f'<defs><linearGradient id="spg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{color}" stop-opacity="0.35"/>'
        f'<stop offset="100%" stop-color="{color}" stop-opacity="0.0"/>'
        f'</linearGradient></defs>'
        f'<polygon points="{area_pts}" fill="url(#spg)"/>'
        f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
        f'<circle cx="{pts[-1].split(",")[0]}" cy="{pts[-1].split(",")[1]}" r="2.5" fill="{color}"/>'
        f'</svg>'
    )


def empty_placeholder(message="No data", icon_name="insights"):
    import streamlit as st
    from src.ui_components import icon

    st.markdown(
        f'<div class="glass-card" style="padding:48px;text-align:center;color:var(--lumina-outline);">'
        f'{icon(icon_name, size=40)}{message}</div>',
        unsafe_allow_html=True,
    )