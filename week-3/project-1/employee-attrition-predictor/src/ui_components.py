"""
Lumina UI Components
Shared design tokens, HTML builders, and cached pipeline loaders
for the Employee Attrition Predictor dashboard.

Design language: "Lumina Insights" — modern glassmorphism,
analytical navy -> predictive purple (Material 3 scheme).
"""

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
MODELS_DIR = PROJECT_ROOT / "models"
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"
ASSETS_DIR = PROJECT_ROOT / "assets"

# ── Design tokens ──────────────────────────────────────────────────────────
COLORS = {
    "primary": "#000666",
    "primary_container": "#1a237e",
    "on_primary": "#ffffff",
    "on_primary_container": "#8690ee",
    "surface_tint": "#4c56af",
    "primary_fixed": "#e0e0ff",
    "primary_fixed_dim": "#bdc2ff",
    "secondary": "#006b5f",
    "secondary_fixed": "#8df5e4",
    "on_secondary_container": "#007165",
    "tertiary": "#380b00",
    "tertiary_container": "#5c1800",
    "on_tertiary_container": "#e17c5a",
    "error": "#ba1a1a",
    "error_container": "#ffdad6",
    "on_error_container": "#93000a",
    "surface": "#fbf8ff",
    "surface_low": "#f5f2fb",
    "surface_container": "#efecf5",
    "surface_high": "#eae7ef",
    "surface_highest": "#e4e1ea",
    "surface_lowest": "#ffffff",
    "on_surface": "#1b1b21",
    "on_surface_variant": "#454652",
    "outline": "#767683",
    "outline_variant": "#c6c5d4",
    "background": "#f1f5f9",
    "risk_high": "#e17c5a",
    "risk_mid": "#b57614",
    "retain": "#006b5f",
    "alert": "#ba1a1a",
}

PIE_PALETTE = [COLORS["primary"], COLORS["primary_fixed_dim"], COLORS["secondary_fixed"]]
BAR_PALETTE = [
    COLORS["primary"],
    COLORS["surface_tint"],
    COLORS["on_primary_container"],
    COLORS["secondary"],
    COLORS["on_tertiary_container"],
    COLORS["risk_mid"],
]

DEFAULT_CONFIG = {
    "risk_threshold": 0.5,
    "low_bound_factor": 0.6,
    "sensitivity": "Balanced",
    "algorithm": "Logistic Regression",
    "n_estimators": 100,
    "max_depth": 10,
}

SENSITIVITY_PRESETS = {
    "Balanced": 0.5,
    "Conservative (raise alarm early)": 0.4,
    "Strict (fewer false alarms)": 0.6,
}


# ── Config persistence ─────────────────────────────────────────────────────
def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        try:
            cfg.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg


def save_config(cfg: dict) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def config_mtime() -> float:
    return CONFIG_FILE.stat().st_mtime if CONFIG_FILE.exists() else 0.0


# ── Asset injection ────────────────────────────────────────────────────────
_CSS_CACHE: str = ""


def ensure_assets() -> None:
    """Inject the design system (style.css + body fonts) on every rerun.

    Icons are inline SVG (no external icon font), so rendering never depends
    on a font-face loading over the network. A static-asset version seed is
    embedded so hard-refreshes always pick up the latest design system.
    """
    global _CSS_CACHE
    css_path = ASSETS_DIR / "style.css"
    if not css_path.exists():
        raise FileNotFoundError(f"CSS file not found: {css_path}")
    css = css_path.read_text(encoding="utf-8")
    if not css.strip():
        raise ValueError(f"CSS file is empty: {css_path}")
    _CSS_CACHE = css
    seed = str(int(sum(ord(c) for c in css) % 10**6)).zfill(6)
    guard = (
        "/* SVG-only design system — stale icon-font spans must never leak */"
        "span.material-symbols-outlined, span.material-symbols, [class*=material-symbols]{"
        "  font-family: inherit !important;"
        "  letter-spacing: 0 !important;"
        "  font-variant-ligatures: none !important;"
        "  font-feature-settings: normal !important;"
        "  display: none !important;"
        "  visibility: hidden !important;"
        "  width: 0 !important;"
        "  height: 0 !important;"
        "  overflow: hidden !important;"
        "}"
    )
    fonts = (
        "<link rel='preconnect' href='https://fonts.googleapis.com'>"
        "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
        "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&"
        "family=Roboto+Flex:opsz,wght@8..144,400;8..144,500;8..144,600&display=swap' rel='stylesheet'>"
    )

    # Split CSS at comment boundaries into chunks small enough that Streamlit
    # will not silently truncate them.  Each chunk gets its own <style> tag.
    chunks = _split_css(css, max_chars=12000)
    chunks.append(guard)
    for i, chunk in enumerate(chunks):
        st.markdown(
            f'<style data-lumina="{seed}-{i}">{chunk}</style>',
            unsafe_allow_html=True,
        )
    st.markdown(fonts, unsafe_allow_html=True)


