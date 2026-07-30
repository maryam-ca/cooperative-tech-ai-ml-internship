"""
Sidebar Component - Navigation sidebar with user info
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any

class SidebarComponent:
    """Render the navigation sidebar"""
    
    def __init__(self, components: Dict[str, Any]):
        self.components = components
    
    def render(self):
        """Render the sidebar"""
        with st.sidebar:
            # Logo
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <span style="font-size: 3rem;">🚀</span>
                <h3 style="margin: 0;">AI Marketing</h3>
                <p style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Local Business Agent</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navigation
            nav_options = self._get_navigation()
            
            selected = st.radio(
                "Navigation",
                options=list(nav_options.keys()),
                format_func=lambda x: nav_options[x]
            )
            
            st.markdown("---")
            
            # Business info
            self._render_business_info()
            
            st.markdown("---")
            
            # Quick stats
            self._render_quick_stats()
            
            st.markdown("---")
            
            # User actions
            self._render_user_actions()
            
            return selected
    
    def _get_navigation(self) -> Dict[str, str]:
        """Get navigation options"""
        return {
            "dashboard": "📊 Dashboard",
            "create": "📝 Create Campaign",
            "social": "📱 Social Media",
            "email": "📧 Email Campaigns",
            "whatsapp": "💬 WhatsApp",
            "google": "📍 Google Business",
            "analytics": "📈 Analytics",
            "settings": "⚙️ Settings",
            "history": "📚 Campaign History"
        }
    
    def _render_business_info(self):
        """Render business information in sidebar"""
        profile = st.session_state.get('business_profile', {})
        
        if profile:
            name = profile.get('name', 'My Business')
            business_type = profile.get('type', 'shop')
            icon = {'restaurant': '🍽️', 'gym': '💪', 'shop': '🛍️', 'clinic': '🏥'}.get(business_type, '🏢')
            
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 0.8rem; border-radius: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.5rem;">{icon}</span>
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem;">{name[:20]}</div>
                        <div style="color: rgba(255,255,255,0.5); font-size: 0.7rem;">{business_type.title()}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👤 No business profile set")
    
    def _render_quick_stats(self):
        """Render quick statistics"""
        campaigns = st.session_state.get('campaign_history', [])
        published = len([c for c in campaigns if c.get('status') == 'published'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Campaigns", len(campaigns))
        with col2:
            st.metric("Published", published)
    
    def _render_user_actions(self):
        """Render user actions"""
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        if st.button("📖 Help", use_container_width=True):
            st.info("📚 Documentation available")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()