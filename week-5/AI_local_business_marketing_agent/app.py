"""
AI Local Business Marketing Agent
Streamlit Application - Complete Marketing Automation Suite
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from config.settings import APP_CONFIG, BUSINESS_TYPES, PLATFORMS
from models.content_generator import ContentGenerator
from models.social_media import SocialMediaManager
from models.email_campaign import EmailCampaignGenerator
from models.whatsapp_campaign import WhatsAppCampaignGenerator
from models.google_business import GoogleBusinessManager
from models.sentiment_analyzer import SentimentAnalyzer
from utils.database import DatabaseManager
from utils.analytics import AnalyticsEngine
from frontend.components.dashboard import DashboardComponent
from frontend.components.campaign_creator import CampaignCreator
from frontend.components.analytics import AnalyticsComponent
from frontend.components.settings import SettingsComponent

# Page configuration
st.set_page_config(
    page_title="AI Local Business Marketing Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (loaded with a path that is robust to the working directory)
def load_css():
    css_path = Path(__file__).parent / 'frontend' / 'styles' / 'custom.css'
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Navigation options (single source of truth) — top navigation bar
# Keys are plain strings (no emojis) to keep state matching reliable.
NAV_OPTIONS = [
    {"key": "dashboard", "icon": "M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z", "label": "Dashboard"},
    {"key": "create", "icon": "M12 5v14M5 12h14", "label": "Create"},
    {"key": "social", "icon": "M17 8a4 4 0 0 0-8 0M7 20a5 5 0 0 1 10 0M12 3v2", "label": "Social"},
    {"key": "email", "icon": "M4 6h16v12H4zM4 7l8 6 8-6", "label": "Email"},
    {"key": "whatsapp", "icon": "M21 11.5a8.5 8.5 0 1 1-3.6-6.9M9 9a8 8 0 0 0 6 6", "label": "WhatsApp"},
    {"key": "google", "icon": "M12 21s-7-4.5-7-10a7 7 0 0 1 14 0c0 5.5-7 10-7 10zM12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z", "label": "Google"},
    {"key": "analytics", "icon": "M5 19V9M12 19V5M19 19v-7", "label": "Analytics"},
    {"key": "settings", "icon": "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19 12a7 7 0 0 0-.1-1.2l2-1.5-2-3.4-2.3 1a7 7 0 0 0-2-1.2L14 3h-4l-.6 2.7a7 7 0 0 0-2 1.2l-2.3-1-2 3.4 2 1.5A7 7 0 0 0 5 12c0 .4 0 .8.1 1.2l-2 1.5 2 3.4 2.3-1a7 7 0 0 0 2 1.2L10 21h4l.6-2.7a7 7 0 0 0 2-1.2l2.3 1 2-3.4-2-1.5c.1-.4.1-.8.1-1.2z", "label": "Settings"},
    {"key": "history", "icon": "M3 12a9 9 0 1 0 3-6.7M3 4v4h4M12 8v4l3 2", "label": "History"},
]
NAV_DEFAULT = "dashboard"


def load_campaigns_into_session(db: DatabaseManager):
    """Load persisted campaigns from the database into session state for display."""
    try:
        rows = db.get_campaigns()
    except Exception:
        rows = []
    campaigns = []
    for r in rows:
        campaigns.append({
            'id': r.get('id'),
            'name': r.get('name', 'Unnamed Campaign'),
            'type': r.get('type', 'promotional'),
            'platform': r.get('platform', 'social_media'),
            'business_type': r.get('business_type', 'shop'),
            'content': r.get('content', ''),
            'status': r.get('status', 'draft'),
            'created_at': str(r.get('created_at', '')),
            'published_at': str(r.get('published_at') or ''),
            'metadata': r.get('metadata', {}) or {},
            'engagement': r.get('engagement_data', {}) or {},
        })
    return campaigns


# Initialize session state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
    if 'business_profile' not in st.session_state:
        st.session_state.business_profile = {
            'name': 'Demo Business',
            'type': 'restaurant',
            'email': 'demo@business.com',
            'phone': '+1234567890',
            'address': '123 Main Street',
            'website': 'www.demobusiness.com',
            'description': 'Your business description here'
        }
    if 'nav' not in st.session_state:
        st.session_state.nav = NAV_DEFAULT
    if 'campaign_history' not in st.session_state:
        st.session_state.campaign_history = []
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    if 'edit_campaign' not in st.session_state:
        st.session_state.edit_campaign = None

init_session_state()


# Initialize components
@st.cache_resource
def init_components():
    db_manager = DatabaseManager()
    content_generator = ContentGenerator()
    social_media = SocialMediaManager()
    email_generator = EmailCampaignGenerator()
    whatsapp_generator = WhatsAppCampaignGenerator()
    google_manager = GoogleBusinessManager()
    sentiment_analyzer = SentimentAnalyzer()
    analytics = AnalyticsEngine(db_manager)

    return {
        'db': db_manager,
        'content': content_generator,
        'social': social_media,
        'email': email_generator,
        'whatsapp': whatsapp_generator,
        'google': google_manager,
        'sentiment': sentiment_analyzer,
        'analytics': analytics
    }

components = init_components()

# Populate session campaigns from the database (once per session)
if not st.session_state.campaign_history and components.get('db'):
    st.session_state.campaign_history = load_campaigns_into_session(components['db'])


# Branded header
def goto(nav: str):
    """Programmatically navigate."""
    st.session_state.nav = nav
    st.session_state["nav_radio"] = nav

def render_header():
    profile = st.session_state.get('business_profile', {})
    name = profile.get('name', 'Your Business')
    st.markdown(f"""
    <div class="app-header">
        <div class="app-header-left">
            <div class="app-logo">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#04121a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
            </div>
            <div>
                <div class="app-title">AI Marketing Agent</div>
                <div class="app-subtitle">{APP_CONFIG.get('description', '')}</div>
            </div>
        </div>
        <div class="app-header-right">
            <div class="app-business">
                <span class="app-business-dot"></span>
                <span>{name}</span>
            </div>
        </div>
    </div>
    <script>
    (function(){{
        function animateValue(el, end){{
            const raw = el.textContent.replace(/[^0-9.]/g,'');
            const isFloat = raw.indexOf('.') > -1;
            const start = 0; const dur = 1100; const t0 = performance.now();
            const suffix = el.textContent.replace(/[0-9.,]/g,'');
            function tick(now){{
                const p = Math.min((now - t0)/dur, 1);
                const eased = 1 - Math.pow(1-p, 3);
                const val = start + (end-start)*eased;
                el.textContent = (isFloat ? val.toFixed(0) : Math.round(val).toLocaleString()) + suffix;
                if(p<1) requestAnimationFrame(tick);
            }}
            requestAnimationFrame(tick);
        }}
        const els = document.querySelectorAll('.metric-value');
        els.forEach(el=>{{
            const num = parseFloat(el.textContent.replace(/[^0-9.]/g,''));
            if(!isNaN(num)) animateValue(el, num);
        }});
    }})();
    </script>
    """, unsafe_allow_html=True)

# Left Icon Rail Navigation (replaces the native Streamlit sidebar)
# Rendered inside a Streamlit column so it always shows and aligns.
def render_sidebar(rail_col):
    current = st.session_state.nav
    profile = st.session_state.get('business_profile', {})
    name = profile.get('name', 'Business')

    with rail_col:
        # Brand mark
        st.markdown(
            '<div class="rail-logo">'
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#04121a" '
            'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="rail-sep"></div>', unsafe_allow_html=True)
        st.markdown('<div class="rail-buttons">', unsafe_allow_html=True)

        # Nav items as real Streamlit buttons (always visible + clickable)
        for opt in NAV_OPTIONS:
            is_active = (opt["key"] == current)
            if st.button(
                opt["label"],
                key=f"nav_{opt['key']}",
                help=opt["label"],
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.nav = opt["key"]
                st.session_state["nav_radio"] = opt["key"]
                st.rerun()

        st.markdown('<div class="rail-sep"></div>', unsafe_allow_html=True)
        if st.button("Logout", key="nav_logout", help="Logout",
                     use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    return current

def render_login():
    """Simple, functional login gate shown when the user is logged out."""
    st.markdown("""
    <div class="login-wrap">
        <div class="login-card">
            <div class="login-logo">
                <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#04121a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>
            </div>
            <div class="login-title">AI Local Business Marketing Agent</div>
            <div class="login-sub">Sign in to your marketing workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", value="demo@business.com")
        password = st.text_input("Password", type="password", value="demo1234")
        submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
        if submitted:
            st.session_state.authenticated = True
            st.rerun()