def _split_css(css, max_chars=12000):
    """Split CSS into chunks at line boundaries, each <= max_chars."""
    lines = css.split("\n")
    chunks = []
    current = []
    current_len = 0
    for line in lines:
        if current_len + len(line) + 1 > max_chars and current:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks


# ── Inline SVG icons (feather-style, currentColor) ────────────────────────
def _svg(*parts, cls="ic-s", filled: bool = False) -> str:
    if filled:
        return "".join(parts)
    return "".join(
        p if p.startswith("<path") or p.startswith("<circle") or p.startswith("<rect")
        or p.startswith("<ellipse") or p.startswith("<line") or p.startswith("<poly")
        else p
        for p in parts
    )


_SVG_PATHS = {
    "auto_awesome": '<path d="M12 3l1.9 4.6L18.5 9.5l-4.6 1.9L12 16l-1.9-4.6L5.5 9.5l4.6-1.9L12 3z" fill="currentColor" stroke="none"/><path d="M19 14l.9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9L19 14z" fill="currentColor" stroke="none"/><path d="M5 14l.9 2.1L8 17l-2.1.9L5 20l-.9-2.1L2 17l2.1-.9L5 14z" fill="currentColor" stroke="none"/>',
    "search": '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/>',
    "notifications": '<path d="M6 9a6 6 0 0 1 12 0c0 5 2.5 6.5 2.5 6.5h-17S6 14 6 9z"/><line x1="10.3" y1="19.5" x2="13.7" y2="19.5"/>',
    "notifications_active": '<path d="M6 9a6 6 0 0 1 12 0c0 5 2.5 6.5 2.5 6.5h-17S6 14 6 9z"/><line x1="10.3" y1="19.5" x2="13.7" y2="19.5"/><path d="M18 5.3a7.6 7.6 0 0 1 0 8.9"/><path d="M20 3a10.8 10.8 0 0 1 0 13.4"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 1.6-2.9 2.4-2.9 4"/><circle cx="12" cy="17.6" r="0.9" fill="currentColor" stroke="none"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "group": '<circle cx="9" cy="8" r="3.6"/><path d="M2.5 20c.9-3.4 3.4-5 6.5-5s5.6 1.6 6.5 5"/><circle cx="17" cy="8.5" r="2.6"/><path d="M15.5 15.4c2.7.1 4.8 1.5 5.8 4.1"/>',
    "groups": '<circle cx="10.5" cy="8" r="3.4"/><path d="M2.8 20c.9-3.3 3.6-4.9 7-4.9s6.1 1.6 7 4.9"/><circle cx="17.5" cy="8" r="2.8"/><path d="M15.8 15.1c2.6.1 4.7 1.4 5.8 3.9"/>',
    "warning": '<path d="M12 4 2.8 20h18.4z"/><line x1="12" y1="10" x2="12" y2="14.2"/><circle cx="12" cy="17.4" r="0.8" fill="currentColor" stroke="none"/>',
    "trending_up": '<polyline points="3 17 9 11 13 15 21 7"/><polyline points="15 7 21 7 21 13"/>',
    "tune": '<line x1="4" y1="6" x2="20" y2="6"/><circle cx="14" cy="6" r="2.2"/><line x1="4" y1="12" x2="20" y2="12"/><circle cx="9" cy="12" r="2.2"/><line x1="4" y1="18" x2="20" y2="18"/><circle cx="16" cy="18" r="2.2"/>',
    "calendar_today": '<rect x="3" y="5" width="18" height="16" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/>',
    "g_automation": '<rect x="5" y="9" width="14" height="10" rx="2.5"/><line x1="12" y1="19" x2="12" y2="22"/><circle cx="12" cy="4.5" r="1.6"/><circle cx="9" cy="13.5" r="1" fill="currentColor" stroke="none"/><circle cx="15" cy="13.5" r="1" fill="currentColor" stroke="none"/>',
    "cloud_queue": '<path d="M6.5 18.5a4.5 4.5 0 0 1-.4-9A6 6 0 0 1 18 10.6a3.8 3.8 0 0 1-.5 7.9z"/>',
    "table_rows": '<rect x="3" y="5" width="18" height="14" rx="2"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="9" y1="5" x2="9" y2="19"/>',
    "view_column": '<rect x="4" y="5" width="4.7" height="14" rx="1"/><rect x="9.6" y="5" width="4.7" height="14" rx="1"/><rect x="15.3" y="5" width="4.7" height="14" rx="1"/>',
    "highlight_off": '<circle cx="12" cy="12" r="9"/><line x1="8.6" y1="8.6" x2="15.4" y2="15.4"/><line x1="15.4" y1="8.6" x2="8.6" y2="15.4"/>',
    "merge": '<circle cx="12" cy="5" r="2.2"/><circle cx="6" cy="19" r="2.4"/><circle cx="18" cy="19" r="2.4"/><path d="M12 7.2v8"/><path d="M12 15.2l-6 2.6M12 15.2l6 2.6"/>',
    "check_circle": '<circle cx="12" cy="12" r="9"/><polyline points="8.2 12.4 10.8 15 15.8 9.6"/>',
    "verified": '<path d="M12 2.6 14.3 5l3.5-.6.9 3.4 3 2-.9 3.4.9 3.4-3 2-.9 3.4-3.5-.6-2.3 2.4-2.3-2.4-3.5.6-.9-3.4-3-2 .9-3.4-.9-3.4 3-2 .9-3.4 3.5.6z"/><polyline points="8.6 12.2 11 14.6 15.4 9.8"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
    "rate_review": '<path d="M4 16V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H8z"/><line x1="9" y1="18.5" x2="7.5" y2="21"/><line x1="9" y1="18.5" x2="13" y2="18.5"/>',
    "show_chart": '<polyline points="3 17 8.5 11.5 12.5 15 21 7"/><line x1="21" y1="10" x2="21" y2="7"/><line x1="18" y1="7" x2="21" y2="7"/>',
    "restore": '<path d="M3.5 12a8.5 8.5 0 1 1 2.5 6"/><polyline points="3 6 3 11 8 11"/>',
    "favorite": '<path d="M12 20.5C7 16.5 4 13.5 4 10a4 4 0 0 1 8-1.6A4 4 0 0 1 20 10c0 3.5-3 6.5-8 10.5z" fill="currentColor" stroke="none"/>',
    "balance": '<line x1="12" y1="3.5" x2="12" y2="20.5"/><line x1="6" y1="6.5" x2="18" y2="6.5"/><path d="M4.5 10.5 7.5 6.5v4a2 2 0 0 1-3 0z"/><path d="m19.5 10.5-3-4v4a2 2 0 0 0 3 0z"/><line x1="5.5" y1="20.5" x2="18.5" y2="20.5"/>',
    "payments": '<rect x="3" y="6" width="18" height="13" rx="2"/><circle cx="12" cy="12.5" r="2.2"/><line x1="6" y1="15.5" x2="9" y2="15.5"/><line x1="15" y1="15.5" x2="18" y2="15.5"/>',
    "school": '<path d="M2.5 9.5 12 4.5l9.5 5L12 14.5z"/><polyline points="7 12.5 7 17c0 1.4 5 2.4 10 2.4s10-1 10-2.4v-4.5"/><line x1="17.5" y1="12.6" x2="17.5" y2="17"/>',
    "home": '<path d="M3.5 11 12 3.5 20.5 11"/><path d="M5.5 9.5V20h13V9.5"/><line x1="10" y1="20" x2="10" y2="14" /><line x1="14" y1="20" x2="14" y2="14"/>',
    "circle": '<circle cx="12" cy="12" r="6" fill="currentColor" stroke="none"/>',
    "insights": '<path d="M12 3.5 13.7 8l4.5 1.7-4.5 1.7-1.7 4.5-1.7-4.5-4.5-1.7L10.3 8z"/><path d="M18.5 15.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/><line x1="5" y1="19" x2="19" y2="19"/>',
    "stat_minus": '<line x1="4" y1="12" x2="8" y2="12"/><polyline points="10 12 14 8 18 12"/><line x1="14" y1="8" x2="14" y2="16"/><line x1="19" y1="16" x2="20" y2="16"/>',
    "visible": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "database": '<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "monitoring": '<polyline points="4 20 4 13"/><polyline points="10 20 10 7"/><polyline points="16 20 16 12"/><polyline points="22 20 22 15"/><line x1="2" y1="20" x2="22" y2="20"/>',
    "campaign": '<path d="M3 11v2h3l4 3V8l-4 3H3z"/><path d="M14 9.5a4 4 0 0 1 0 5"/><path d="M17 7a8 8 0 0 1 0 10"/>',
    "science": '<path d="M8 3h8"/><line x1="12" y1="3" x2="12" y2="8"/><path d="M5.5 21h13L14 10h-4z"/><line x1="10" y1="14" x2="14" y2="14"/>',
    "history": '<path d="M3.5 12a8.5 8.5 0 1 1 2.5 6"/><polyline points="3 6 3 11 8 11"/><polyline points="12 8 12 12 15 14"/>',
    "hub": '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="17" r="2"/><circle cx="19" cy="17" r="2"/><line x1="11" y1="6.8" x2="6.2" y2="15.2"/><line x1="13" y1="6.8" x2="17.8" y2="15.2"/>',
    "space_dashboard": '<rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="5" rx="1.5"/><rect x="13" y="10" width="8" height="11" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/>',
    "query_stats": '<polyline points="3 17 8.5 11.5 12.5 15 21 7"/><circle cx="18" cy="6" r="1.5" fill="currentColor" stroke="none"/><circle cx="16" cy="17" r="2"/><circle cx="8" cy="14" r="2"/>',
    "travel_explore": '<circle cx="8" cy="16" r="5"/><polyline points="11.6 12.4 21 3"/><line x1="16" y1="3" x2="21" y2="3"/><line x1="21" y1="3" x2="21" y2="8"/>',
    "arrow_forward": '<line x1="4" y1="12" x2="20" y2="12"/><polyline points="13 5 20 12 13 19"/>',
    "arrow_back": '<line x1="20" y1="12" x2="4" y2="12"/><polyline points="11 5 4 12 11 19"/>',
    "arrow_upward": '<line x1="12" y1="20" x2="12" y2="4"/><polyline points="5 13 12 6 19 13"/>',
    "arrow_downward": '<line x1="12" y1="4" x2="12" y2="20"/><polyline points="5 11 12 18 19 11"/>',
    "chevron_right": '<polyline points="9 6 15 12 9 18"/>',
    "chevron_down": '<polyline points="6 9 12 15 18 9"/>',
    "close": '<line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/>',
    "info": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16.5"/><circle cx="12" cy="7.8" r="0.9" fill="currentColor" stroke="none"/>',
    "open_in_new": '<path d="M13 5h6v6"/><path d="M19 5 10.5 13.5"/><path d="M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4"/>',
    "download": '<line x1="12" y1="4" x2="12" y2="15.5"/><polyline points="7.5 11 12 15.5 16.5 11"/><path d="M4.5 19.5h15"/>',
    "refresh": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8"/><polyline points="20 3 20 8 15 8"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 16"/><polyline points="4 21 4 16 9 16"/>',
    "launch": '<path d="M14 5h5v5"/><path d="M19 5 11 13"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5"/>',
    "keyboard_double_arrow_left": '<polyline points="15 5 8 12 15 19"/><polyline points="11 5 4 12 11 19"/>',
    "keyboard_double_arrow_right": '<polyline points="9 5 16 12 9 19"/><polyline points="13 5 20 12 13 19"/>',
}


def icon(name: str, cls: str = "", size: int = 20, color: str = "") -> str:
    """Inline SVG icon. Rendering is self-contained — no icon font needed."""
    body = _SVG_PATHS.get(name) or _SVG_PATHS["circle"]
    style = f"width:{size}px;height:{size}px;"
    if color:
        style += f"color:{color};"
    return (
        f'<svg class="lumina-ic {cls}" viewBox="0 0 24 24" width="{size}" height="{size}" '
        f'style="{style}" fill="none" stroke="currentColor" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
    )


def eyebrow(text: str) -> str:
    return f'<div class="lumina-eyebrow">{text}</div>'


def lumina_section(title: str, right: str = "") -> str:
    """Section header (headline-md style) — plain, no card background."""
    r = f'<span style="margin-left:auto;">{right}</span>' if right else ""
    return (
        f'<div class="lumina-section">'
        f'<span class="lumina-section-title">{title}</span>{r}</div>'
    )


def page_header(title: str, subtitle: str = "", chips: list = None) -> str:
    chips_html = ""
    if chips:
        chips_html = "<div style='display:flex;gap:8px;flex-wrap:wrap;'>" + "".join(chips) + "</div>"
    sub = f'<div class="lumina-sub">{subtitle}</div>' if subtitle else ""
    return (
        '<div style="display:flex;align-items:flex-start;justify-content:space-between;'
        'gap:16px;flex-wrap:wrap;margin:4px 0 20px;">'
        f'<div><div class="lumina-h1">{title}</div>{sub}</div>{chips_html}</div>'
    )