def main():
    if not st.session_state.authenticated:
        render_login()
        return

    render_header()

    # Two-column layout: slim icon rail on the left, content on the right.
    rail_col, content_col = st.columns([1.1, 6])

    with rail_col:
        render_sidebar(rail_col)

    with content_col:
        # Initialize components from cache
        dashboard = DashboardComponent(components)
        campaign_creator = CampaignCreator(components)
        analytics_component = AnalyticsComponent(components)
        settings_component = SettingsComponent(components)
        
        # Use cached components for other pages
        social_media_manager = components.get('social')
        email_generator = components.get('email')
        whatsapp_generator = components.get('whatsapp')
        google_manager = components.get('google')

        # Render selected page (driven by session state so navigation is reliable)
        nav = st.session_state.nav

        st.markdown('<div class="page-body fade-up">', unsafe_allow_html=True)

        if nav == "dashboard":
            dashboard.render()

        elif nav == "create":
            campaign_creator.render()

        elif nav == "social":
            if social_media_manager:
                social_media_manager.render_ui()
            else:
                st.error("Social media manager not available")

        elif nav == "email":
            if email_generator:
                email_generator.render_ui()
            else:
                st.error("Email generator not available")

        elif nav == "whatsapp":
            if whatsapp_generator:
                whatsapp_generator.render_ui()
            else:
                st.error("WhatsApp generator not available")

        elif nav == "google":
            if google_manager:
                google_manager.render_ui()
            else:
                st.error("Google Business manager not available")

        elif nav == "analytics":
            analytics_component.render()

        elif nav == "settings":
            settings_component.render()

        elif nav == "history":
            render_campaign_history()

        st.markdown('</div>', unsafe_allow_html=True)