def status_chip(text: str, kind: str = "neutral") -> str:
    return f'<span class="status-chip {kind}">{icon("circle", size=10)} {text}</span>'


def kpi_card(
    label: str,
    value: str,
    icon_name: str = "stat_minus",
    ic_class: str = "ic-primary",
    delta: str = "",
    delta_kind: str = "neutral",
    delta_icon: str = "trending_flat",
    chip: str = "",
    chip_kind: str = "neutral",
    sparkline: str = "",
) -> str:
    delta_html = ""
    if delta:
        delta_html = (
            f'<span class="kpi-delta {delta_kind}">{icon(delta_icon, size=14)} {delta}</span>'
        )
    chip_html = (
        f'<span class="kpi-chip {chip_kind}">{chip}</span>' if chip else ""
    )
    spark_html = f'<div style="position:relative;z-index:2;margin-top:12px;">{sparkline}</div>' if sparkline else ""
    return f"""
    <div class="lumina-kpi glass-card">
      <div class="card-ambient"></div>
      <div class="kpi-top">
        <span class="lumina-label">{label}</span>
        <span class="kpi-ic {ic_class}">{icon(icon_name, size=18)}</span>
      </div>
      <div class="kpi-value-row">
        <span class="kpi-value">{value}</span>
        {delta_html}
        {chip_html}
      </div>
      {spark_html}
    </div>
    """


def bar_row(label: str, pct: float, value_text: str, fill_class: str = "") -> str:
    """Feature-impact row: fixed label column, flex bar, right-aligned tag.

    Wrapped as a CSS grid so the bar can never paint over the label/tag.
    """
    pct = max(0.0, min(1.0, pct))
    safe_label = (label or "").replace("<", "&lt;").replace(">", "&gt;")
    safe_tag = (value_text or "").replace("<", "&lt;").replace(">", "&gt;")
    return (
        '<div class="lumina-bar-row" title="' + safe_label + '">'
        f'<span class="lumina-bar-label">{safe_label}</span>'
        f'<div class="lumina-bar" aria-hidden="true">'
        f'<div class="lumina-bar-fill {fill_class}" style="width:{pct * 100:.1f}%;"></div></div>'
        f'<span class="lumina-bar-tag">{safe_tag}</span>'
        "</div>"
    )


def cm_grid(tn: int, fp: int, fn: int, tp: int) -> str:
    return f"""
    <div class="cm-grid">
      <div></div>
      <div class="cm-head">Predicted: No churn</div>
      <div class="cm-head">Predicted: Churn</div>
      <div class="cm-rowlabel">Actual: No churn</div>
      <div class="cm-cell tn"><span>{tn}</span><span class="cm-cap">True Negative</span></div>
      <div class="cm-cell fp"><span>{fp}</span><span class="cm-cap">False Positive</span></div>
      <div class="cm-rowlabel">Actual: Churn</div>
      <div class="cm-cell fn"><span>{fn}</span><span class="cm-cap">False Negative</span></div>
      <div class="cm-cell tp"><span>{tp}</span><span class="cm-cap">True Positive</span></div>
    </div>
    """