def render_campaign_history():
    if not st.session_state.campaign_history:
        st.info("No campaigns created yet. Start by creating your first campaign!")
        return

    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        platform_filter = st.selectbox("Platform", ["All"] + list(PLATFORMS.keys()))
    with col2:
        date_range = st.date_input("Date Range", [datetime.now() - timedelta(days=30), datetime.now()])
    with col3:
        status_filter = st.selectbox("Status", ["All", "Draft", "Published", "Scheduled", "Archived"])

    # Filter campaigns
    filtered_campaigns = st.session_state.campaign_history

    if platform_filter != "All":
        filtered_campaigns = [c for c in filtered_campaigns if c.get('platform') == platform_filter]

    if status_filter != "All":
        filtered_campaigns = [c for c in filtered_campaigns if (c.get('status') or '').capitalize() == status_filter]

    if not filtered_campaigns:
        st.info("No campaigns match the selected filters.")
        return

    # Display campaigns
    for campaign in filtered_campaigns:
        camp_id = campaign.get('id')
        with st.expander(f"{campaign.get('name', 'Unnamed')} - {campaign.get('date', campaign.get('created_at', 'N/A')[:10] if campaign.get('created_at') else 'N/A')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Platform:** {campaign.get('platform', 'N/A')}")
                st.write(f"**Status:** {campaign.get('status', 'N/A')}")
                st.write(f"**Type:** {campaign.get('type', 'N/A')}")
            with col2:
                st.write(f"**Reach:** {campaign.get('engagement', {}).get('reach', 0):,}")
                st.write(f"**Engagement:** {campaign.get('engagement', {}).get('likes', 0) + campaign.get('engagement', {}).get('comments', 0) + campaign.get('engagement', {}).get('shares', 0):,}")
                st.write(f"**Created:** {campaign.get('created_at', 'N/A')}")

            if campaign.get('content'):
                st.markdown("**Content Preview:**")
                st.text(campaign['content'][:200] + "..." if len(campaign['content']) > 200 else campaign['content'])

            # Actions
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("View Analytics", key=f"analytics_{camp_id}"):
                    goto("analytics")
                    st.rerun()
            with col2:
                if st.button("Edit", key=f"edit_{camp_id}"):
                    st.session_state.edit_campaign = campaign
                    goto("create")
                    st.rerun()
            with col3:
                if st.button("🔄 Duplicate", key=f"duplicate_{camp_id}"):
                    clone = dict(campaign)
                    clone.pop('id', None)
                    clone['status'] = 'draft'
                    clone['name'] = f"{campaign.get('name', 'Campaign')} (Copy)"
                    if components.get('db'):
                        clone['id'] = components['db'].save_campaign(clone)
                    st.session_state.campaign_history.append(clone)
                    st.success("Campaign duplicated!")
                    st.rerun()
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{camp_id}"):
                    if camp_id is not None and components.get('db'):
                        components['db'].delete_campaign(camp_id)
                    st.session_state.campaign_history = [
                        c for c in st.session_state.campaign_history if c.get('id') != camp_id
                    ]
                    st.success("Campaign deleted!")
                    st.rerun()


if __name__ == "__main__":
    main()