def lumina_table(headers: list, rows: list, aligns: list = None) -> str:
    th = []
    for i, h in enumerate(headers):
        cls = (aligns or [])[i] if aligns else ""
        th.append(f'<th class="{cls}">{h}</th>')
    body = ""
    for row in rows:
        tds = "".join(f"<td>{c}</td>" for c in row)
        body += f"<tr>{tds}</tr>"
    return f'<table class="lumina-table"><thead><tr>{"".join(th)}</tr></thead><tbody>{body}</tbody></table>'


# ── Cached data / pipeline ─────────────────────────────────────────────────
_DATA_URLS = [
    "https://raw.githubusercontent.com/IBM/employee-attrition-predictor/refs/heads/main/data/WA_Fn-UseC_-HR-Employee-Attrition.csv",
    "https://raw.githubusercontent.com/ANONIMOWA11/Employee-Attrition-Prediction/main/WA_Fn-UseC_-HR-Employee-Attrition.csv",
]


def ensure_data_file() -> None:
    """Download the IBM HR dataset if it is missing (e.g. on Streamlit Cloud)."""
    if DATA_FILE.exists():
        return
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    import urllib.request
    for url in _DATA_URLS:
        try:
            urllib.request.urlretrieve(url, DATA_FILE)
            if DATA_FILE.stat().st_size > 1000:
                return
        except Exception:
            DATA_FILE.unlink(missing_ok=True)
    raise FileNotFoundError(
        f"Could not download dataset. Place WA_Fn-UseC_-HR-Employee-Attrition.csv in {DATA_FILE.parent}"
    )


@st.cache_data(show_spinner="Loading dataset\u2026")
def load_cached_data(_mtime: float) -> pd.DataFrame:
    ensure_data_file()
    return pd.read_csv(DATA_FILE)


@st.cache_resource(show_spinner="Loading model\u2026")
def load_pipeline(_mtime: float):
    from src.preprocessor import DataPreprocessor

    required = [
        MODELS_DIR / "best_model.pkl",
        MODELS_DIR / "scaler.pkl",
        MODELS_DIR / "label_encoders.pkl",
        MODELS_DIR / "feature_columns.pkl",
    ]
    missing = [p for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            f"Missing model artifacts: {[str(p.name) for p in missing]}. "
            "Retraining will be triggered automatically."
        )
    model = joblib.load(MODELS_DIR / "best_model.pkl")
    pre = DataPreprocessor()
    pre.scaler = joblib.load(MODELS_DIR / "scaler.pkl")
    pre.label_encoders = joblib.load(MODELS_DIR / "label_encoders.pkl")
    pre.feature_columns = joblib.load(MODELS_DIR / "feature_columns.pkl")
    return model, pre


def artifact_mtime() -> tuple:
    def m(p):
        return p.stat().st_mtime if p.exists() else 0.0

    return (
        m(MODELS_DIR / "best_model.pkl"),
        m(MODELS_DIR / "scaler.pkl"),
        m(MODELS_DIR / "label_encoders.pkl"),
        m(MODELS_DIR / "feature_columns.pkl"),
    )


def model_type_label(model) -> str:
    name = model.__class__.__name__
    mapping = {
        "LogisticRegression": "Logistic Regression",
        "RandomForestClassifier": "Random Forest",
        "GradientBoostingClassifier": "Gradient Boosting",
    }
    return mapping.get(name, name)


def risk_tier(proba: float, cfg: dict) -> str:
    hi = float(cfg.get("risk_threshold", 0.5))
    lo = hi * float(cfg.get("low_bound_factor", 0.6))
    if proba >= hi:
        return "High"
    if proba >= lo:
        return "Medium"
    return "Low"


def risk_chip(proba: float, cfg: dict) -> str:
    tier = risk_tier(proba, cfg)
    kind = {"High": "high", "Medium": "medium", "Low": "low"}[tier]
    return status_chip(tier, kind)


def score_dataframe(df: pd.DataFrame, model, pre) -> pd.DataFrame:
    """Score every employee through the full pipeline (encode + scale) with the deployed model."""
    cfg = load_config()
    X = pre.transform(df)
    out = df.copy().reset_index(drop=True)
    out["AttritionProbability"] = model.predict_proba(X)[:, 1]
    out["RiskTier"] = out["AttritionProbability"].apply(lambda p: risk_tier(p, cfg))
    return out


def centered_pill(text: str, kind: str = "active") -> str:
    return f'<div style="text-align:center;margin:8px 0;"><span class="status-chip {kind}">{text}</span></div>'